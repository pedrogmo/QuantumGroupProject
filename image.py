from typing import Final, Self
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PIL import Image as PILImage
from bitstring import Bits

import lz4.frame

PRECISION: Final[int] = 8


def decompress(bitstr: str) -> str:
    raw_bitstr = Bits(bin=bitstr).tobytes()
    bitstr = lz4.frame.decompress(raw_bitstr).decode()

    return bitstr


def compress(bitstr: str) -> str:
    compressed_bits = lz4.frame.compress(
        bitstr.encode(), compression_level=lz4.frame.COMPRESSIONLEVEL_MAX
    )
    bitstr = Bits(bytes=compressed_bits).bin

    return bitstr


def convert_bitstr_to_bytes(bitstr: str, precision: int = 8) -> bytes:
    # split up the bitstring into precision bit-chunks
    bit_chunks = [bitstr[i : i + precision] for i in range(0, len(bitstr), precision)]

    # convert each bit-chunk to a byte using the Bits class
    bytes_list = [Bits(bin=chunk, length=precision).tobytes() for chunk in bit_chunks]

    # concatenate the bytes together
    byt = b"".join(bytes_list)

    return byt


def convert_bytes_to_bitstr(data: bytes, precision: int = 8) -> str:
    # for each byte in the data, convert it to a bitstring using the Bits class

    bit_chunks = [Bits(uint=byte, length=precision).bin for byte in data]

    return "".join(bit_chunks)


class Image:
    path: Path
    width: int
    height: int
    buffer: PILImage.Image

    encoding: str = "RGB"

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

        data: bytes = convert_bitstr_to_bytes(bitstr, PRECISION)

        return PILImage.frombytes(mode, size, data)

    @staticmethod
    def _encode(image: PILImage.Image, mode: str) -> str:
        """Encodes a PIL Image to a bitstring

        Returns:
            str: Returns a bitstring
        """

        if mode != "1":
            image = image.convert(mode)
        else:
            image = image.split()[0].point(lambda p: p > 1 and 255).convert(mode)
        data: bytes = image.tobytes()

        return convert_bytes_to_bitstr(data)

    @classmethod
    def from_bitstr(
        cls: Self,
        bitstr: str,
        width: int = 16,
        height: int = 16,
        encoding: str = None,
        compress_flag: bool = True,
    ) -> Self:
        """Creates an instance of the Image class from a bitstring

        Args:
            bitstr (str): Bitstring representation of the image
            width (int, optional): Image width. Defaults to 16.
            height (int, optional): Image height. Defaults to 8.

        Returns:
            Image: Returns an instance of the Image class
        """
        new_instance: Image = cls.__new__(Image)
        new_instance.width = width
        new_instance.height = height
        new_instance.path = "bitstring"

        encoding = encoding or cls.encoding

        if compress_flag:
            bitstr = decompress(bitstr)

        new_instance.buffer = cls._decode(bitstr, encoding, (width, height))

        return new_instance

    def to_bitstr(self, encoding: str = None, compress_flag: bool = True) -> str:
        """Converts the image to a bitstring

        Returns:
            str: Returns the bitstring representation of the image
        """

        encoding = encoding or self.encoding

        bitstr = self._encode(self.buffer, encoding)

        if compress_flag:
            bitstr = compress(bitstr)

        return bitstr

    def display(self, subplot=(1, 1, 1)):
        """Displays the image using matplotlib"""
        print(f"Displaying image from {self.path}")
        plt.subplot(subplot[0], subplot[1], subplot[2])
        plt.imshow(self.buffer)
        plt.axis("off")
