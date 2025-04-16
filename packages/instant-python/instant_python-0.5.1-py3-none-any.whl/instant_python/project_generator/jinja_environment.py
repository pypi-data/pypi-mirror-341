from jinja2 import Environment, Template, PackageLoader

from instant_python.project_generator.jinja_custom_filters import (
    is_in,
    compute_base_path,
)


class JinjaEnvironment:
    def __init__(self) -> None:
        self._env = Environment(
            loader=PackageLoader("instant_python", "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._env.filters["is_in"] = is_in
        self._env.filters["compute_base_path"] = compute_base_path

    def get_template(self, name: str) -> Template:
        return self._env.get_template(name)
