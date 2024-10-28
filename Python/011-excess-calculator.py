# This script counts how many bits are entered and returns the proper excess-K for that amount of bits.
import re

BINARY_RADIX = 2
BIT_PATTERN_REGEX = r"^[01]+$"
NUM_BITS_REGEX = r"^\d+$"

ONE = 1
ZERO = 0


def main(mode: str = input( "(1) Do you want to enter the bits or (2) Or how many bits are used? Enter the number `1` or `2`. \n")):
    match mode:
        case "1":
            return excess_k_bit_pattern(bit_pattern = input( "Enter binary string: \n"))

        case "2":
            return excess_k_num_bits(num_bits= input( "Enter bits used: \n"))
        case _:
            return f"Invalid input: {_}. Select which mode to use."

def excess_k_bit_pattern(bit_pattern: str) -> int:
    if re.fullmatch(BIT_PATTERN_REGEX, bit_pattern):
        return BINARY_RADIX**( len( bit_pattern ) - ONE)
    else:
        print( f"Input isn't binary: {bit_pattern}")
        return ZERO


def excess_k_num_bits(num_bits: str) -> int:
    if re.fullmatch(NUM_BITS_REGEX, num_bits):
        return BINARY_RADIX**( int(num_bits) - ONE)
    else:
        print(f"Input isn't numeric: {num_bits}.")
        return ZERO

if __name__ == "__main__":
    print( f"Proper excess-K: {main()}")