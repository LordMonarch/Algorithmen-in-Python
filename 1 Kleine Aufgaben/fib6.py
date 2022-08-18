from typing import Generator


def fib6(n: int) -> Generator[int, None, None]:
    yield 0  # Spezialfall
    if n > 0: yield 1  # Spezialfall
    last: int = 0  # Am Anfang auf fib(0) setzen
    next: int = 1  # Am Angang auf fib(1) setzen
    for _ in range(1, n):  # _ ist leere Variable
        last, next = next, last + next
        yield next  # Haupt-Generatorschritt


if __name__ == "__main__":
    for i in fib6(50):
        print(i)