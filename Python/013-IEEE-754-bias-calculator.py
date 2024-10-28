# This script calculates the IEEE 754 bias of a given bit pattern or bit amount entered.

import re

BINARY_RADIX = 2
BIT_PATTERN_REGEX = r"^[01]+$"
NUM_BITS_REGEX = r"^\d+$"

ONE = 1
ZERO = 0


def main() -> int:
    mode = input("(1) Do you want to enter the bit pattern or (2) Enter the amount of bits used? \n")
    match mode:
        case "1":
            return bias_notation_bit_pattern(bit_pattern=input("Enter bit pattern: "))
        case "2":
            return bias_notation_num_bits(num_bits=input("Enter number of bits used: "))
        case _:
            print("Invalid input. Must be `1` or `2` only.")
            return ZERO

def bias_notation_bit_pattern(bit_pattern: str) -> int:
     
    if re.fullmatch(BIT_PATTERN_REGEX, bit_pattern):
        return BINARY_RADIX** ( len(bit_pattern) - ONE) - ONE

    else:
        return ZERO

def bias_notation_num_bits(num_bits: str) -> int:

    if re.fullmatch(NUM_BITS_REGEX, num_bits):

        return BINARY_RADIX** ( int(num_bits) - ONE) - ONE

    else:
        return ZERO

if __name__=="__main__":
    try:
        print( main() )
    except ValueError:
        print("The returned value exceeds the 4300-digit limit. Python's print function cannot handle this.")