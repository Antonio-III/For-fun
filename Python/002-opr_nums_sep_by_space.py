# This file is for copy-pasting numbers from a `.csv` file. 
# Its general purpose is to RETURN THE SELECTED OPERATION OF INPUTTED NUMBERS

def main():
    while True:
        print( "Select mode (Enter 'q' to exit or press `ctrl+c`):" )
        
        try:        
            operation = input( "1: Add \n2: Average\n" )
            numbers = input( "Numbers: " )

        except (KeyboardInterrupt):
            break
            
        else:
            if operation.lower() == "q" or numbers.lower() == "q":
                break
            
            result = operate(operation, numbers)

            print( result ) if result != None else None
        
        
      

def operate(mode, str):
    list = str.split()
    
    sums = sum( [ int( value ) for value in list if value.isnumeric() ] )

    match mode:
            case "1":
                answer = sums

            case "2": 
                numerator = sums
                denominator = len( list )

                answer = numerator / denominator
            
            case _:
                print("Invalid mode")

    try:
        return answer
    
    except UnboundLocalError: 
        return None    
    
        

main()