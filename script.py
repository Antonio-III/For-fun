import keyboard

def main():
    while True:
        if input("Start? ") == "y":
           start_loop()
        

def start_loop():
    while True:
        keyboard.press_and_release("esc")

main()