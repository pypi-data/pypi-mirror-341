import pathlib
import re

from gadutils import urls

from gadopenapiconverter import const
from gadopenapiconverter.os import HTTP
from gadopenapiconverter.os import File


def sortimports(lines: list[str]) -> str:
    imports, code = [], []
    for line in lines:
        (imports if re.match(const.REGEXP_IMPORT, line) else code).append(line)
    return const.SYMBOL_EMPTY.join(sorted(imports) + code)


def getcontent(workdir: pathlib.Path, content: str) -> str:
    if content.startswith(const.SYNTAX_FILE):
        path = pathlib.Path(content[len(const.SYNTAX_FILE) :].strip())

        if not path.is_absolute():
            path = workdir / path

        if path.exists() and path.is_file():
            return File.read(path)
    elif urls.checkurl(content):
        return HTTP.download(content)
    else:
        return content
