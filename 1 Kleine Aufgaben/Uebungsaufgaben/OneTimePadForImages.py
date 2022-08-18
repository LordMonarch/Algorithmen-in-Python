# Verwenden Sie ein One-Time-Pad, um Bilder zu verschlüsseln und zu entschlüsseln

from secrets import token_bytes
from typing import Tuple


def random_key(length: int) -> int:
    # length Zufalls-Bytes erzeugen
    tb: bytes = token_bytes(length)
    # Diese Bytes in einem Bit-String konvertieren und zurückgeben
    return int.from_bytes(tb, "big")


def encrypt(original: bytes) -> Tuple[int, int]:
    original_bytes: bytes = original  # Hier kein String mehr
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR
    return dummy, encrypted


def decrypt(key1: int, key2: int) -> bytes:
    decrypted: int = key1 ^ key2  # XOR
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp  # Hier kein String mehr


if __name__ == "__main__":
    datei = open('Bild.jpg', 'rb')  # Bild einlesen
    start: bytes = datei.read()

    key1, key2 = encrypt(start)
    result: bytes = decrypt(key1, key2)

    datei = open('Bild_result.jpg', 'wb')  # Bild abspeichern
    datei.write(result)


