import random
d=0
l=0
w=0
d={"Draw":0,"Lose":0,"Win":0}
exit=False
def main():
    while exit!=True:
        options=["rock","paper","scissors"]
        # player draws
        player=convert(input("Player: "),options)
        
        # computer draws
        computer=random.randint(0,len(options)-1)

        # what computer drew
        print(f"Computer: {options[computer]}")

        # get result
        draw(player,computer)

        # prompt the user if they want to keep playing
        try_again()

def convert(input,rps):
    for i in rps:
        first_letter=i[0]
        if input.startswith(first_letter):
            return rps.index(i)

def draw(user,cpu):
    global d,l,w
    results=["Draw","Lose","Win"]
    print(results[(user-cpu)%3])
    d[results[(user-cpu)%3]]+=1

def try_again():
    global exit, d, l, w
    while True:
        response=input("try again? or type 's' to see W/L ")
        # no
        if response.startswith(("n","q")):
            exit=True
            break
        # stats
        elif response.startswith("s"):
            print(f"draw: {d}    lose: {l}    win: {w}")
        # yes
        else:
            break
main()
