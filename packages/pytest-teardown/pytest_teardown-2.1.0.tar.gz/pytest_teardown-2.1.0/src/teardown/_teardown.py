import ast
import inspect
import logging
import re
import traceback
from contextlib import suppress
from functools import cached_property
from typing import Any, Callable, Optional

from _pytest.scope import Scope
from simple_singleton import Singleton, SingletonArgs
from simple_singleton.singleton_args import T

_logger = logging.getLogger("pytest-teardown")


class TeardownSingleton(SingletonArgs):
    def __call__(cls: T, *args, **kwargs) -> T:
        cls.current_instance = super().__call__(*args, **kwargs)
        return cls.current_instance


class TeardownStep:
    __lambda_regex = re.compile(r"add\w*\(lambda:(.*)\)")

    def __init__(self, fn: Callable[..., Any], ignore_errors: Optional[bool] = False):
        """An instance of the TeardownStep class represents the action to be performed during the teardown stage.
        fn - Callable object representing a function to execute. Can be lambda;
        ignore_errors - Flag to ignore errors when executing fn.
        """
        self.fn = fn
        self.ignore_errors = ignore_errors

    def __call__(self) -> Any:
        """Calling a TeardownStep object calls a stored function."""
        return self.fn()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.name}>"

    @cached_property
    def name(self) -> str:
        if "lambda" in self.fn.__name__:
            source, _ = inspect.getsourcelines(self.fn)
            oneliner = str("".join([line.strip() for line in source]))
            return self.__get_lambda_code_ast(oneliner) or self.__get_lambda_code_regex(oneliner) or oneliner
        return f"{self.fn.__name__}()"

    @staticmethod
    def __get_lambda_code_ast(source_oneliner: str) -> Optional[str]:
        with suppress(Exception):
            source_ast = ast.parse(source_oneliner)
            lambda_node = next((node for node in ast.walk(source_ast) if isinstance(node, ast.Lambda)), None)
            return source_oneliner[lambda_node.col_offset + 7:lambda_node.end_col_offset].strip()

    @classmethod
    def __get_lambda_code_regex(cls, source_oneliner: str) -> str:
        with suppress(AttributeError):
            return cls.__lambda_regex.search(source_oneliner).group(1).strip()


class Teardown(metaclass=TeardownSingleton):
    def __init__(self, name: str = "default") -> None:
        self._name = name
        self._steps: dict[Scope, list[TeardownStep]] = {scope: [] for scope in Scope}

    def execute(self, scope: Scope) -> None:
        """Executing teardown of a given scope."""
        if not self._steps[scope]:
            _logger.info("No %s teardown (%s)", scope.value, self._name)
            return
        _logger.info("Executing %s teardown (%s)...", scope.value, self._name)
        exceptions: list[str] = []
        for call in reversed(self._steps[scope]):
            try:
                _logger.info(f"Executing `%s`...", call.name)
                call()
                _logger.info(f"`%s` executed successfully!", call.name)
            except Exception as e:
                _logger.info(f"Execution of `%s` failed!{' Ignoring...' if call.ignore_errors else ''}", call.name)
                if not call.ignore_errors:
                    number = len(exceptions) + 1
                    _logger.exception(
                        f"Exception #%s occurred during `%s` execution in %s teardown (%s):",
                        str(number), call.name, scope.value, self._name,
                    )
                    last_traceback = "\n".join(traceback.format_exception(e)[-2:])
                    sep_length = len(max(last_traceback.split("\n"), key=len))
                    exception = f"{number}.\n{last_traceback}\n{sep_length * '='}"
                    exceptions.append(exception)
        self._steps[scope] = []
        if exceptions:
            exceptions_str = "\n".join(exceptions)
            raise Exception(
                f"Errors occurred during {scope.value} teardown execution:\n{exceptions_str}"
            )

    def add(self, fn: Callable[..., Any], ignore_errors: bool = False, scope: Scope = Scope.Function):
        """Add a function call to a teardown of the given scope. Scope is function by default."""
        if not callable(fn):
            raise TypeError(f"`fn` argument passed for a teardown must be callable! Got {fn=} of type {type(fn)}")
        self._steps[scope].append(TeardownStep(fn, ignore_errors))

    def add_session(self, fn: Callable[..., Any], ignore_errors: bool = False):
        """Add a function call to session teardown."""
        self.add(fn, ignore_errors, Scope.Session)

    def add_package(self, fn: Callable[..., Any], ignore_errors: bool = False):
        """Add a function call to package teardown."""
        self.add(fn, ignore_errors, Scope.Package)

    def add_module(self, fn: Callable[..., Any], ignore_errors: bool = False):
        """Add a function call to module teardown."""
        self.add(fn, ignore_errors, Scope.Module)

    def add_class(self, fn: Callable[..., Any], ignore_errors: bool = False):
        """Add a function call to class teardown."""
        self.add(fn, ignore_errors, Scope.Class)
