import sys

sys.path.append("..")
sys.path.append(".")

import image
from image import Image

from bitstring import Bits


mario_path = "./images/mario.png"


def display_mario_test():
    img = Image(mario_path)

    img.display()


def bitstr_mario_test():
    img = Image(mario_path)

    bitstr = img.to_bitstr()
    print(f"Length of bitstr: {len(bitstr)}")

    img2 = Image.from_bitstr(bitstr)

    img2.display()


def convert_bitstr_to_bytes_test():
    precision = 8

    test_str = "123"
    test_bytes = test_str.encode()

    test_bitstr = image.convert_bytes_to_bitstr(test_bytes, precision)

    result_bytes = image.convert_bitstr_to_bytes(test_bitstr, precision)
    result_str = result_bytes.decode()

    assert test_str == result_str


if __name__ == "__main__":
    # display_mario_test()
    bitstr_mario_test()
    # convert_bitstr_to_bytes_test()
