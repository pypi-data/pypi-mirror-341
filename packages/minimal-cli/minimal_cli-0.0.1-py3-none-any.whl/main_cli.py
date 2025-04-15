import click

@click.command()
def cli():
    click.echo("Hello from minimal CLI!")

if __name__ == "__main__":
    cli()
