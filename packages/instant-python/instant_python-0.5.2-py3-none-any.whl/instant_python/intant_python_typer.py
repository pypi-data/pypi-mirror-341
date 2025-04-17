import sys
from collections.abc import Callable

import typer

ExceptionType = type[Exception]
ErrorHandlingCallback = Callable[[Exception], None]


class InstantPythonTyper(typer.Typer):
    error_handlers: dict[ExceptionType, ErrorHandlingCallback] = {}

    def error_handler(self, exc: ExceptionType):
        """Registers a callback function to be called when 'exc' (the given exception) is raised."""

        def decorator(func: ErrorHandlingCallback):
            self.error_handlers[exc] = func
            return func

        return decorator

    def __call__(self, *args, **kwargs):
        """Overrides Typer.__call__ so that when we run the CLI,
        we can catch any exception that's raised and see if there's
        a matching error handler for it.
        """
        try:
            super().__call__(*args, **kwargs)
        except Exception as error:
            for registered_exc_type, handler in self.error_handlers.items():
                if isinstance(error, registered_exc_type):
                    handler(error)
                    sys.exit(1)
            raise