"""
Specification
├── openapi
├── info
│   ├── title
│   ├── description
│   └── version
├── paths
│   ├── <path>
│   │   ├── get
│   │   ├── post
│   │   ├── put
│   │   ├── patch
│   │   └── delete
│   │       ├── tags
│   │       ├── summary
│   │       ├── operationId
│   │       ├── parameters
│   │       │   ├── name
│   │       │   ├── in
│   │       │   ├── required
│   │       │   ├── description
│   │       │   └── schema
│   │       │       └── Schema | Reference
│   │       ├── requestBody
│   │       │   ├── required
│   │       │   └── content
│   │       │       └── <content-type>
│   │       │           └── schema
│   │       │               └── Schema | Reference
│   │       ├── responses
│   │       │   ├── <status-code>
│   │       │   │   ├── description
│   │       │   │   └── content
│   │       │   │       └── <content-type>
│   │       │   │           └── schema
│   │       │   │               └── Schema | Reference
│   │       └── security
├── components
│   └── schemas
│       └── <name>
│           ├── title
│           ├── type
│           ├── format
│           ├── enum
│           ├── description
│           ├── default
│           ├── properties
│           │   └── <name>: Schema | Reference
│           ├── required
│           ├── items
│           │   └── Schema | Reference
│           ├── allOf | anyOf | oneOf
│           │   └── List[Schema | Reference]
│           └── additionalProperties
│               └── bool | Schema | Reference
└── security
"""

from __future__ import annotations

import http

import pydantic

from gadopenapiconverter import enums
from gadopenapiconverter import typings


class SpecificationReference(pydantic.BaseModel):
    ref: str = pydantic.Field(..., alias="$ref")


class SpecificationSchema(pydantic.BaseModel):
    title: str | None = None
    type: enums.SpecificationSchemaType | None = None
    format: enums.SpecificationSchemaFormat | None = None
    enum: list[typings.Any] | None = None
    description: str | None = None
    default: typings.Any | None = None
    properties: dict[str, SpecificationSchema | SpecificationReference] | None = None
    required: list[str] | None = None
    items: SpecificationSchema | SpecificationReference | list[SpecificationSchema | SpecificationReference] | None = (
        None
    )
    allOf: list[SpecificationSchema | SpecificationReference] | None = None
    anyOf: list[SpecificationSchema | SpecificationReference] | None = None
    oneOf: list[SpecificationSchema | SpecificationReference] | None = None
    additionalProperties: bool | SpecificationSchema | SpecificationReference | None = None


class SpecificationContent(pydantic.BaseModel):
    model: SpecificationSchema | SpecificationReference | None = pydantic.Field(None, alias="schema")


class SpecificationPathOperationParameter(pydantic.BaseModel):
    name: str
    location: enums.HTTPAttribute = pydantic.Field(..., alias="in")
    required: bool | None = None
    description: str | None = None
    model: SpecificationSchema | SpecificationReference | None = pydantic.Field(..., alias="schema")


class SpecificationPathOperationRequestBody(pydantic.BaseModel):
    required: bool | None = None
    content: dict[enums.HTTPContentType, SpecificationContent]


class SpecificationPathOperationResponse(pydantic.BaseModel):
    description: str | None = None
    content: dict[enums.HTTPContentType, SpecificationContent] | None = None


class SpecificationPathOperation(pydantic.BaseModel):
    tags: list[str] | None = None
    summary: str | None = None
    operationId: str | None = None
    parameters: list[SpecificationPathOperationParameter | SpecificationReference] | None = None
    requestBody: SpecificationPathOperationRequestBody | SpecificationReference | None = None
    responses: dict[http.HTTPStatus, SpecificationPathOperationResponse]
    security: list[dict[enums.SpecificationSecurityType, list[str]]] | None = None


class SpecificationPath(pydantic.BaseModel):
    get: SpecificationPathOperation | None = None
    post: SpecificationPathOperation | None = None
    put: SpecificationPathOperation | None = None
    patch: SpecificationPathOperation | None = None
    delete: SpecificationPathOperation | None = None


class SpecificationInfo(pydantic.BaseModel):
    title: str
    description: str | None = None
    version: str


class SpecificationComponents(pydantic.BaseModel):
    schemas: dict[str, SpecificationSchema | SpecificationReference] | None = None


class Specification(pydantic.BaseModel):
    openapi: str
    info: SpecificationInfo
    paths: dict[str, SpecificationPath]
    components: SpecificationComponents | None = None
    security: list[dict[enums.SpecificationSecurityType | str, list[str]]] | None = None
