import pathlib

from gadopenapiconverter import const


class File:
    @classmethod
    def create(cls, path: pathlib.Path) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()

    @classmethod
    def write(cls, path: pathlib.Path, content: str, mode: str = const.FILE_WRITE) -> None:
        cls.create(path)
        with path.open(mode=mode, encoding=const.FILE_ENCODING) as f:
            f.write(const.SYMBOL_NEWLINE + content if mode == const.FILE_APPEND else content)

    @classmethod
    def read(cls, path: pathlib.Path, tolist: bool = False, mode: str = const.FILE_READ) -> str | list[str]:
        with path.open(mode=mode, encoding=const.FILE_ENCODING) as f:
            return f.readlines() if tolist else f.read()
