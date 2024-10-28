# Script to enter a text, and replace it with a given character, and outputs the result.

INVALID_LEN = 0

def main():
    input_text = input("Enter text:\n")
    find_this_text = input("Enter characters that are to be replaced:\n")
    replacement_text = input("Enter replacement character:\n")

    return (find_and_replace(input_text, find_this_text, replacement_text))
    

def find_and_replace(text: str, find: str, replacement: str):
    match replacement:
        case r"\n":
            replacement = "\n"
        case r"\t":
            replacement = "\t"
        case _:
                replacement = replacement
    
    
    if INVALID_LEN in [len(text), len(find), len(replacement) ]:
            return f"Invalid lengths. Impossible to find & replace. Length text: {len(text)}, find: {len(find)}, replace: {len(replacement)}"
    while find in text:
        text = text.replace(find, replacement)
        
    return text

if __name__ == "__main__":
    print( main() )

