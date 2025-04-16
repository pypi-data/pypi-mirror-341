import http

from gadutils import strings

from gadopenapiconverter import const
from gadopenapiconverter import enums
from gadopenapiconverter import mappers
from gadopenapiconverter import models
from gadopenapiconverter import typings
from gadopenapiconverter.utils import codegeneration
from gadopenapiconverter.utils import specification


def parsetype(schema: models.SpecificationSchema) -> enums.PythonType:
    if schema.format is enums.SpecificationSchemaFormat.binary:
        return mappers.MAPPING_TYPE_SPECIFICATION_TO_PYTHON[(schema.type, schema.format)]
    else:
        return mappers.MAPPING_TYPE_SPECIFICATION_TO_PYTHON[schema.type]


def parseitems(
    items: models.SpecificationSchema
    | models.SpecificationReference
    | list[models.SpecificationSchema | models.SpecificationReference],
) -> tuple[list[enums.PythonType], list[typings.Model], typings.Default | None]:
    default = None
    python, datamodels = [], []

    if isinstance(items, models.SpecificationReference):
        datamodels.append(specification.getmodel(items.ref))

    elif isinstance(items, models.SpecificationSchema):
        datamodels.append(parsetype(items))
        default = items.default if items.default else default

    elif isinstance(items, list):
        for item in items:
            if isinstance(item, models.SpecificationReference):
                datamodels.append(specification.getmodel(item.ref))
            else:
                python.append(parsetype(item))
                default = item.default if item.default else default

    return python, datamodels, default


def parseof(
    schema: models.SpecificationSchema | models.SpecificationReference,
) -> tuple[list[enums.PythonType], list[typings.Model], list[enums.TypingType], typings.Default | None]:
    null = False
    default = None
    python, datamodels, wrappers = [], [], []

    if isinstance(schema, models.SpecificationReference):
        datamodels.append(specification.getmodel(schema.ref))

    for item in schema.anyOf or schema.oneOf or schema.allOf:
        if isinstance(item, models.SpecificationReference):
            datamodels.append(specification.getmodel(item.ref))

        elif isinstance(item, models.SpecificationSchema) and item.type is enums.SpecificationSchemaType.null:
            null = True

        elif item.items:
            _python, _datamodels, _default = parseitems(item.items)
            python.extend(_python)
            datamodels.extend(_datamodels)
            default = _default if _default else default

        else:
            python.append(parsetype(item))
            default = item.default if item.default else default

    if len(python + datamodels) > 1:
        wrappers.append(enums.TypingType.union)

    if null:
        wrappers.append(enums.TypingType.null)

    return python, datamodels, wrappers, default


def parseresponses(
    responses: dict[http.HTTPStatus, models.SpecificationPathOperationResponse],
) -> tuple[str | None, bool]:
    array = False
    response = None, None
    python, datamodels, wrappers = [], [], []

    for status in (http.HTTPStatus.OK, http.HTTPStatus.CREATED, http.HTTPStatus.ACCEPTED):
        if not (response := responses.get(status)):
            continue

        if not (content := response.content):
            continue

        for _, schema in content.items():
            if not (model := schema.model):
                continue

            if isinstance(model, models.SpecificationSchema) and model.type is None:
                continue

            if isinstance(model, models.SpecificationReference):
                response = specification.getmodel(model.ref)

            elif isinstance(model, models.SpecificationSchema):
                if model.anyOf or model.oneOf or model.allOf:
                    python, datamodels, wrappers, _ = parseof(model)
                else:
                    python, datamodels, _ = parseitems(model.items)

                if python:
                    response = python[0]

                elif datamodels:
                    response = datamodels[0]

                if wrappers:
                    for wrapper in wrappers:
                        response = wrapper.wrapp(response)
                        if wrapper is enums.TypingType.array:
                            array = True

            break

    return response, array


def parserequest(
    request: models.SpecificationPathOperationRequestBody,
) -> tuple[bool, bool, bool, bool, bool, dict[str, str], dict[str, models.Field]]:
    upload = False
    default = None
    body, data, file, files = False, False, False, False
    headers, arguments = {}, {}
    python, datamodels, wrappers = [], [], []
    attribute = enums.HTTPAttribute.body
    required = request.required if request.required is not None else False

    for content_type, content in request.content.items():
        headers[const.HTTP_HEADER_CONTENTTYPE] = codegeneration.setstring(content_type.value)

        if content_type is enums.HTTPContentType.json:
            body = True
            model = content.model
            attribute = enums.HTTPAttribute.body

            if isinstance(model, models.SpecificationReference):
                datamodels.append(specification.getmodel(model.ref))

            elif isinstance(model, models.SpecificationSchema):
                if model.anyOf or model.oneOf or model.allOf:
                    python, datamodels, wrappers, default = parseof(model)
                else:
                    python, datamodels, default = parseitems(model.items)

            else:
                python.append(parsetype(model))
                default = model.default

        elif content_type is enums.HTTPContentType.multipart:
            model = content.model

            if isinstance(model, models.SpecificationReference):
                file = True
                attribute = enums.HTTPAttribute.file
                datamodels.append(specification.getmodel(model.ref))

            elif isinstance(model, models.SpecificationSchema):
                upload = True
                datamodels.append(const.MODEL_UPLOAD_FILE)

                if model.type is enums.SpecificationSchemaType.array:
                    files = True
                    attribute = enums.HTTPAttribute.files
                    wrappers.append(enums.TypingType.array)
                else:
                    file = True
                    attribute = enums.HTTPAttribute.file

        elif content_type is enums.HTTPContentType.form:
            data = True
            attribute = enums.HTTPAttribute.data
            python.append(enums.PythonType.object)

        else:
            continue

        arguments[attribute.value] = models.Field(
            required=required,
            priority=attribute.priority,
            python=python,
            wrappers=wrappers,
            datamodels=datamodels,
            default=default,
        )

    return upload, body, data, file, files, headers, arguments


def parsesecurity(
    security: list[dict[enums.SpecificationSecurityType, list[str]]],
) -> tuple[bool, list[str], dict[str, str], dict[str, models.Field]]:
    auth = False
    queries = []
    headers, arguments = {}, {}

    for _security in security:
        for _type, _ in _security.items():
            if _type is enums.SpecificationSecurityType.bearer:
                headers[const.HTTP_HEADER_BEARER] = codegeneration.setfstring(const.HTTP_HEADER_BEARER_VALUE)
                arguments[const.HTTP_HEADER_BEARER_KEY] = models.Field(
                    required=True,
                    priority=enums.HTTPAttribute.header.priority,
                    python=[enums.PythonType.string],
                )
            elif _type is enums.SpecificationSecurityType.basic:
                auth = True
                arguments[const.HTTP_AUTH_USERNAME] = models.Field(
                    required=True,
                    priority=enums.HTTPAttribute.auth.priority,
                    python=[enums.PythonType.string],
                )
                arguments[const.HTTP_AUTH_PASSWORD] = models.Field(
                    required=True,
                    priority=enums.HTTPAttribute.auth.priority,
                    python=[enums.PythonType.string],
                )
            else:
                name = strings.snake(_type)
                queries.append(name)
                arguments[name] = models.Field(
                    required=True,
                    priority=enums.HTTPAttribute.query.priority,
                    python=[enums.PythonType.string],
                )

    return auth, queries, headers, arguments


def parseparameter(
    parameter: models.SpecificationPathOperationParameter | models.SpecificationReference,
) -> tuple[list[str], list[str], dict[str, str], dict[str, models.Field]]:
    default = None
    paths, queries = [], []
    headers, arguments = {}, {}
    python, datamodels, wrappers = [], [], []

    if isinstance(parameter, models.SpecificationReference):
        return paths, queries, headers, arguments

    model = parameter.model

    if isinstance(model, models.SpecificationReference):
        datamodels.append(specification.getmodel(model.ref))

    elif isinstance(model, models.SpecificationSchema):
        if isinstance(model, models.SpecificationReference):
            datamodels.append(specification.getmodel(model.ref))

        elif model.anyOf or model.oneOf or model.allOf:
            python, datamodels, wrappers, default = parseof(model)

        elif model.items:
            python, datamodels, default = parseitems(model.items)

        else:
            python.append(parsetype(model))
            default = model.default

    required = parameter.required if parameter.required is not None else False
    attribute = enums.HTTPAttribute(parameter.location)
    name = strings.snake(parameter.name)

    arguments[name] = models.Field(
        required=required,
        priority=attribute.priority,
        python=python,
        wrappers=wrappers,
        datamodels=datamodels,
        default=default,
    )

    if attribute is enums.HTTPAttribute.header:
        headers[parameter.name] = name
    elif attribute is enums.HTTPAttribute.path:
        paths.append(name)
    elif attribute is enums.HTTPAttribute.query:
        queries.append(name)

    return paths, queries, headers, arguments


def parseoperation(
    coroutine: bool,
    client: enums.PythonModule,
    model: enums.PythonModule,
    path: str,
    method: enums.HTTPMethod,
    operation: models.SpecificationPathOperation,
) -> tuple[models.HTTPRequest, models.PythonFunction]:
    upload, auth, body, data, file, files = False, False, False, False, False, False
    paths, queries = [], []
    headers, arguments = {}, {}
    name = strings.snake(operation.operationId) if operation.operationId else strings.snake(operation.summary)

    if operation.security:
        _auth, _queries, _headers, _arguments = parsesecurity(operation.security)
        auth = _auth
        queries.extend(_queries)
        headers.update(_headers)
        arguments.update(_arguments)

    if operation.parameters:
        for parameter in operation.parameters:
            _paths, _queries, _headers, _arguments = parseparameter(parameter)
            paths.extend(_paths)
            queries.extend(_queries)
            headers.update(_headers)
            arguments.update(_arguments)

    if operation.requestBody:
        _upload, _body, _data, _file, _files, _headers, _arguments = parserequest(operation.requestBody)
        upload = _upload
        body = _body
        data = _data
        file = _file
        files = _files
        headers.update(_headers)
        arguments.update(_arguments)

    response, array = parseresponses(operation.responses)

    function = models.PythonFunction(
        coroutine=coroutine,
        name=name,
        arguments=codegeneration.makearguments(
            sorted(
                arguments.items(),
                key=lambda item: (item[1].required, item[1].priority),
                reverse=True,
            )
        ),
        response=response,
        serialize=codegeneration.makeserialize(client, model, response, array),
    )

    request = models.HTTPRequest(
        method=method,
        url=path,
        paths=paths,
        queries=queries,
        headers=headers,
        upload=upload,
        body=body,
        data=data,
        file=file,
        files=files,
        auth=auth,
    )

    return request, function


def parsespecification(
    coroutine: bool,
    client: enums.PythonModule,
    model: enums.PythonModule,
    spec: models.Specification,
) -> list[tuple[models.HTTPRequest, models.PythonFunction]]:
    operations = []
    for path, item in spec.paths.items():
        for method in enums.HTTPMethod:
            if operation := getattr(item, method):
                operations.append(parseoperation(coroutine, client, model, path, method, operation))
    return operations
