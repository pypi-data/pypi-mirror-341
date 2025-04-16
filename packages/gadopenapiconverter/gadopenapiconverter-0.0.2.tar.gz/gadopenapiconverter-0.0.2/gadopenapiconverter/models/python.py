import pydantic


class PythonFunction(pydantic.BaseModel):
    coroutine: bool
    name: str
    arguments: str
    response: str | None = None
    serialize: str | None = None
