import random
d={"Draw":0,"Lose":0,"Win":0}
exit=False
def main():
    while exit!=True:
        items=["rock","paper","scissors"]
        # player draws
        player=convert(input("Player: "),items)
        
        # computer draws
        computer=random.randint(0,len(items)-1)

        # item the computer drew
        print(f"Computer: {items[computer]}")

        # get result
        draw(player,computer)

        # prompt the user if they want to keep playing
        try_again()

def convert(input,rps):
    # return the index value of the chosen item
    for i in rps:
        first_letter=i[0]
        if input.startswith(first_letter):
            return rps.index(i)

def draw(user,cpu):
    global d
    results=["Draw","Lose","Win"]
    r=(user-cpu+3)%3

    # print the item of the index `r`
    print(results[r])

    # update the values in dictionary `d`
    d[results[r]]+=1

def try_again():
    global exit, d
    while True:
        response=input("try again? or type 's' to see W/L ")
        # no
        if response.startswith(("n","q")):
            exit=True
            break
        # stats
        elif response.startswith("s"):
            print("draw: {}    lose: {}    win: {}".format(*d.values()))
        # yes
        else:
            break
        
main()
