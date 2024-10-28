# Script to convert a given bitstring to decimal in unsigned binary representation.
NONE = ""
ONCE = 1
ONE =1
START = 0
ZERO = 0
RADIX = 2
MINIMUM = 1

def main():
    return bin_to_dec(input("Enter binary: "))

def bin_to_dec(bit_str):
    curr_bit = bit_str[START]
    exponent = len(bit_str) - ONE
    value = int(curr_bit) * RADIX**exponent
    if len(bit_str)>MINIMUM:
        return value + bin_to_dec(bit_str.replace(curr_bit,NONE,ONCE))   
        
    else:
        return value

if __name__ =="__main__":
    print( main())
