bit_flip_threshold = 0.7
bit_flip_no = "0"
bit_flip_yes = "1"


def repetition_encode(bitstring: str, n: int=3) -> str:
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an uneven number")
    return "".join(bit * n for bit in bitstring)


def repetition_decode(bitstring: str, n: int=3) -> str:
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an uneven number")
    threshold = int((n - 1) / 2)

    results = list(bitstring[i:i + n] for i in range(0, len(bitstring), n))
    return "".join(list("1" if bit.count("1") > threshold else "0" for bit in results))


def bitstring_flip(bitstring: str) -> str:
    return "".join("1" if bit == "0" else "0" for bit in bitstring)


def bit_flip_encode(bitstring: str, n: int=2) -> str:
    if n % 2 == 1:
        raise ValueError("Invalid bit length: n should be an even number")

    count_1 = bitstring.count("1") / len(bitstring)
    if count_1 > bit_flip_threshold:
        return n * bit_flip_yes + bitstring_flip(bitstring)
    return n * bit_flip_no + bitstring


def bit_flip_decode(bitstring: str, n: int=2) -> str:
    if bitstring[0:n] == n * bit_flip_no:
        return bitstring[n:]
    return  bitstring_flip(bitstring[n:])
