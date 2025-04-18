import argparse
from pathlib import Path

import rich
import typer
from typer.cli import app

from qtlizlib import commands
from qtlizlib.scripts import gen_qrc, gen_res_py, gen_css_py


# def main():
#     parser = argparse.ArgumentParser(description="Generators for qt/pyside projects.")
#
#     parser.add_argument("--gen-qrc", action='store_true', help='Generate .qrc file from paths')
#     parser.add_argument("--gen-res-py", action='store_true', help='Generate python variables from .qrc file')
#     parser.add_argument("--gen-css-py", action='store_true', help='Generate python variables from css file')
#
#     parser.add_argument("--qrc-path", type=str, help='Path of the .qrc')
#     parser.add_argument("--css-dir", type=str, help='Path of the css folder')
#     parser.add_argument("--res-dir", dest="resDirList", action="append", help="Path(s) to the folder containing the resources file to be includes in .qrc file.")
#     parser.add_argument("--py-file", action='store_true', help='Path of the .py file to be generated')
#     parser.add_argument("--py-file-class-name", type=str, help='Name of the class to be generated in the .py file')
#
#
#     args = parser.parse_args()
#
#     if args.gen_qrc:
#         if args.qrc_path and args.resDirList:
#             gen_qrc(Path(args.qrc_path), [Path(p) for p in args.resDirList])
#         else:
#             rich.print("You must provide both --qrc-path and --res-dirList")
#
#     if args.gen_res_py:
#         if args.qrc_path and args.py_file:
#             class_name = args.py_file_class_name if args.py_file_class_name else "ResourcesIds"
#             gen_res_py(args.qrc_path, args.py_file, class_name)
#         else:
#             rich.print("You must provide both --qrc-path and --py-file")
#
#     if args.gen_css_py:
#         if args.css_dir and args.py_file:
#             gen_css_py(Path(args.css_dir), Path(args.py_file))
#         else:
#             rich.print("You must provide both --css-dir and --py-file")


@app.command("gen-qrc")
def gen_qrc(
        qrc_path: Path = typer.Argument(..., help="Path del file .qrc (può non esistere)"),
        res_dir: list[Path] = typer.Argument(..., help="Uno o più path di directory esistenti contenenti risorse")
):
    for path in res_dir:
        if not path.is_dir():
            typer.echo(f"Errore: la cartella '{path}' non esiste.", err=True)
            raise typer.Exit(code=1)

    typer.echo(f"Generazione QRC in: {qrc_path}")
    typer.echo(f"Cartelle risorse:")
    for path in res_dir:
        typer.echo(f" - {path}")
    gen_qrc(qrc_path, res_dir)


@app.command("gen-res-ids")
def gen_res_ids(
        qrc_path: Path = typer.Argument(..., help="Path del file .qrc (deve esistere)"),
        py_file: Path = typer.Argument(..., help="Path del file Python da generare (può non esistere)"),
        class_name: str = typer.Option("ResourcesIds", help="Nome della classe da generare nel file Python")
):
    if not qrc_path.is_file():
        typer.echo(f"Errore: il file '{qrc_path}' non esiste.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Generazione identificatori risorse da '{qrc_path}' in '{py_file}'")
    gen_res_py(qrc_path, py_file, class_name)


@app.command("gen-css-py")
def gen_css_py(
        css_dir: Path = typer.Argument(..., help="Path della cartella CSS (deve esistere)"),
        py_file: Path = typer.Argument(..., help="Path del file Python da generare (può non esistere)")
):
    if not css_dir.is_dir():
        typer.echo(f"Errore: la cartella '{css_dir}' non esiste.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Generazione file Python da CSS nella cartella '{css_dir}' in '{py_file}'")
    gen_css_py(css_dir, py_file)



app = typer.Typer(help="Utility per la gestione delle risorse Qt e CSS.")


def main():
    typer.run(app)
