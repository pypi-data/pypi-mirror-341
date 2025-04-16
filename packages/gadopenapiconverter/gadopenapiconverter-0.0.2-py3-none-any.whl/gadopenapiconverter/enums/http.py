from gadopenapiconverter import typings


class HTTPMethod(str, typings.Enum):
    get = "get"
    post = "post"
    put = "put"
    patch = "patch"
    delete = "delete"


class HTTPContentType(str, typings.Enum):
    json = "application/json"
    form = "application/x-www-form-urlencoded"
    multipart = "multipart/form-data"
    octet = "application/octet-stream"
    pdf = "application/pdf"
    zip = "application/zip"
    gzip = "application/gzip"
    tar = "application/x-tar"
    xml = "application/xml"

    plain = "text/plain"
    html = "text/html"
    csv = "text/csv"

    png = "image/png"
    jpeg = "image/jpeg"
    gif = "image/gif"
    bmp = "image/bmp"
    svg = "image/svg+xml"
    webp = "image/webp"


class HTTPAttribute(str, typings.Enum):
    header = "header"
    query = "query"
    path = "path"
    cookie = "cookie"
    body = "body"
    file = "file"
    files = "files"
    data = "data"
    auth = "auth"

    @property
    def priority(self) -> int:
        return [
            self.auth,
            self.cookie,
            self.header,
            self.path,
            self.query,
            self.body,
            self.file,
            self.files,
            self.data,
        ].index(self)
