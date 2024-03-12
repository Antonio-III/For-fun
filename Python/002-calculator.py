# This file is for copy-pasting numbers from a `.csv` file. 
# Its general purpose is to RETURN THE SUM OF INPUTTED NUMBERS

def main():
    while True:
        try:
            prompt = input( "Numbers: " )
            print(add( prompt ) )
            
        except EOFError:
            break
        except ValueError:
            pass
        else:
            if prompt.lower() == "q":
                break


def add(str):
    l = str.split()
    
    numerator = sum( [ int( i ) for i in l ] )
    denominator = len( l )

    return round( numerator / denominator )


main()