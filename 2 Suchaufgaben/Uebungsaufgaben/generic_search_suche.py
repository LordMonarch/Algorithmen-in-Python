# Zeigen Sie den Performancevorteil der binären Suche gegenüber der linearen Suche,
# indem Sie eine Liste von einer Millionen Zahlen erzeugen und die Zeit stoppen, wie
# lange die in diesem Kapitel definierten Funktionen linear_contains() und binary_
# contains() brauchen, um verschiedene Zahlen in der Liste zu finden.

from __future__ import annotations

import random
import statistics
import time
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing import Protocol
from heapq import heappush, heappop

T = TypeVar('T')

# Decorator um die Zeit zu messen, die der Vorgang benötigt.
# Für lineare und binäre Suche.
# Überschreibt leider die Funktionalität.
def time_measure(fnc):
    def inner(iterable: Iterable[T], key: T):
        start_time: time = time.time()
        result: bool = fnc(iterable, key)
        # print("Zeit für: {0:5f}s".format(time.time() - start_time))
        return time.time() - start_time

    return inner


@time_measure
def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return (self < other) or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


@time_measure
def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not ist für leeren Container True

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0,
                 heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    # Für Heapvergleich, verwendet < um PriorityQeue zu bestimmen
    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier bezeichnet, wohin wir noch gehen müssen
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored bezeichnet, wo wir schon waren
    explored: Set[T] = {initial}

    # Weitersuchen, solange es noch etwas zu entdecken gibt
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # Wenn wir das Ziel gefunden haben, sind wir fertig
        if goal_test(current_state):
            return current_node
        # Prüfen, wohin wir als Nächstes gehen können und wo wir noch
        # nicht gesucht haben
        for child in successors(current_state):
            if child in explored:  # Bereits durchsuchte Kindknoten überspringen
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # Alles durchsucht, aber nie das Ziel gefunden


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # Rückwärts vom Ende zum Anfang arbeiten
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Queue(Generic[T]):
    def __init__(self):
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container  # not ist leer für Container True

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO

    def __repr__(self) -> str:
        return repr(self._container)


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier bezeichnet, wohin wir noch gehen müssen
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored bezeichnet, wo wir schon waren
    explored: Set[T] = {initial}

    # Weitersuchen, solange es noch etwas zu entdecken gibt
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # Wenn wir das Ziel gefunden haben, sind wir fertig
        if goal_test(current_state):
            return current_node
        # Prüfen, wohin wir als Nächstes gehen können und wo wir noch
        # nicht gesucht haben
        for child in successors(current_state):
            if child in explored:  # Bereits durchsuchte Kindknoten überspringen
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # Alles durchsucht, aber nie das Ziel gefunden


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not ist für leere Container True

    def push(self, item: T) -> None:
        heappush(self._container, item)  # Hinein nach Priorität

    def pop(self) -> T:
        return heappop(self._container)  # Heraus nach Priorität

    def __repr__(self) -> str:
        return repr(self._container)


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    # frontier bezeichnet, wohin wir noch gehen müssen
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push((Node(initial, None, 0.0, heuristic(initial))))
    # explored bezeichnet, wo wir schon waren
    explored: Dict[T, float] = {initial: 0.0}

    # Weitersuchen, solange es noch etwas zu entdecken gibt
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # Wenn wir das Ziel gefunden haben, sind wir fertig
        if goal_test(current_state):
            return current_node
        # Prüfen, wohin wir als Nächstes gehen können und wo wir noch nicht waren
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1
            # 1 nimmt ein Gitter an; für komplexere Anwendungen ist eine
            # Kostenfunktion erforderlich
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None  # Alles durchsucht, aber nie das Ziel gefunden


if __name__ == "__main__":
    suchraum: int = 1000000
    suchzahlen: int = 100
    numbers: List = [i for i in range(suchraum)]
    numbers_linear: Dict = {}
    numbers_binary: Dict = {}

    for i in range(suchzahlen):
        key: int = int(random.random() * suchraum)
        numbers_linear[key] = linear_contains(numbers, key)
        numbers_binary[key] = binary_contains(numbers, key)

    print("Suche von {0} Zahlen im Suchraum von {1} Zahlen.".format(suchzahlen, suchraum))
    print("Zeit für lineare Suche:\t {0:5f}s".format(statistics.mean(numbers_linear.values())))
    print("Zeit für binäre Suche:\t {0:5f}s".format(statistics.mean(numbers_binary.values())))

