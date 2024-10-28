# press G every `x` seconds. It's for a macro in a game.

import keyboard
import time

TIME_BEFORE_START = 3


ZERO_SECONDS = 0
ONE_SECOND = 1

CD_BEFORE_NEXT_KEY = 1
CD_BEFORE_NEXT_ITER = 50

STAGE_KEY = "g" # Runs a macro that presses which stage to run.
SPAM_KEY = "v" # Runs a macro that presses the screen repeatedly.


def main():
    heads_up()
    press_keys()
    

def heads_up():
    global TIME_BEFORE_START
    while TIME_BEFORE_START > ZERO_SECONDS:
        print(f"Starting in...{TIME_BEFORE_START}")
        TIME_BEFORE_START -= ONE_SECOND
        time.sleep(ONE_SECOND)
    
def press_keys():

    press_key(STAGE_KEY)

    wait(CD_BEFORE_NEXT_KEY)

    press_key(SPAM_KEY)

    wait(CD_BEFORE_NEXT_ITER)


def press_key(this_key: str):
    keyboard.press_and_release(this_key)
    print(f"{this_key} is pressed.")

def wait(seconds_to_wait: int):
    while seconds_to_wait > ZERO_SECONDS:
        print(f"Waiting...{seconds_to_wait}")
        time.sleep(ONE_SECOND)
        seconds_to_wait-=ONE_SECOND


if __name__ == "__main__":
    while True:
        main()