import pathlib
import shlex
import subprocess

import jinja2
import typer
from datamodel_code_generator import InputFileType
from datamodel_code_generator import generate as generate_models
from gadutils import json
from gadutils import paths
from gadutils import temp

from gadopenapiconverter import const
from gadopenapiconverter import enums
from gadopenapiconverter import mappers
from gadopenapiconverter import models
from gadopenapiconverter import parsers
from gadopenapiconverter.os import File
from gadopenapiconverter.os import Folder
from gadopenapiconverter.utils import files
from gadopenapiconverter.utils import specification
from gadopenapiconverter.utils import toml

app = typer.Typer(help="gadopenapiconverter")


@app.command()
def generate(
    file: str = typer.Option(..., "-f", "--file", help="Path or link to configuration file"),
    context: str = typer.Option("{}", "-c", "--context", help="JSON context for templates"),
) -> None:
    cwd = paths.current()

    file, buffer = toml.getconfig(file)

    config = toml.todict(File.read(file))

    if buffer:
        file.unlink(missing_ok=True)

    workdir = paths.define(config.get(const.SYNTAX_WORKDIR))

    Folder.create(workdir)

    context = json.fromjson(context)

    context["workdir"] = workdir

    specifications = config.get(const.SYNTAX_SPECIFICATION)

    if not specifications:
        return

    for spec in specifications:
        coroutine = spec.get(const.SYNTAX_SPECIFICATION_ASYNC, True)
        path = workdir / pathlib.Path(jinja2.Template(spec.get(const.SYNTAX_SPECIFICATION_PATH)).render(context))
        model = enums.PythonModule(spec.get(const.SYNTAX_SPECIFICATION_MODEL, enums.PythonModule.pydantic.value))
        client = enums.PythonModule(spec.get(const.SYNTAX_SPECIFICATION_CLIENT, enums.PythonModule.httpx.value))
        content = json.fromjson(files.getcontent(workdir=cwd, content=spec.get(const.SYNTAX_SPECIFICATION_CONTENT)))

        if operationids := spec.get(const.SYNTAX_SPECIFICATION_OPERATIONS, []):
            content = specification.filteroperations(content=content, operationids=operationids)

        content = specification.removemetadata(content)

        file, buffer = temp.getfile(str(content), extension=const.EXTENSION_JSON), True

        generate_models(
            file,
            output=path,
            input_file_type=InputFileType.OpenAPI,
            output_model_type=mappers.MAPPING_PYTHON_MODULE_TO_DATAMODEL.get(model),
            use_title_as_name=False,
        )

        if buffer:
            file.unlink(missing_ok=True)

        operations = parsers.parsespecification(
            coroutine=coroutine,
            client=client,
            model=model,
            spec=models.Specification(**content),
        )

        for request, function in operations:
            if request.upload:
                File.write(
                    path=path,
                    content=jinja2.Template(
                        File.read(pathlib.Path(const.TEMPLATE_MODULE_FILE.format(module=model.name)))
                    ).render(),
                    mode=const.FILE_APPEND,
                )
                break

        File.write(
            path=path,
            content=jinja2.Template(File.read(pathlib.Path(const.TEMPLATE_CLIENT))).render(),
            mode=const.FILE_APPEND,
        )

        for request, function in operations:
            File.write(
                path=path,
                content=const.SYMBOL_NEWLINE
                + jinja2.Template(File.read(pathlib.Path(const.TEMPLATE_METHOD))).render(
                    function=function.model_dump(), request=request.model_dump()
                ),
                mode=const.FILE_APPEND,
            )

        File.write(path=path, content=files.sortimports(File.read(path=path, tolist=True)))

        if scripts := config.get(const.SYNTAX_SCRIPTS, []):
            for script in scripts:
                if command := script.get(const.SYNTAX_SCRIPTS_COMMAND):
                    subprocess.run(
                        shlex.split(jinja2.Template(command).render(context)),
                        cwd=workdir,
                        text=True,
                        check=script.get(const.SYNTAX_SCRIPTS_CHECK, False),
                    )


if __name__ == "__main__":
    app()
