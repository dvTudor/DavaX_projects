import click
from app import services, store
from app.models import (PowerInput, FibonacciInput, FactorialInput,
                        FloatOutput, IntegerOutput)


@click.group()
def cli():
    store.init_db()


@cli.command()
@click.argument("base", type=float)
@click.argument("exponent", type=float)
def power(base, exponent):
    data = PowerInput(base=base, exponent=exponent)
    result = services.power(data.base, data.exponent)
    output = FloatOutput(result=result)
    store.save_request("power", data.model_dump(), output.model_dump())
    click.echo(output.model_dump_json())


@cli.command()
@click.argument("n", type=int)
def fibonacci(n):
    data = FibonacciInput(n=n)
    result = services.fibonacci(data.n)
    output = IntegerOutput(result=result)
    store.save_request("fibonacci", data.model_dump(), output.model_dump())
    click.echo(output.model_dump_json())


@cli.command()
@click.argument("n", type=int)
def factorial(n):
    data = FactorialInput(n=n)
    result = services.factorial(data.n)
    output = IntegerOutput(result=result)
    store.save_request("factorial", data.model_dump(), output.model_dump())
    click.echo(output.model_dump_json())


@cli.command()
def history():
    logs = store.fetch_history()
    for ID, op, params, res, ts in logs:
        click.echo(f"{ID}. {op}({params}) = {res} at {ts}")


if __name__ == "__main__":
    cli()
