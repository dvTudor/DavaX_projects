import aiohttp
import asyncio
from time import perf_counter


url = "http://127.0.0.1:80"


async def test_power(session, base, exponent):
    async with session.post(f"{url}/power",
                            json={"base": base, "exponent": exponent}) as resp:
        await resp.text()


async def test_fibonacci(session, n):
    async with session.post(f"{url}/fibonacci", json={"n": n}) as resp:
        await resp.text()


async def test_factorial(session, n):
    async with session.post(f"{url}/factorial", json={"n": n}) as resp:
        await resp.text()


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(30):
            tasks.append(test_fibonacci(session, i))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    end = perf_counter()
    print(f"Time: {end-start:.2f} seconds")
