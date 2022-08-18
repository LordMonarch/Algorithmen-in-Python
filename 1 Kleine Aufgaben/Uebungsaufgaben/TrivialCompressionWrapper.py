# Sie haben geshen, wie der einfache Typ int in Python verwendet werden kann, um
# einen Bit-String darzustellen. Schreiben Sie einen ergonomischen Wrapper um int,
# der generisch als Abfolge von Bits verwendet werden kann (machen Sie ihn iterierbar,
# und implementieren Sie __getitem__()). Implementieren Sie CompressedGene mithilfe
# des Wrappers neu.

from builtins import int
from sys import getsizeof


def decorator(cls):
    class Bits:
        def __init__(self):
            self.bit_string: int = 1

        def __iter__(self):
            for it in range(0, self.bit_string.bit_length() - 1, 2):  # - 1 to exclude sentinel
                yield it

        def __str__(self):
            return str(self.bit_string)

        def __sizeof__(self):
            return self.bit_string.__sizeof__()

        def __getitem__(self, item):
            gene: str = ""
            bits: int = self.bit_string >> item & 0b11
            self.bit_string << item
            if bits == 0b00:  # A
                gene += "A"
            elif bits == 0b01:  # C
                gene += "C"
            elif bits == 0b10:  # G
                gene += "G"
            elif bits == 0b11:  # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
            return gene

        def __add__(self, other):
            self.bit_string <<= 2
            if other == "A":  # Letzte zwei Bit in 00 ändern
                self.bit_string |= 0b00
            elif other == "C":  # Letzte zwei Bit in 01 ändern
                self.bit_string |= 0b01
            elif other == "G":  # Letzte zwei Bit in 10 ändern
                self.bit_string |= 0b10
            elif other == "T":  # Letzten zwei Bit in 11 ändern
                self.bit_string |= 0b11
            else:
                raise ValueError("Ungültiges Nukleotid:{}".format(other))

    return Bits


@decorator
class int(int):
    def __init__(self):
        pass


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = int()  # Mit Sentinel starten (Automatisch)
        for nucleotide in gene.upper():
            self.bit_string + nucleotide  # Nach Schema Buchstaben hinzufügen, und paarweise in Bits umwandeln

    def decompress(self) -> str:
        gene: str = ""
        for i in self.bit_string:   # Bits in Paaren durchlaufen
            gene += self.bit_string[i]  # Zurück umwandeln in Buchstaben
        return gene[::-1]  # [::-1] reverses string by slicing backwards

    def __str__(self) -> str:  # String-Darstellung für formatierte Ausgaben
        return self.decompress()


if __name__ == "__main__":
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("Original: {} Byte".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # Komprimieren
    print("Komprimiert: {} Byte".format(getsizeof(compressed.bit_string)))
    print(compressed)
    print(compressed.bit_string)

    print("Originaldaten und dekomprimierte Daten sind identisch".format(original == compressed.decompress()))
