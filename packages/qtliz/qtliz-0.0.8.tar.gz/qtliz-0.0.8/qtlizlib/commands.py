from pathlib import Path

import typer
from typer.cli import app


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
    # TODO: Logica per generare il file .qrc

@app.command("gen-res-ids")
def gen_res_ids(
        qrc_path: Path = typer.Argument(..., help="Path del file .qrc (deve esistere)"),
        py_file: Path = typer.Argument(..., help="Path del file Python da generare (può non esistere)")
):
    if not qrc_path.is_file():
        typer.echo(f"Errore: il file '{qrc_path}' non esiste.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Generazione identificatori risorse da '{qrc_path}' in '{py_file}'")
    # TODO: Logica per generare py_file da qrc_path

@app.command("gen-css-py")
def gen_css_py(
        css_dir: Path = typer.Argument(..., help="Path della cartella CSS (deve esistere)"),
        py_file: Path = typer.Argument(..., help="Path del file Python da generare (può non esistere)")
):
    if not css_dir.is_dir():
        typer.echo(f"Errore: la cartella '{css_dir}' non esiste.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Generazione file Python da CSS nella cartella '{css_dir}' in '{py_file}'")
    # TODO: Logica per generare py_file da css_dir



app = typer.Typer(help="Utility per la gestione delle risorse Qt e CSS.")