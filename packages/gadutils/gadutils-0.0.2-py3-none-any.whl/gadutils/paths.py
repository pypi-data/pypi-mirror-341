import pathlib
import typing

from gadutils import const


def current() -> pathlib.Path:
    return pathlib.Path.cwd()


def define(path: typing.Union[str, pathlib.Path, None] = None) -> pathlib.Path:
    if not path:
        return current()
    elif path.startswith(const.SYMBOL_FORWARD_SLASH):
        return pathlib.Path(path)
    else:
        return current() / path
