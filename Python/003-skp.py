import keyboard
import time

def main():
    while True:
        if input("Start? ") == "y":
           start_loop()
        

def start_loop():
    while True:
        keyboard.press_and_release("esc")
        time.sleep(2)

main()
