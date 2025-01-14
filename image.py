from typing import Self
import matplotlib.pyplot as plt
import numpy as np


class Image:
    path: str

    def __init__(self, path: str):
        self.path = path

        if path:
            self.buffer = plt.imread(self.path)
        else:
            raise ValueError("Invalid image path")

    def __init__(self, width: int, height: int):
        self.path = None
        self.width = width
        self.height = height

        self.buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)

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
        raise NotImplementedError
        new_instance: Image = cls()

        return new_instance

    def to_bitstr(self) -> str:
        """Converts the image to a bitstring

        Returns:
            str: Returns the bitstring representation of the image
        """
        raise NotImplementedError

    def display(self):
        """Displays the image using matplotlib"""
        print(f"Displaying image from {self.path}")
        plt.imshow(plt.imread(self.path))
