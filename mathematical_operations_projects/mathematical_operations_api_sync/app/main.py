from fastapi import FastAPI
from app import services, store
from app.models import (PowerInput, FibonacciInput, FactorialInput,
                        FloatOutput, IntegerOutput)
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.init_db()
    yield


app = FastAPI(
    title="Mathematical Operations",
    version="1.0.0",
    description="Power / N-th Fibonacci / N Factorial",
    lifespan=lifespan
)


@app.post("/power", response_model=FloatOutput)
def power(data: PowerInput):
    result = services.power(data.base, data.exponent)
    output = FloatOutput(result=result)
    store.save_request("power", data.model_dump(), output.model_dump())
    return output


@app.post("/fibonacci", response_model=IntegerOutput)
def fibonacci(data: FibonacciInput):
    result = services.fibonacci(data.n)
    output = IntegerOutput(result=result)
    store.save_request("fibonacci", data.model_dump(), output.model_dump())
    return output


@app.post("/factorial", response_model=IntegerOutput)
def factorial(data: FactorialInput):
    result = services.factorial(data.n)
    output = IntegerOutput(result=result)
    store.save_request("factorial", data.model_dump(), output.model_dump())
    return output


@app.get("/history")
def history():
    logs = store.fetch_history()
    rows = []
    for ID, op, params, res, ts in logs:
        rows.append(f"{ID}. {op}({params}) = {res} at {ts}")
    return rows
