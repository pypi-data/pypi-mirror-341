<p align="center">
  <a href="https://github.com/AlexDemure/gadopenapiconverter">
    <a href="https://ibb.co/k6D5VxP6"><img src="https://i.ibb.co/Xk5jfbGk/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A CLI tool that generates HTTP clients from an OpenAPI specification.
</p>

---

### Installation

```
pip install gadopenapiconverter
```

### Usage

```sh
gadopenapiconverter --file {config.toml} --context "{}"
```

#### General Structure

```
workdir = "myproject"

[[specifications]]
path = "{{name}}.py"
content = "file:openapi.json"
client = "httpx"
model = "pydantic"
async = true
operations = []

[[scripts]]
command = "isort {{workdir}}"
check = true
```

### Sections Overview
| Section              | Format                               | Description                                                                           |   |   |
|----------------------|--------------------------------------|---------------------------------------------------------------------------------------|---|---|
| `workdir`            | `""`                                 | Uses the current directory                                                            |   |   |
|                      | `"myproject"`                        | Uses the current directory + `/myproject`                                             |   |   |
|                      | `"/home/myproject"`                  | Uses an absolute path                                                                 |   |   |
| `[[specifications]]` |                                      | Defines file creation rules                                                           |   |   |
|                      | `mode = "a"`                         | File writing mode: `"a"` (append), `"w"` (overwrite)                                  |   |   |
|                      | `path = "src/__init__.py"`           | Relative to workdir, specifies file location.                                         |   |   |
|                      | `content = """ ... """ / path / url` | Raw content, local file path, or URL for remote content.                              |   |   |
|                      | `model = "pydantic"`                 | Type of models created (pydantic, dataclasses, typing, msgspec)                       |   |   |
|                      | `client = "httpx"`                   | Type of http-client created (requests, httpx, aiohttp, urllib, urllib3, http.client)  |   |   |
|                      | `async = "true"`                     | Type of methods (true, false)                                                         |   |   |
|                      | `operations = []`                    | Filtering methods by operation_id                                                     |   |   |
| `[[scripts]]`        |                                      | Defines commands to be executed after generation.                                     |   |   |
|                      | `command = "isort {{workdir}}"`      | Command to execute, supports dynamic variables.                                       |   |   |
|                      | `check = True\False"`                | If true, raises an error if the command fails, otherwise logs output.                 |   |   |
