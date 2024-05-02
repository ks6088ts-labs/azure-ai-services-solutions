import typer

app = typer.Typer()


@app.command()
def backend():
    print(f"Hello backend")


@app.command()
def frontend():
    print(f"Hello frontend")


if __name__ == "__main__":
    app()
