from pydantic import BaseModel, Field


class PowerInput(BaseModel):
    base: float
    exponent: float


class FibonacciInput(BaseModel):
    n: int = Field(ge=1, description="Fibonacci input must be at least 1")


class FactorialInput(BaseModel):
    n: int = Field(ge=1, description="Factorial input must be at least 1")


class FloatOutput(BaseModel):
    result: float


class IntegerOutput(BaseModel):
    result: int
