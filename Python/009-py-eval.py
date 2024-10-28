# Python script that returns a value after passing it to the eval() function. This is supposed to be my offline calculator.

OPEN_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"
MULTIPLY_X = "x"
MULTIPLY_SIGN = "*"


def main():
    
    equation = input( "Enter equation: " ).replace( MULTIPLY_X, MULTIPLY_SIGN )
    if equation.count( OPEN_PARENTHESIS ) == equation.count( CLOSING_PARENTHESIS ):
        return eval( equation ) 
    else:
        return "Your parenthesis count is uneven. Please change your equation."


if __name__ =="__main__":
    print( main() )