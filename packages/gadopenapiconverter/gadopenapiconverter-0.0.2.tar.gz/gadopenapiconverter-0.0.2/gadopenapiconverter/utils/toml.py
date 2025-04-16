import pathlib

import tomli
from gadutils import temp
from gadutils import urls

from gadopenapiconverter import const
from gadopenapiconverter.os import HTTP


def todict(content: str) -> dict:
    return tomli.loads(content)


def getconfig(file: str) -> tuple[pathlib.Path, bool]:
    if urls.checkurl(file):
        return temp.getfile(HTTP.download(file), extension=const.EXTENSION_TOML), True
    else:
        return pathlib.Path(file), False
