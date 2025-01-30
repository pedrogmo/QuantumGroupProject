pre_coding_threshold = 0.5
pre_coding_no = "0"
pre_coding_yes = "1"


def repetition_assert_n(n: int) -> None:
    # Repetition uses majority voting, meaning only odd numbers are allowed
    if n % 2 == 0:
        raise ValueError("Invalid multiplier: n should be an odd number")


def pre_coding_optimize_assert_n(n: int) -> None:
    # Pre-coding uses added on bit pairs, meaning only even numbers are allowed
    if n % 2 == 1:
        raise ValueError("Invalid bit length: n should be an even number")


def repetition_encode(bitstring: str, n: int=3) -> str:
    # Repeats each bit in the string n times
    repetition_assert_n(n)
    return "".join(bit * n for bit in bitstring)


def repetition_decode(bitstring: str, n: int=3) -> str:
    # Retrieves each bit from multiple sent bits using majority voting
    repetition_assert_n(n)
    threshold = int((n - 1) / 2)

    results = list(bitstring[i:i + n] for i in range(0, len(bitstring), n))
    return "".join(list("1" if bit.count("1") > threshold else "0" for bit in results))


def bitstring_invert(bitstring: str) -> str:
    # Flips every '0' to '1' and '1' to '0'
    return "".join("1" if bit == "0" else "0" for bit in bitstring)


def pre_coding_optimize_encode(bitstring: str, n: int=2) -> str:
    # Determines if bitstring should be inverted to achieve least '1' count and adds bits signaling if the bitstring
    # has been inverted or not.
    pre_coding_optimize_assert_n(n)
    count_1 = bitstring.count("1") / len(bitstring)
    if count_1 > pre_coding_threshold:
        return n * pre_coding_yes + bitstring_invert(bitstring)
    return n * pre_coding_no + bitstring


def pre_coding_optimize_decode(bitstring: str, n: int=2) -> str:
    # Reads the first few bits to determine if the bitstring has been inverted or not and returns the original bitstring
    pre_coding_optimize_assert_n(n)
    if bitstring[0:n] == n * pre_coding_no:
        return bitstring[n:]
    return  bitstring_invert(bitstring[n:])
