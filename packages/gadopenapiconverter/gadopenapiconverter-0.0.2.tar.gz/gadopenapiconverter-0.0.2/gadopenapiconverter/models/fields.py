import pydantic

from gadopenapiconverter import enums
from gadopenapiconverter import typings


class Field(pydantic.BaseModel):
    required: bool
    priority: int
    python: list[enums.PythonType] = pydantic.Field(default_factory=list)
    wrappers: list[enums.TypingType] = pydantic.Field(default_factory=list)
    datamodels: list[typings.Model] = pydantic.Field(default_factory=list)
    default: typings.Default | None = None
