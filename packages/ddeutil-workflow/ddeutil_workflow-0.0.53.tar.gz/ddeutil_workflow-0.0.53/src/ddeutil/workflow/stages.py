# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
# [x] Use dynamic config
"""Stage model. It stores all stage model that use for getting stage data template
from the Job Model. The stage handle the minimize task that run in some thread
(same thread at its job owner) that mean it is the lowest executor of a workflow
that can tracking logs.

    The output of stage execution only return 0 status because I do not want to
handle stage error on this stage model. I think stage model should have a lot of
use-case, and it does not worry when I want to create a new one.

    Execution   --> Ok      --> Result with SUCCESS

                --> Error   ┬-> Result with FAILED (if env var was set)
                            ╰-> Raise StageException(...)

    On the context I/O that pass to a stage object at execute process. The
execute method receives a `params={"params": {...}}` value for mapping to
template searching.
"""
from __future__ import annotations

import asyncio
import contextlib
import copy
import inspect
import subprocess
import sys
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import Iterator
from concurrent.futures import (
    FIRST_EXCEPTION,
    Future,
    ThreadPoolExecutor,
    as_completed,
    wait,
)
from datetime import datetime
from inspect import Parameter, isclass, isfunction, ismodule
from pathlib import Path
from subprocess import CompletedProcess
from textwrap import dedent
from threading import Event
from typing import Annotated, Any, Optional, TypeVar, Union, get_type_hints

from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from .__types import DictData, DictStr, TupleStr
from .conf import dynamic
from .exceptions import StageException, UtilException, to_dict
from .result import CANCEL, FAILED, SUCCESS, WAIT, Result, Status
from .reusables import TagFunc, extract_call, not_in_template, param2template
from .utils import (
    delay,
    filter_func,
    gen_id,
    make_exec,
)

T = TypeVar("T")


class BaseStage(BaseModel, ABC):
    """Base Stage Model that keep only id and name fields for the stage
    metadata. If you want to implement any custom stage, you can use this class
    to parent and implement ``self.execute()`` method only.

        This class is the abstraction class for any stage model that want to
    implement to workflow model.
    """

    extras: DictData = Field(
        default_factory=dict,
        description="An extra override config values.",
    )
    id: Optional[str] = Field(
        default=None,
        description=(
            "A stage ID that use to keep execution output or getting by job "
            "owner."
        ),
    )
    name: str = Field(
        description="A stage name that want to logging when start execution.",
    )
    condition: Optional[str] = Field(
        default=None,
        description="A stage condition statement to allow stage executable.",
        alias="if",
    )

    @property
    def iden(self) -> str:
        """Return identity of this stage object that return the id field first.
        If the id does not set, it will use name field instead.

        :rtype: str
        """
        return self.id or self.name

    @model_validator(mode="after")
    def __prepare_running_id(self) -> Self:
        """Prepare stage running ID that use default value of field and this
        method will validate name and id fields should not contain any template
        parameter (exclude matrix template).

        :raise ValueError: When the ID and name fields include matrix parameter
            template with the 'matrix.' string value.

        :rtype: Self
        """

        # VALIDATE: Validate stage id and name should not dynamic with params
        #   template. (allow only matrix)
        if not_in_template(self.id) or not_in_template(self.name):
            raise ValueError(
                "Stage name and ID should only template with 'matrix.'"
            )

        return self

    @abstractmethod
    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute abstraction method that action something by sub-model class.
        This is important method that make this class is able to be the stage.

        :param params: (DictData) A parameter data that want to use in this
            execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        raise NotImplementedError("Stage should implement `execute` method.")

    def handler_execute(
        self,
        params: DictData,
        *,
        run_id: str | None = None,
        parent_run_id: str | None = None,
        result: Result | None = None,
        raise_error: bool | None = None,
        event: Event | None = None,
    ) -> Result | DictData:
        """Handler stage execution result from the stage `execute` method.

            This stage exception handler still use ok-error concept, but it
        allows you force catching an output result with error message by
        specific environment variable,`WORKFLOW_CORE_STAGE_RAISE_ERROR`.

            Execution   --> Ok      --> Result
                                        |-status: SUCCESS
                                        ╰-context:
                                            ╰-outputs: ...

                        --> Error   --> Result (if env var was set)
                                        |-status: FAILED
                                        ╰-errors:
                                            |-class: ...
                                            |-name: ...
                                            ╰-message: ...

                        --> Error   --> Raise StageException(...)

            On the last step, it will set the running ID on a return result object
        from current stage ID before release the final result.

        :param params: (DictData) A parameterize value data that use in this
            stage execution.
        :param run_id: (str) A running stage ID for this execution.
        :param parent_run_id: (str) A parent workflow running ID for this
            execution.
        :param result: (Result) A result object for keeping context and status
            data before execution.
        :param raise_error: (bool) A flag that all this method raise error
        :param event: (Event) An event manager that pass to the stage execution.

        :rtype: Result
        """
        result: Result = Result.construct_with_rs_or_id(
            result,
            run_id=run_id,
            parent_run_id=parent_run_id,
            id_logic=self.iden,
            extras=self.extras,
        )

        try:
            rs: Result = self.execute(params, result=result, event=event)
            return rs
        except Exception as e:
            result.trace.error(f"[STAGE]: {e.__class__.__name__}: {e}")

            if dynamic("stage_raise_error", f=raise_error, extras=self.extras):
                if isinstance(e, StageException):
                    raise

                raise StageException(
                    f"{self.__class__.__name__}: \n\t"
                    f"{e.__class__.__name__}: {e}"
                ) from e

            errors: DictData = {"errors": to_dict(e)}
            return result.catch(status=FAILED, context=errors)

    def set_outputs(self, output: DictData, to: DictData) -> DictData:
        """Set an outputs from execution process to the received context. The
        result from execution will pass to value of `outputs` key.

            For example of setting output method, If you receive execute output
        and want to set on the `to` like;

            ... (i)   output: {'foo': bar}
            ... (ii)  to: {'stages': {}}

            The result of the `to` argument will be;

            ... (iii) to: {
                        'stages': {
                            '<stage-id>': {
                                'outputs': {'foo': 'bar'},
                                'skipped': False,
                            }
                        }
                    }

        Important:
            This method is use for reconstruct the result context and transfer
        to the `to` argument.

        :param output: (DictData) An output data that want to extract to an
            output key.
        :param to: (DictData) A context data that want to add output result.

        :rtype: DictData
        """
        if "stages" not in to:
            to["stages"] = {}

        if self.id is None and not dynamic(
            "stage_default_id", extras=self.extras
        ):
            return to

        _id: str = (
            param2template(self.id, params=to, extras=self.extras)
            if self.id
            else gen_id(
                param2template(self.name, params=to, extras=self.extras)
            )
        )
        output: DictData = output.copy()
        errors: DictData = (
            {"errors": output.pop("errors", {})} if "errors" in output else {}
        )
        skipping: dict[str, bool] = (
            {"skipped": output.pop("skipped", False)}
            if "skipped" in output
            else {}
        )
        to["stages"][_id] = {
            "outputs": copy.deepcopy(output),
            **skipping,
            **errors,
        }
        return to

    def get_outputs(self, outputs: DictData) -> DictData:
        """Get the outputs from stages data. It will get this stage ID from
        the stage outputs mapping.

        :param outputs: (DictData) A stage outputs that want to get by stage ID.

        :rtype: DictData
        """
        if self.id is None and not dynamic(
            "stage_default_id", extras=self.extras
        ):
            return {}

        _id: str = (
            param2template(self.id, params=outputs, extras=self.extras)
            if self.id
            else gen_id(
                param2template(self.name, params=outputs, extras=self.extras)
            )
        )
        return outputs.get("stages", {}).get(_id, {}).get("outputs", {})

    def is_skipped(self, params: DictData | None = None) -> bool:
        """Return true if condition of this stage do not correct. This process
        use build-in eval function to execute the if-condition.

        :raise StageException: When it has any error raise from the eval
            condition statement.
        :raise StageException: When return type of the eval condition statement
            does not return with boolean type.

        :param params: (DictData) A parameters that want to pass to condition
            template.

        :rtype: bool
        """
        if self.condition is None:
            return False

        params: DictData = {} if params is None else params

        try:
            # WARNING: The eval build-in function is very dangerous. So, it
            #   should use the `re` module to validate eval-string before
            #   running.
            rs: bool = eval(
                param2template(self.condition, params, extras=self.extras),
                globals() | params,
                {},
            )
            if not isinstance(rs, bool):
                raise TypeError("Return type of condition does not be boolean")
            return not rs
        except Exception as e:
            raise StageException(f"{e.__class__.__name__}: {e}") from e


class BaseAsyncStage(BaseStage):
    """Base Async Stage model."""

    @abstractmethod
    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        raise NotImplementedError(
            "Async Stage should implement `execute` method."
        )

    @abstractmethod
    async def axecute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Async execution method for this Empty stage that only logging out to
        stdout.

        :param params: (DictData) A context data that want to add output result.
            But this stage does not pass any output.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        raise NotImplementedError(
            "Async Stage should implement `axecute` method."
        )

    async def handler_axecute(
        self,
        params: DictData,
        *,
        run_id: str | None = None,
        parent_run_id: str | None = None,
        result: Result | None = None,
        raise_error: bool | None = None,
        event: Event | None = None,
    ) -> Result:
        """Async Handler stage execution result from the stage `execute` method.

        :param params: (DictData) A parameterize value data that use in this
            stage execution.
        :param run_id: (str) A running stage ID for this execution.
        :param parent_run_id: (str) A parent workflow running ID for this
            execution.
        :param result: (Result) A result object for keeping context and status
            data before execution.
        :param raise_error: (bool) A flag that all this method raise error
        :param event: (Event) An event manager that pass to the stage execution.

        :rtype: Result
        """
        result: Result = Result.construct_with_rs_or_id(
            result,
            run_id=run_id,
            parent_run_id=parent_run_id,
            id_logic=self.iden,
            extras=self.extras,
        )

        try:
            rs: Result = await self.axecute(params, result=result, event=event)
            return rs
        except Exception as e:  # pragma: no cov
            await result.trace.aerror(f"[STAGE]: {e.__class__.__name__}: {e}")

            if dynamic("stage_raise_error", f=raise_error, extras=self.extras):
                if isinstance(e, StageException):
                    raise

                raise StageException(
                    f"{self.__class__.__name__}: \n\t"
                    f"{e.__class__.__name__}: {e}"
                ) from None

            errors: DictData = {"errors": to_dict(e)}
            return result.catch(status=FAILED, context=errors)


class EmptyStage(BaseAsyncStage):
    """Empty stage that do nothing (context equal empty stage) and logging the
    name of stage only to stdout.

    Data Validate:
        >>> stage = {
        ...     "name": "Empty stage execution",
        ...     "echo": "Hello World",
        ...     "sleep": 1,
        ... }
    """

    echo: Optional[str] = Field(
        default=None,
        description="A string message that want to show on the stdout.",
    )
    sleep: float = Field(
        default=0,
        description="A second value to sleep before start execution.",
        ge=0,
        lt=1800,
    )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execution method for the Empty stage that do only logging out to
        stdout. This method does not use the `handler_result` decorator because
        it does not get any error from logging function.

            The result context should be empty and do not process anything
        without calling logging function.

        :param params: (DictData) A context data that want to add output result.
            But this stage does not pass any output.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        result: Result = result or Result(
            run_id=gen_id(self.name + (self.id or ""), unique=True),
            extras=self.extras,
        )

        if not self.echo:
            message: str = "..."
        else:
            message: str = param2template(
                dedent(self.echo), params, extras=self.extras
            )
            if "\n" in self.echo:
                message: str = "\n\t" + message.replace("\n", "\n\t").strip(
                    "\n"
                )

        result.trace.info(
            f"[STAGE]: Empty-Execute: {self.name!r}: ( {message} )"
        )
        if self.sleep > 0:
            if self.sleep > 5:
                result.trace.info(f"[STAGE]: ... sleep ({self.sleep} seconds)")
            time.sleep(self.sleep)

        return result.catch(status=SUCCESS)

    async def axecute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Async execution method for this Empty stage that only logging out to
        stdout.

        :param params: (DictData) A context data that want to add output result.
            But this stage does not pass any output.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        await result.trace.ainfo(
            f"[STAGE]: Empty-Execute: {self.name!r}: "
            f"( {param2template(self.echo, params, extras=self.extras) or '...'} )"
        )

        if self.sleep > 0:
            if self.sleep > 5:
                await result.trace.ainfo(
                    f"[STAGE]: ... sleep ({self.sleep} seconds)"
                )
            await asyncio.sleep(self.sleep)

        return result.catch(status=SUCCESS)


class BashStage(BaseStage):
    """Bash execution stage that execute bash script on the current OS.
    If your current OS is Windows, it will run on the bash in the WSL.

        I get some limitation when I run shell statement with the built-in
    subprocess package. It does not good enough to use multiline statement.
    Thus, I add writing ``.sh`` file before execution process for fix this
    issue.

    Data Validate:
        >>> stage = {
        ...     "name": "The Shell stage execution",
        ...     "bash": 'echo "Hello $FOO"',
        ...     "env": {
        ...         "FOO": "BAR",
        ...     },
        ... }
    """

    bash: str = Field(description="A bash statement that want to execute.")
    env: DictStr = Field(
        default_factory=dict,
        description=(
            "An environment variables that set before start execute by adding "
            "on the header of the `.sh` file."
        ),
    )

    @contextlib.contextmanager
    def create_sh_file(
        self, bash: str, env: DictStr, run_id: str | None = None
    ) -> Iterator[TupleStr]:
        """Return context of prepared bash statement that want to execute. This
        step will write the `.sh` file before giving this file name to context.
        After that, it will auto delete this file automatic.

        :param bash: (str) A bash statement that want to execute.
        :param env: (DictStr) An environment variable that use on this bash
            statement.
        :param run_id: (str | None) A running stage ID that use for writing sh
            file instead generate by UUID4.

        :rtype: Iterator[TupleStr]
        """
        run_id: str = run_id or uuid.uuid4()
        f_name: str = f"{run_id}.sh"
        f_shebang: str = "bash" if sys.platform.startswith("win") else "sh"

        with open(f"./{f_name}", mode="w", newline="\n") as f:
            # NOTE: write header of `.sh` file
            f.write(f"#!/bin/{f_shebang}\n\n")

            # NOTE: add setting environment variable before bash skip statement.
            f.writelines([f"{k}='{env[k]}';\n" for k in env])

            # NOTE: make sure that shell script file does not have `\r` char.
            f.write("\n" + bash.replace("\r\n", "\n"))

        # NOTE: Make this .sh file able to executable.
        make_exec(f"./{f_name}")

        yield [f_shebang, f_name]

        # Note: Remove .sh file that use to run bash.
        Path(f"./{f_name}").unlink()

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the Bash statement with the Python build-in ``subprocess``
        package.

        :param params: A parameter data that want to use in this execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        bash: str = param2template(
            dedent(self.bash), params, extras=self.extras
        )

        result.trace.info(f"[STAGE]: Shell-Execute: {self.name}")
        with self.create_sh_file(
            bash=bash,
            env=param2template(self.env, params, extras=self.extras),
            run_id=result.run_id,
        ) as sh:
            result.trace.debug(f"... Create `{sh[1]}` file.")
            rs: CompletedProcess = subprocess.run(
                sh, shell=False, capture_output=True, text=True
            )

        if rs.returncode > 0:
            # NOTE: Prepare stderr message that returning from subprocess.
            e: str = (
                rs.stderr.encode("utf-8").decode("utf-16")
                if "\\x00" in rs.stderr
                else rs.stderr
            ).removesuffix("\n")
            raise StageException(
                f"Subprocess: {e}\nRunning Statement:\n---\n"
                f"```bash\n{bash}\n```"
            )
        return result.catch(
            status=SUCCESS,
            context={
                "return_code": rs.returncode,
                "stdout": None if (out := rs.stdout.strip("\n")) == "" else out,
                "stderr": None if (out := rs.stderr.strip("\n")) == "" else out,
            },
        )


class PyStage(BaseStage):
    """Python executor stage that running the Python statement with receiving
    globals and additional variables.

        This stage allow you to use any Python object that exists on the globals
    such as import your installed package.

    Data Validate:
        >>> stage = {
        ...     "name": "Python stage execution",
        ...     "run": 'print("Hello {x}")',
        ...     "vars": {
        ...         "x": "BAR",
        ...     },
        ... }
    """

    run: str = Field(
        description="A Python string statement that want to run with `exec`.",
    )
    vars: DictData = Field(
        default_factory=dict,
        description=(
            "A variable mapping that want to pass to globals parameter in the "
            "`exec` func."
        ),
    )

    @staticmethod
    def filter_locals(values: DictData) -> Iterator[str]:
        """Filter a locals mapping values that be module, class, or
        __annotations__.

        :param values: (DictData) A locals values that want to filter.

        :rtype: Iterator[str]
        """
        for value in values:

            if (
                value == "__annotations__"
                or (value.startswith("__") and value.endswith("__"))
                or ismodule(values[value])
                or isclass(values[value])
            ):
                continue

            yield value

    def set_outputs(self, output: DictData, to: DictData) -> DictData:
        """Override set an outputs method for the Python execution process that
        extract output from all the locals values.

        :param output: (DictData) An output data that want to extract to an
            output key.
        :param to: (DictData) A context data that want to add output result.

        :rtype: DictData
        """
        output: DictData = output.copy()
        lc: DictData = output.pop("locals", {})
        gb: DictData = output.pop("globals", {})
        super().set_outputs(lc | output, to=to)
        to.update({k: gb[k] for k in to if k in gb})
        return to

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the Python statement that pass all globals and input params
        to globals argument on ``exec`` build-in function.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        lc: DictData = {}
        gb: DictData = (
            globals()
            | param2template(self.vars, params, extras=self.extras)
            | {"result": result}
        )

        result.trace.info(f"[STAGE]: Py-Execute: {self.name}")

        # WARNING: The exec build-in function is very dangerous. So, it
        #   should use the re module to validate exec-string before running.
        exec(
            param2template(dedent(self.run), params, extras=self.extras),
            gb,
            lc,
        )

        return result.catch(
            status=SUCCESS,
            context={
                "locals": {k: lc[k] for k in self.filter_locals(lc)},
                "globals": {
                    k: gb[k]
                    for k in gb
                    if (
                        not k.startswith("__")
                        and k != "annotations"
                        and not ismodule(gb[k])
                        and not isclass(gb[k])
                        and not isfunction(gb[k])
                    )
                },
            },
        )


class CallStage(BaseStage):
    """Call executor that call the Python function from registry with tag
    decorator function in ``utils`` module and run it with input arguments.

        This stage is different with PyStage because the PyStage is just calling
    a Python statement with the ``eval`` and pass that locale before eval that
    statement. So, you can create your function complexly that you can for your
    objective to invoked by this stage object.

        This stage is the usefull stage for run every job by a custom requirement
    that you want by creating the Python function and adding it to the task
    registry by importer syntax like `module.tasks.registry` not path style like
    `module/tasks/registry`.

    Data Validate:
        >>> stage = {
        ...     "name": "Task stage execution",
        ...     "uses": "tasks/function-name@tag-name",
        ...     "args": {"arg01": "BAR", "kwarg01": 10},
        ... }
    """

    uses: str = Field(
        description=(
            "A pointer that want to load function from the call registry."
        ),
    )
    args: DictData = Field(
        default_factory=dict,
        description="An arguments that want to pass to the call function.",
        alias="with",
    )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the Call function that already in the call registry.

        :raise ValueError: When the necessary arguments of call function do not
            set from the input params argument.
        :raise TypeError: When the return type of call function does not be
            dict type.

        :param params: (DictData) A parameter that want to pass before run any
            statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :raise ValueError: If necessary arguments does not pass from the `args`
            field.
        :raise TypeError: If the result from the caller function does not match
            with a `dict` type.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        has_keyword: bool = False
        call_func: TagFunc = extract_call(
            param2template(self.uses, params, extras=self.extras),
            registries=self.extras.get("registry_caller"),
        )()

        # VALIDATE: check input task caller parameters that exists before
        #   calling.
        args: DictData = {"result": result} | param2template(
            self.args, params, extras=self.extras
        )
        ips = inspect.signature(call_func)
        necessary_params: list[str] = []
        for k in ips.parameters:
            if (
                v := ips.parameters[k]
            ).default == Parameter.empty and v.kind not in (
                Parameter.VAR_KEYWORD,
                Parameter.VAR_POSITIONAL,
            ):
                necessary_params.append(k)
            elif v.kind == Parameter.VAR_KEYWORD:
                has_keyword = True

        if any(
            (k.removeprefix("_") not in args and k not in args)
            for k in necessary_params
        ):
            raise ValueError(
                f"Necessary params, ({', '.join(necessary_params)}, ), "
                f"does not set to args, {list(args.keys())}."
            )

        if "result" not in ips.parameters and not has_keyword:
            args.pop("result")

        result.trace.info(
            f"[STAGE]: Call-Execute: {call_func.name}@{call_func.tag}"
        )

        args = self.parse_model_args(call_func, args, result)

        if inspect.iscoroutinefunction(call_func):
            loop = asyncio.get_event_loop()
            rs: DictData = loop.run_until_complete(
                call_func(**param2template(args, params, extras=self.extras))
            )
        else:
            rs: DictData = call_func(
                **param2template(args, params, extras=self.extras)
            )

        # VALIDATE:
        #   Check the result type from call function, it should be dict.
        if isinstance(rs, BaseModel):
            rs: DictData = rs.model_dump(by_alias=True)
        elif not isinstance(rs, dict):
            raise TypeError(
                f"Return type: '{call_func.name}@{call_func.tag}' does not "
                f"serialize to result model, you change return type to `dict`."
            )
        return result.catch(status=SUCCESS, context=rs)

    @staticmethod
    def parse_model_args(
        func: TagFunc,
        args: DictData,
        result: Result,
    ) -> DictData:
        """Parse Pydantic model from any dict data before parsing to target
        caller function.

        :param func: A tag function that want to get typing.
        :param args: An arguments before passing to this tag function.
        :param result: (Result) A result object for keeping context and status
            data.

        :rtype: DictData
        """
        try:
            type_hints: dict[str, Any] = get_type_hints(func)
        except TypeError as e:
            result.trace.warning(
                f"[STAGE]: Get type hint raise TypeError: {e}, so, it skip "
                f"parsing model args process."
            )
            return args

        for arg in type_hints:

            if arg == "return":
                continue

            if arg.removeprefix("_") in args:
                args[arg] = args.pop(arg.removeprefix("_"))

            t: Any = type_hints[arg]

            # NOTE: Check Result argument was passed to this caller function.
            #
            # if is_dataclass(t) and t.__name__ == "Result" and arg not in args:
            #     args[arg] = result

            if issubclass(t, BaseModel) and arg in args:
                args[arg] = t.model_validate(obj=args[arg])

        return args


class TriggerStage(BaseStage):
    """Trigger Workflow execution stage that execute another workflow. This
    the core stage that allow you to create the reusable workflow object or
    dynamic parameters workflow for common usecase.

    Data Validate:
        >>> stage = {
        ...     "name": "Trigger workflow stage execution",
        ...     "trigger": 'workflow-name-for-loader',
        ...     "params": {"run-date": "2024-08-01", "source": "src"},
        ... }
    """

    trigger: str = Field(
        description=(
            "A trigger workflow name that should exist on the config path."
        ),
    )
    params: DictData = Field(
        default_factory=dict,
        description="A parameter that want to pass to workflow execution.",
    )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Trigger another workflow execution. It will wait the trigger
        workflow running complete before catching its result.

        :param params: A parameter data that want to use in this execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        from .exceptions import WorkflowException
        from .workflow import Workflow

        if result is None:
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        _trigger: str = param2template(self.trigger, params, extras=self.extras)
        result.trace.info(f"[STAGE]: Trigger-Execute: {_trigger!r}")
        try:
            rs: Result = Workflow.from_conf(
                name=_trigger,
                extras=self.extras | {"stage_raise_error": True},
            ).execute(
                params=param2template(self.params, params, extras=self.extras),
                parent_run_id=result.run_id,
                event=event,
            )
        except WorkflowException as e:
            raise StageException("Trigger workflow stage was failed") from e

        if rs.status == FAILED:
            err_msg: str | None = (
                f" with:\n{msg}"
                if (msg := rs.context.get("errors", {}).get("message"))
                else ""
            )
            raise StageException(f"Trigger workflow was failed{err_msg}.")
        return rs


class ParallelStage(BaseStage):  # pragma: no cov
    """Parallel execution stage that execute child stages with parallel.

        This stage is not the low-level stage model because it runs muti-stages
    in this stage execution.

    Data Validate:
        >>> stage = {
        ...     "name": "Parallel stage execution.",
        ...     "parallel": {
        ...         "branch01": [
        ...             {
        ...                 "name": "Echo first stage",
        ...                 "echo": "Start run with branch 1",
        ...                 "sleep": 3,
        ...             },
        ...         ],
        ...         "branch02": [
        ...             {
        ...                 "name": "Echo second stage",
        ...                 "echo": "Start run with branch 2",
        ...                 "sleep": 1,
        ...             },
        ...         ],
        ...     }
        ... }
    """

    parallel: dict[str, list[Stage]] = Field(
        description="A mapping of parallel branch name and stages.",
    )
    max_workers: int = Field(
        default=2,
        ge=1,
        lt=20,
        description=(
            "The maximum thread pool worker size for execution parallel."
        ),
        alias="max-workers",
    )

    def execute_task(
        self,
        branch: str,
        params: DictData,
        result: Result,
        *,
        event: Event | None = None,
        extras: DictData | None = None,
    ) -> DictData:
        """Task execution method for passing a branch to each thread.

        :param branch: A branch ID.
        :param params: A parameter data that want to use in this execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.
        :param extras: (DictData) An extra parameters that want to override
            config values.

        :rtype: DictData
        """
        result.trace.debug(f"... Execute branch: {branch!r}")
        context: DictData = copy.deepcopy(params)
        context.update({"branch": branch})
        output: DictData = {"branch": branch, "stages": {}}
        for stage in self.parallel[branch]:

            if extras:
                stage.extras = extras

            if stage.is_skipped(params=context):
                result.trace.info(f"... Skip stage: {stage.iden!r}")
                stage.set_outputs(output={"skipped": True}, to=output)
                continue

            if event and event.is_set():
                error_msg: str = (
                    "Branch-Stage was canceled from event that had set before "
                    "stage item execution."
                )
                return result.catch(
                    status=CANCEL,
                    parallel={
                        branch: {
                            "branch": branch,
                            "stages": filter_func(output.pop("stages", {})),
                            "errors": StageException(error_msg).to_dict(),
                        }
                    },
                )

            try:
                rs: Result = stage.handler_execute(
                    params=context,
                    run_id=result.run_id,
                    parent_run_id=result.parent_run_id,
                    raise_error=True,
                    event=event,
                )
                stage.set_outputs(rs.context, to=output)
                stage.set_outputs(stage.get_outputs(output), to=context)
            except (StageException, UtilException) as e:  # pragma: no cov
                result.trace.error(f"[STAGE]: {e.__class__.__name__}: {e}")
                raise StageException(
                    f"Sub-Stage execution error: {e.__class__.__name__}: {e}"
                ) from None

            if rs.status == FAILED:
                error_msg: str = (
                    f"Item-Stage was break because it has a sub stage, "
                    f"{stage.iden}, failed without raise error."
                )
                return result.catch(
                    status=FAILED,
                    parallel={
                        branch: {
                            "branch": branch,
                            "stages": filter_func(output.pop("stages", {})),
                            "errors": StageException(error_msg).to_dict(),
                        },
                    },
                )

        return result.catch(
            status=SUCCESS,
            parallel={
                branch: {
                    "branch": branch,
                    "stages": filter_func(output.pop("stages", {})),
                },
            },
        )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the stages that parallel each branch via multi-threading mode
        or async mode by changing `async_mode` flag.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )
        event: Event = Event() if event is None else event
        result.trace.info(
            f"[STAGE]: Parallel-Execute: {self.max_workers} workers."
        )
        result.catch(status=WAIT, context={"parallel": {}})
        with ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="parallel_stage_exec_",
        ) as executor:

            context: DictData = {}
            status: Status = SUCCESS

            futures: list[Future] = (
                executor.submit(
                    self.execute_task,
                    branch=branch,
                    params=params,
                    result=result,
                    event=event,
                    extras=self.extras,
                )
                for branch in self.parallel
            )

            done = as_completed(futures, timeout=1800)
            for future in done:
                try:
                    future.result()
                except StageException as e:
                    status = FAILED
                    result.trace.error(
                        f"[STAGE]: {e.__class__.__name__}:\n\t{e}"
                    )
                    context.update({"errors": e.to_dict()})

        return result.catch(status=status, context=context)


class ForEachStage(BaseStage):
    """For-Each execution stage that execute child stages with an item in list
    of item values. This stage is not the low-level stage model because it runs
    muti-stages in this stage execution.

        The concept of this stage use the same logic of the Job execution.

    Data Validate:
        >>> stage = {
        ...     "name": "For-each stage execution",
        ...     "foreach": [1, 2, 3]
        ...     "stages": [
        ...         {
        ...             "name": "Echo stage",
        ...             "echo": "Start run with item {{ item }}"
        ...         },
        ...     ],
        ... }
    """

    foreach: Union[list[str], list[int], str] = Field(
        description=(
            "A items for passing to each stages via ${{ item }} template."
        ),
    )
    stages: list[Stage] = Field(
        default_factory=list,
        description=(
            "A list of stage that will run with each item in the foreach field."
        ),
    )
    concurrent: int = Field(
        default=1,
        ge=1,
        lt=10,
        description=(
            "A concurrent value allow to run each item at the same time. It "
            "will be sequential mode if this value equal 1."
        ),
    )

    def execute_item(
        self,
        item: Union[str, int],
        params: DictData,
        result: Result,
        *,
        event: Event | None = None,
    ) -> Result:
        """Execute foreach item from list of item.

        :param item: (str | int) An item that want to execution.
        :param params: (DictData) A parameter that want to pass to stage
            execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :raise StageException: If the stage execution raise errors.

        :rtype: Result
        """
        result.trace.debug(f"[STAGE]: Execute item: {item!r}")
        context: DictData = copy.deepcopy(params)
        context.update({"item": item})
        output: DictData = {"item": item, "stages": {}}
        for stage in self.stages:

            if self.extras:
                stage.extras = self.extras

            if stage.is_skipped(params=context):
                result.trace.info(f"... Skip stage: {stage.iden!r}")
                stage.set_outputs(output={"skipped": True}, to=output)
                continue

            if event and event.is_set():  # pragma: no cov
                error_msg: str = (
                    "Item-Stage was canceled from event that had set before "
                    "stage item execution."
                )
                return result.catch(
                    status=CANCEL,
                    foreach={
                        item: {
                            "item": item,
                            "stages": filter_func(output.pop("stages", {})),
                            "errors": StageException(error_msg).to_dict(),
                        }
                    },
                )

            try:
                rs: Result = stage.handler_execute(
                    params=context,
                    run_id=result.run_id,
                    parent_run_id=result.parent_run_id,
                    raise_error=True,
                    event=event,
                )
                stage.set_outputs(rs.context, to=output)
                stage.set_outputs(stage.get_outputs(output), to=context)
            except (StageException, UtilException) as e:
                result.trace.error(f"[STAGE]: {e.__class__.__name__}: {e}")
                raise StageException(
                    f"Sub-Stage execution error: {e.__class__.__name__}: {e}"
                ) from None

            if rs.status == FAILED:
                error_msg: str = (
                    f"Item-Stage was break because it has a sub stage, "
                    f"{stage.iden}, failed without raise error."
                )
                return result.catch(
                    status=FAILED,
                    foreach={
                        item: {
                            "item": item,
                            "stages": filter_func(output.pop("stages", {})),
                            "errors": StageException(error_msg).to_dict(),
                        },
                    },
                )
        return result.catch(
            status=SUCCESS,
            foreach={
                item: {
                    "item": item,
                    "stages": filter_func(output.pop("stages", {})),
                },
            },
        )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the stages that pass each item form the foreach field.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )
        event: Event = Event() if event is None else event
        foreach: Union[list[str], list[int]] = (
            param2template(self.foreach, params, extras=self.extras)
            if isinstance(self.foreach, str)
            else self.foreach
        )
        if not isinstance(foreach, list):
            raise StageException(
                f"Foreach does not support foreach value: {foreach!r}"
            )

        result.trace.info(f"[STAGE]: Foreach-Execute: {foreach!r}.")
        result.catch(status=WAIT, context={"items": foreach, "foreach": {}})
        if event and event.is_set():  # pragma: no cov
            return result.catch(
                status=CANCEL,
                context={
                    "errors": StageException(
                        "Stage was canceled from event that had set "
                        "before stage foreach execution."
                    ).to_dict()
                },
            )

        with ThreadPoolExecutor(
            max_workers=self.concurrent, thread_name_prefix="stage_foreach_"
        ) as executor:

            futures: list[Future] = [
                executor.submit(
                    self.execute_item,
                    item=item,
                    params=params,
                    result=result,
                    event=event,
                )
                for item in foreach
            ]
            context: DictData = {}
            status: Status = SUCCESS

            done, not_done = wait(
                futures, timeout=1800, return_when=FIRST_EXCEPTION
            )

            if len(done) != len(futures):
                result.trace.warning(
                    "[STAGE]: Set the event for stop running stage."
                )
                event.set()
                for future in not_done:
                    future.cancel()

            for future in done:
                try:
                    future.result()
                except StageException as e:
                    status = FAILED
                    result.trace.error(
                        f"[STAGE]: {e.__class__.__name__}:\n\t{e}"
                    )
                    context.update({"errors": e.to_dict()})

        return result.catch(status=status, context=context)


class UntilStage(BaseStage):  # pragma: no cov
    """Until execution stage.

    Data Validate:
        >>> stage = {
        ...     "name": "Until stage execution",
        ...     "item": 1,
        ...     "until": "${{ item }} > 3"
        ...     "stages": [
        ...         {
        ...             "name": "Start increase item value.",
        ...             "run": "item = ${{ item }}\\nitem += 1\\n"
        ...         },
        ...     ],
        ... }
    """

    item: Union[str, int, bool] = Field(
        default=0,
        description=(
            "An initial value that can be any value in str, int, or bool type."
        ),
    )
    until: str = Field(description="A until condition.")
    stages: list[Stage] = Field(
        default_factory=list,
        description=(
            "A list of stage that will run with each item until condition "
            "correct."
        ),
    )
    max_loop: int = Field(
        default=10,
        ge=1,
        lt=100,
        description="The maximum value of loop for this until stage.",
        alias="max-loop",
    )

    def execute_item(
        self,
        item: T,
        loop: int,
        params: DictData,
        result: Result,
        event: Event | None = None,
    ) -> tuple[Result, T]:
        """Execute until item set item by some stage or by default loop
        variable.

        :param item: (T) An item that want to execution.
        :param loop: (int) A number of loop.
        :param params: (DictData) A parameter that want to pass to stage
            execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: tuple[Result, T]
        """
        result.trace.debug(f"... Execute until item: {item!r}")
        context: DictData = copy.deepcopy(params)
        context.update({"item": item})
        output: DictData = {"loop": loop, "item": item, "stages": {}}
        next_item: T = None
        for stage in self.stages:

            if self.extras:
                stage.extras = self.extras

            if stage.is_skipped(params=context):
                result.trace.info(f"... Skip stage: {stage.iden!r}")
                stage.set_outputs(output={"skipped": True}, to=output)
                continue

            if event and event.is_set():
                error_msg: str = (
                    "Item-Stage was canceled from event that had set before "
                    "stage item execution."
                )
                return (
                    result.catch(
                        status=CANCEL,
                        until={
                            loop: {
                                "loop": loop,
                                "item": item,
                                "stages": filter_func(output.pop("stages", {})),
                                "errors": StageException(error_msg).to_dict(),
                            }
                        },
                    ),
                    next_item,
                )

            try:
                rs: Result = stage.handler_execute(
                    params=context,
                    run_id=result.run_id,
                    parent_run_id=result.parent_run_id,
                    raise_error=True,
                    event=event,
                )
                stage.set_outputs(rs.context, to=output)

                if "item" in (_output := stage.get_outputs(output)):
                    next_item = _output["item"]

                stage.set_outputs(_output, to=context)
            except (StageException, UtilException) as e:
                result.trace.error(f"[STAGE]: {e.__class__.__name__}: {e}")
                raise StageException(
                    f"Sub-Stage execution error: {e.__class__.__name__}: {e}"
                ) from None

        return (
            result.catch(
                status=SUCCESS,
                until={
                    loop: {
                        "loop": loop,
                        "item": item,
                        "stages": filter_func(output.pop("stages", {})),
                    }
                },
            ),
            next_item,
        )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the stages that pass item from until condition field and
        setter step.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True)
            )

        result.trace.info(f"[STAGE]: Until-Execution: {self.until}")
        item: Union[str, int, bool] = param2template(
            self.item, params, extras=self.extras
        )
        loop: int = 1
        track: bool = True
        exceed_loop: bool = False
        result.catch(status=WAIT, context={"until": {}})
        while track and not (exceed_loop := loop >= self.max_loop):

            if event and event.is_set():
                return result.catch(
                    status=CANCEL,
                    context={
                        "errors": StageException(
                            "Stage was canceled from event that had set "
                            "before stage until execution."
                        ).to_dict()
                    },
                )

            result, item = self.execute_item(
                item=item,
                loop=loop,
                params=params,
                result=result,
                event=event,
            )

            loop += 1
            if item is None:
                result.trace.warning(
                    "... Does not have set item stage. It will use loop by "
                    "default."
                )
                item = loop

            next_track: bool = eval(
                param2template(
                    self.until,
                    params | {"item": item, "loop": loop},
                    extras=self.extras,
                ),
                globals() | params | {"item": item},
                {},
            )
            if not isinstance(next_track, bool):
                raise StageException(
                    "Return type of until condition does not be boolean, it"
                    f"return: {next_track!r}"
                )
            track: bool = not next_track
            delay(0.025)

        if exceed_loop:
            raise StageException(
                f"The until loop was exceed {self.max_loop} loops"
            )
        return result.catch(status=SUCCESS)


class Match(BaseModel):
    """Match model for the Case Stage."""

    case: Union[str, int] = Field(description="A match case.")
    stages: list[Stage] = Field(
        description="A list of stage to execution for this case."
    )


class CaseStage(BaseStage):
    """Case execution stage.

    Data Validate:
        >>> stage = {
        ...     "name": "If stage execution.",
        ...     "case": "${{ param.test }}",
        ...     "match": [
        ...         {
        ...             "case": "1",
        ...             "stages": [
        ...                 {
        ...                     "name": "Stage case 1",
        ...                     "eche": "Hello case 1",
        ...                 },
        ...             ],
        ...         },
        ...         {
        ...             "case": "_",
        ...             "stages": [
        ...                 {
        ...                     "name": "Stage else",
        ...                     "eche": "Hello case else",
        ...                 },
        ...             ],
        ...         },
        ...     ],
        ... }

    """

    case: str = Field(description="A case condition for routing.")
    match: list[Match] = Field(
        description="A list of Match model that should not be an empty list.",
    )
    skip_not_match: bool = Field(
        default=False,
        description=(
            "A flag for making skip if it does not match and else condition "
            "does not set too."
        ),
        alias="skip-not-match",
    )

    def execute_case(
        self,
        case: str,
        stages: list[Stage],
        params: DictData,
        result: Result,
        *,
        event: Event | None = None,
    ) -> Result:
        """Execute case.

        :param case: (str) A case that want to execution.
        :param stages: (list[Stage]) A list of stage.
        :param params: (DictData) A parameter that want to pass to stage
            execution.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        context: DictData = copy.deepcopy(params)
        context.update({"case": case})
        output: DictData = {"case": case, "stages": {}}

        for stage in stages:

            if self.extras:
                stage.extras = self.extras

            if stage.is_skipped(params=context):
                result.trace.info(f"... Skip stage: {stage.iden!r}")
                stage.set_outputs(output={"skipped": True}, to=output)
                continue

            if event and event.is_set():  # pragma: no cov
                error_msg: str = (
                    "Case-Stage was canceled from event that had set before "
                    "stage case execution."
                )
                return result.catch(
                    status=CANCEL,
                    context={
                        "case": case,
                        "stages": filter_func(output.pop("stages", {})),
                        "errors": StageException(error_msg).to_dict(),
                    },
                )

            try:
                rs: Result = stage.handler_execute(
                    params=context,
                    run_id=result.run_id,
                    parent_run_id=result.parent_run_id,
                    raise_error=True,
                    event=event,
                )
                stage.set_outputs(rs.context, to=output)
                stage.set_outputs(stage.get_outputs(output), to=context)
            except (StageException, UtilException) as e:  # pragma: no cov
                result.trace.error(f"[STAGE]: {e.__class__.__name__}: {e}")
                return result.catch(
                    status=FAILED,
                    context={
                        "case": case,
                        "stages": filter_func(output.pop("stages", {})),
                        "errors": e.to_dict(),
                    },
                )

            if rs.status == FAILED:
                error_msg: str = (
                    f"Case-Stage was break because it has a sub stage, "
                    f"{stage.iden}, failed without raise error."
                )
                return result.catch(
                    status=FAILED,
                    context={
                        "case": case,
                        "stages": filter_func(output.pop("stages", {})),
                        "errors": StageException(error_msg).to_dict(),
                    },
                )
        return result.catch(
            status=SUCCESS,
            context={
                "case": case,
                "stages": filter_func(output.pop("stages", {})),
            },
        )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute case-match condition that pass to the case field.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )

        _case: Optional[str] = param2template(
            self.case, params, extras=self.extras
        )

        result.trace.info(f"[STAGE]: Case-Execute: {_case!r}.")
        _else: Optional[Match] = None
        stages: Optional[list[Stage]] = None
        for match in self.match:
            if (c := match.case) == "_":
                _else: Match = match
                continue

            _condition: str = param2template(c, params, extras=self.extras)
            if stages is None and _case == _condition:
                stages: list[Stage] = match.stages

        if stages is None:
            if _else is None:
                if not self.skip_not_match:
                    raise StageException(
                        "This stage does not set else for support not match "
                        "any case."
                    )
                result.trace.info(
                    "... Skip this stage because it does not match."
                )
                error_msg: str = (
                    "Case-Stage was canceled because it does not match any "
                    "case and else condition does not set too."
                )
                return result.catch(
                    status=CANCEL,
                    context={"errors": StageException(error_msg).to_dict()},
                )
            _case: str = "_"
            stages: list[Stage] = _else.stages

        if event and event.is_set():  # pragma: no cov
            return result.catch(
                status=CANCEL,
                context={
                    "errors": StageException(
                        "Stage was canceled from event that had set before "
                        "case-stage execution."
                    ).to_dict()
                },
            )

        return self.execute_case(
            case=_case, stages=stages, params=params, result=result, event=event
        )


class RaiseStage(BaseStage):  # pragma: no cov
    """Raise error stage execution that raise StageException that use a message
    field for making error message before raise.

    Data Validate:
        >>> stage = {
        ...     "name": "Raise stage",
        ...     "raise": "raise this stage",
        ... }

    """

    message: str = Field(
        description=(
            "An error message that want to raise with StageException class"
        ),
        alias="raise",
    )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Raise the StageException object with the message field execution.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True),
                extras=self.extras,
            )
        message: str = param2template(self.message, params, extras=self.extras)
        result.trace.info(f"[STAGE]: Raise-Execute: {message!r}.")
        raise StageException(message)


# TODO: Not implement this stages yet
class HookStage(BaseStage):  # pragma: no cov
    """Hook stage execution."""

    hook: str
    args: DictData = Field(default_factory=dict)
    callback: str

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        raise NotImplementedError("Hook Stage does not implement yet.")


# TODO: Not implement this stages yet
class DockerStage(BaseStage):  # pragma: no cov
    """Docker container stage execution.

    Data Validate:
        >>> stage = {
        ...     "name": "Docker stage execution",
        ...     "image": "image-name.pkg.com",
        ...     "env": {
        ...         "ENV": "dev",
        ...         "DEBUG": "true",
        ...     },
        ...     "volume": {
        ...         "secrets": "/secrets",
        ...     },
        ...     "auth": {
        ...         "username": "__json_key",
        ...         "password": "${GOOGLE_CREDENTIAL_JSON_STRING}",
        ...     },
        ... }
    """

    image: str = Field(
        description="A Docker image url with tag that want to run.",
    )
    tag: str = Field(default="latest", description="An Docker image tag.")
    env: DictData = Field(default_factory=dict)
    volume: DictData = Field(default_factory=dict)
    auth: DictData = Field(
        default_factory=dict,
        description=(
            "An authentication of the Docker registry that use in pulling step."
        ),
    )

    def execute_task(
        self,
        params: DictData,
        result: Result,
    ):
        from docker import DockerClient
        from docker.errors import ContainerError

        client = DockerClient(
            base_url="unix://var/run/docker.sock", version="auto"
        )

        resp = client.api.pull(
            repository=f"{self.image}",
            tag=self.tag,
            auth_config=param2template(self.auth, params, extras=self.extras),
            stream=True,
            decode=True,
        )
        for line in resp:
            result.trace.info(f"... {line}")

        unique_image_name: str = f"{self.image}_{datetime.now():%Y%m%d%H%M%S%f}"
        container = client.containers.run(
            image=f"{self.image}:{self.tag}",
            name=unique_image_name,
            environment=self.env,
            volumes=(
                {
                    Path.cwd()
                    / f".docker.{result.run_id}.logs": {
                        "bind": "/logs",
                        "mode": "rw",
                    },
                }
                | {
                    Path.cwd() / source: {"bind": target, "mode": "rw"}
                    for source, target in (
                        volume.split(":", maxsplit=1) for volume in self.volume
                    )
                }
            ),
            detach=True,
        )

        for line in container.logs(stream=True, timestamps=True):
            result.trace.info(f"... {line.strip().decode()}")

        # NOTE: This code copy from the docker package.
        exit_status: int = container.wait()["StatusCode"]
        if exit_status != 0:
            out = container.logs(stdout=False, stderr=True)
            container.remove()
            raise ContainerError(
                container,
                exit_status,
                None,
                f"{self.image}:{self.tag}",
                out,
            )

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        raise NotImplementedError("Docker Stage does not implement yet.")


# TODO: Not implement this stages yet
class VirtualPyStage(PyStage):  # pragma: no cov
    """Python Virtual Environment stage execution."""

    deps: list[str] = Field(
        description=(
            "list of Python dependency that want to install before execution "
            "stage."
        ),
    )

    def create_py_file(self, py: str, run_id: str | None): ...

    def execute(
        self,
        params: DictData,
        *,
        result: Result | None = None,
        event: Event | None = None,
    ) -> Result:
        """Execute the Python statement via Python virtual environment.

        Steps:
            - Create python file.
            - Create `.venv` and install necessary Python deps.
            - Execution python file with uv and specific `.venv`.

        :param params: A parameter that want to pass before run any statement.
        :param result: (Result) A result object for keeping context and status
            data.
        :param event: (Event) An event manager that use to track parent execute
            was not force stopped.

        :rtype: Result
        """
        if result is None:  # pragma: no cov
            result: Result = Result(
                run_id=gen_id(self.name + (self.id or ""), unique=True)
            )

        result.trace.info(f"[STAGE]: Py-Virtual-Execute: {self.name}")
        raise NotImplementedError(
            "Python Virtual Stage does not implement yet."
        )


# NOTE:
#   An order of parsing stage model on the Job model with ``stages`` field.
#   From the current build-in stages, they do not have stage that have the same
#   fields that because of parsing on the Job's stages key.
#
Stage = Annotated[
    Union[
        DockerStage,
        BashStage,
        CallStage,
        HookStage,
        TriggerStage,
        ForEachStage,
        UntilStage,
        ParallelStage,
        CaseStage,
        VirtualPyStage,
        PyStage,
        RaiseStage,
        EmptyStage,
    ],
    Field(union_mode="smart"),
]
