import requests
from time import perf_counter


url = "http://127.0.0.1:80"


def test_power(base, exponent):
    return requests.post(f"{url}/power",
                         json={"base": base, "exponent": exponent})


def test_fibonacci(n):
    return requests.post(f"{url}/fibonacci", json={"n": n})


def test_factorial(n):
    return requests.post(f"{url}/factorial", json={"n": n})


if __name__ == "__main__":
    start = perf_counter()

    for i in range(30):
        test_fibonacci(i)

    end = perf_counter()

    print(f"Time: {end-start:.2f} seconds")
