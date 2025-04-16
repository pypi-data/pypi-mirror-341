import copy

from gadutils import strings

from gadopenapiconverter import const
from gadopenapiconverter import typings


def getmodel(ref: str) -> str:
    return strings.pascal(ref.split(const.SYMBOL_FORWARD_SLASH)[-1])


def filteroperations(content: dict, operationids: list[str]) -> dict:
    def findrefs(data: typings.Any, refs: set[str]) -> None:
        if isinstance(data, dict):
            if ref := data.get(const.SPECIFICATION_REF):
                if isinstance(ref, str):
                    refs.add(ref)
            else:
                for value in data.values():
                    findrefs(value, refs)
        elif isinstance(data, list):
            for item in data:
                findrefs(item, refs)

    content = copy.deepcopy(content)

    paths = content.get(const.SPECIFICATION_PATHS)
    components = content.get(const.SPECIFICATION_COMPONENTS)
    schemas = components.get(const.SPECIFICATION_COMPONENTS_SCHEMAS) if components else None

    operations, refs = dict(), set()

    for path, methods in paths.items():
        filtered = dict()

        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            if not (operation_id := operation.get(const.SPECIFICATION_PATH_OPERATION_ID)):
                continue
            if not operation_id in operationids:
                continue

            filtered[method] = operation_id

            findrefs(operation, refs)

        if filtered:
            operations[path] = filtered

    if operations:
        content[const.SPECIFICATION_PATHS] = operations

    models = {getmodel(ref) for ref in refs}

    if schemas:
        content[const.SPECIFICATION_COMPONENTS][const.SPECIFICATION_COMPONENTS_SCHEMAS] = {
            name: schema for name, schema in schemas.items() if name in models
        }

    return content


def removemetadata(content: dict) -> dict:
    def cleankeys(data: typings.Any):
        if isinstance(data, dict):
            data.pop(const.SPECIFICATION_DESCRIPTION, None)
            data.pop(const.SPECIFICATION_EXAMPLE, None)
            for key, value in data.items():
                cleankeys(value)
        elif isinstance(data, list):
            for item in data:
                cleankeys(item)

    content = copy.deepcopy(content)

    cleankeys(content)

    return content
