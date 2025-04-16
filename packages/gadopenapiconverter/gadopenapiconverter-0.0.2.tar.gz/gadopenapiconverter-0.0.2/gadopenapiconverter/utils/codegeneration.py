from gadopenapiconverter import const
from gadopenapiconverter import enums
from gadopenapiconverter import models


def settyping(string: str) -> str:
    return f"typing.{string}"


def setstring(string: str) -> str:
    return f"'{string}'"


def setdefault(string: str, default: str) -> str:
    return f"{string} = {setstring(default)}"


def setempty(string: str) -> str:
    return f"{string} = None"


def setfstring(string: str) -> str:
    return f"f'{string}'"


def makeannotation(field: models.Field) -> str:
    annotation = const.SYMBOL_COMMA.join(field.python + field.datamodels)

    if field.wrappers:
        for wrapper in field.wrappers:
            annotation = settyping(wrapper.wrapp(annotation))

    if field.default:
        return setdefault(annotation, field.default)
    elif not field.required:
        return setempty(annotation)

    return annotation


def makearguments(arguments: list[tuple[str, models.Field]]) -> str:
    string = "self"

    if not arguments:
        return string

    for argument in arguments:
        for key, value in argument:
            string += f"{const.SYMBOL_COMMA}{const.SYMBOL_WHITESPACE}{key}: {makeannotation(value)}"

    return string


def makeserialize(
    client: enums.PythonModule,
    model: enums.PythonModule,
    response: enums.PythonType | str,
    array: bool,
) -> str | None:
    if not response:
        return

    if client in [enums.PythonModule.requests, enums.PythonModule.httpx]:
        handler = "response.json()"

    elif client is enums.PythonModule.aiohttp:
        handler = "await response.json()"

    elif client is enums.PythonModule.urllib:
        handler = "json.loads(response.read())"

    elif client in [enums.PythonModule.urllib3, enums.PythonModule.http]:
        handler = "json.loads(response.data)"

    else:
        handler = "response.json()"

    if isinstance(response, enums.PythonType):
        return handler

    elif isinstance(response, str):
        if response.isdigit():
            response = f"Field{response}"

        if model in [enums.PythonModule.pydantic, enums.PythonModule.dataclasses]:
            return f"[{response}(**item) for item in {handler}]" if array else f"{response}(**{handler})"

        elif model is enums.PythonModule.msgspec:
            return (
                f"[msgspec.convert(item, {response}) for item in {handler}]"
                if array
                else f"msgspec.convert({handler}, {response})"
            )

        else:
            return handler
