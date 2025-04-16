from gadopenapiconverter import typings


class SpecificationSchemaType(str, typings.Enum):
    object = "object"
    array = "array"
    string = "string"
    integer = "integer"
    number = "number"
    boolean = "boolean"
    null = "null"


class SpecificationSchemaFormat(str, typings.Enum):
    int32 = "int32"
    int64 = "int64"
    float = "float"
    double = "double"
    byte = "byte"
    binary = "binary"
    date = "date"
    date_time = "date-time"
    password = "password"
    uuid = "uuid"
    email = "email"
    uri = "uri"


class SpecificationSecurityType(str, typings.Enum):
    bearer = "HTTPBearer"
    basic = "HTTPBasic"
