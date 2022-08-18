# Schreiben Sie eine weiter Funktion, die Elment n der Fibonacci-Folge berechnet und
# ein Verfahren Ihrer eigenen Wahl verwendet. Schreiben Sie Unit-Tests, die seine Kor-
# rektheit und seine Performance im Vergleich zu den anderen Versionen in diesem
# Kapitel überprüfen.

from typing import Dict, List
from functools import lru_cache
from typing import Generator
import unittest
import time


class AllFib:

    def __init__(self):
        self._memo: Dict[int, int] = {0: 0, 1: 1}  # Unsere Abbruchbedingungen

    def fib1(self, n: int) -> int:
        return self.fib1(n - 1) + self.fib1(n - 2)

    def fib2(self, n: int) -> int:
        if n < 2:
            return n
        return self.fib2(n - 2) + self.fib2(n - 1)

    def fib3(self, n: int) -> int:
        if n not in self._memo:
            self._memo[n] = self.fib3(n - 1) + self.fib3(n - 2)  # Memorisation
        return self._memo[n]

    @lru_cache(maxsize=None)
    def fib4(self, n: int) -> int:  # Dieselbe Definition wie fib2()
        if n < 2:  # Abbruchbedingung
            return n
        return self.fib4(n - 1) + self.fib4(n - 2)  # Rekursionsbedingung

    @staticmethod
    def fib5(n: int) -> int:
        if n == 0:
            return n  # Spezialfall
        last: int = 0  # Am Anfang auf fib(0) setzen
        next: int = 1  # Am Anfang auf fib(1) setzen
        for _ in range(1, n):  # _ ist leere Variable
            last, next = next, last + next
        return next

    @staticmethod
    def fib6(n: int) -> Generator[int, None, None]:
        yield 0  # Spezialfall
        if n > 0: yield 1  # Spezialfall
        last: int = 0  # Am Anfang auf fib(0) setzen
        next: int = 1  # Am Angang auf fib(1) setzen
        for _ in range(1, n):  # _ ist leere Variable
            last, next = next, last + next
            yield next  # Haupt-Generatorschritt


class TestAllFib(unittest.TestCase):
    def timeAndMessage(self, name: str) -> None:
        print(
            "Zeit für {1}: {0:5f}s".format(time.time() - self.start_time, name))  # Ausgabe Zeitstempel und Methodenname

    def setUp(self) -> None:
        # Die ersten 10 Fibonaci Zahlen
        self.correct_numbers: List = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.iterations: int = len(self.correct_numbers)
        # Zu testende Klasse
        self.af: AllFib = AllFib()
        self.start_time: time = time.time()

    def test_fib1(self):
        # Arrange
        outcome: List = []
        # Act
        # Laeuft nicht durch erzeugt einen Endlosrekursion-Fehler
        try:
            for i in range(self.iterations):
                outcome.append(self.af.fib1(i))
        except RecursionError:
            self.timeAndMessage("fib1")
            self.assertRaises(RecursionError)
        return

    def test_fib2(self):
        # Arrange
        outcome: List = []
        # Act
        for i in range(self.iterations):
            outcome.append(self.af.fib2(i))
        # Assert
        self.timeAndMessage("fib2")
        self.assertEqual(outcome, self.correct_numbers)

    def test_fib3(self):
        # Arrange
        outcome: List = []
        # Act
        for i in range(self.iterations):
            outcome.append(self.af.fib3(i))
        # Assert
        self.timeAndMessage("fib3")
        self.assertEqual(outcome, self.correct_numbers)

    def test_fib4(self):
        # Arrange
        outcome: List = []
        # Act
        for i in range(self.iterations):
            outcome.append(self.af.fib4(i))
        # Assert
        self.timeAndMessage("fib4")
        self.assertEqual(outcome, self.correct_numbers)

    def test_fib5(self):
        # Arrange
        outcome: List = []
        # Act
        for i in range(self.iterations):
            outcome.append(self.af.fib5(i))
        # Assert
        self.timeAndMessage("fib5")
        self.assertEqual(outcome, self.correct_numbers)

    def test_fib6(self):
        # Arrange
        outcome: List = []
        # Act
        for i in range(self.iterations):
            outcome.append(list(self.af.fib6(i)))  # Generator to List
        # Assert
        self.timeAndMessage("fib6")
        self.assertEqual(outcome[-1], self.correct_numbers)  # Letztes Generator Element in Liste ist das vollstaendige


if __name__ == "__main__":
    unittest.main()
