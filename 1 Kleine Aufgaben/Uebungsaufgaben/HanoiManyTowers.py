# Schreiben Sie eine Lösungsfunktion dür die Türme von Hanoi, die mit einer beliebi-
# gen Anzahl von Türmen funktioniert.

import random
from typing import TypeVar, Generic, List

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)


num_discs: int = 20
towers: List = []
for _ in range(random.randrange(3, 21)):  # Zufallstürme von 3 bis 20
    towers.append(Stack())
for i in range(1, num_discs + 1):
    towers[0].push(i)


if __name__ == "__main__":
    hanoi(towers[0], towers[-1], towers[1], num_discs)
    print(towers)

