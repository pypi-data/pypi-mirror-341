from pathlib import Path

from instant_python.errors.application_error import ApplicationError
from instant_python.errors.error_types import ErrorTypes


class TemplateFileNotFoundError(ApplicationError):
    def __init__(self, template_path: str | Path) -> None:
        self._message = f"Could not find YAML file at: {template_path}"
        super().__init__(self._message)

    @property
    def type(self) -> str:
        return ErrorTypes.GENERATOR.value

    @property
    def message(self) -> str:
        return self._message
