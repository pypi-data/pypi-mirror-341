from gadopenapiconverter import typings


class PythonModule(str, typings.Enum):
    pydantic = "pydantic"
    dataclasses = "dataclasses"
    typing = "typing"
    msgspec = "msgspec"
    requests = "requests"
    httpx = "httpx"
    aiohttp = "aiohttp"
    urllib = "urllib"
    urllib3 = "urllib3"
    http = "http.client"


class PythonType(str, typings.Enum):
    object = "dict"
    array = "list"
    string = "str"
    integer = "int"
    number = "float"
    boolean = "bool"
    null = "None"
    bytes = "bytes"
