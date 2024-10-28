# Python script to delete white spaces of a given entry. 
# I use it to enter unsigned binary representation of numbers using Window's calculator to an online converter of binary -> dec.

def main( binary_str:str = input( "Enter binary string: ")):
    return "".join( binary_str.split())


if __name__=="__main__":
    print(main() )