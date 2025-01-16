from typing import Final, Self
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PIL import Image as PILImage

PRECISION: Final[int] = 3


def convert_bitstr_to_bytes(bitstr: str) -> bytes:
    if len(bitstr) % PRECISION != 0:
        raise ValueError("Invalid bitstring length")

    return bytes(
        int(bitstr[i : i + PRECISION], 2) for i in range(0, len(bitstr), PRECISION)
    )


def convert_bytes_to_bitstr(data: bytes) -> str:
    return "".join(f"{round(byte / (2**(len(bin(max(data))[2:]) - PRECISION))):0{PRECISION}b}" for byte in data)


class Image:
    path: Path
    width: int
    height: int
    buffer: PILImage.Image

    def __init__(self, path: str):
        self.path = Path(path)

        if path:
            self.buffer = PILImage.open(self.path)
        else:
            raise ValueError("Invalid image path")

        self.width = self.buffer.width
        self.height = self.buffer.height

    @staticmethod
    def _decode(bitstr: str, mode: str, size: tuple[int, int]) -> PILImage.Image:
        """Decodes a bitstring to a PIL Image

        Args:
            bitstr (str): Bitstring to decode
            mode (str): Image mode
            size (tuple[int, int]): Image size

        Returns:
            PILImage.Image: Returns a PIL Image
        """

        data: bytes = convert_bitstr_to_bytes(bitstr)

        return PILImage.frombytes(mode, size, data)

    @staticmethod
    def _encode(image: PILImage.Image) -> str:
        """Encodes a PIL Image to a bitstring

        Returns:
            str: Returns a bitstring
        """

        data: bytes = image.tobytes()

        return convert_bytes_to_bitstr(data)

    @classmethod
    def from_bitstr(cls: Self, bitstr: str, width: int = 16, height: int = 8) -> Self:
        """Creates an instance of the Image class from a bitstring

        Args:
            bitstr (str): Bitstring representation of the image
            width (int, optional): Image width. Defaults to 16.
            height (int, optional): Image height. Defaults to 8.

        Returns:
            Image: Returns an instance of the Image class
        """
        new_instance: Image = cls()
        new_instance.width = width
        new_instance.height = height

        new_instance.buffer = cls._decode(bitstr, 'RGB', (width, height))

        return new_instance

    def to_bitstr(self) -> str:
        """Converts the image to a bitstring

        Returns:
            str: Returns the bitstring representation of the image
        """
        return self._encode(self.buffer)

    def display(self):
        """Displays the image using matplotlib"""
        print(f"Displaying image from {self.path}")
        plt.imshow(self.buffer)
