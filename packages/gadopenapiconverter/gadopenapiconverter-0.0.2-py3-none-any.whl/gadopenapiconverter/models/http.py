import pydantic


class HTTPRequest(pydantic.BaseModel):
    method: str
    url: str
    paths: list[str]
    queries: list[str]
    headers: dict[str, str]
    upload: bool
    body: bool
    data: bool
    file: bool
    files: bool
    auth: bool
