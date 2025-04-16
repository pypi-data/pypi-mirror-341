from gadopenapiconverter import typings


class TypingType(str, typings.Enum):
    array = "List"
    union = "Union"
    null = "Optional"
    any = "Any"

    def wrapp(self, annotation: str | None = None) -> str:
        if self in (self.array, self.union, self.null):
            return f"{self.value}[{annotation}]"
        else:
            return f"{self.value}"
