import random
import statistics

people_group=[i for i in range(1,100+1)]

comparison_group=37
comparison_list=[]

chosen=0
chosen_list=[]
chosen_max_count=0

def simulate(amount=1):
    global people_group, comparison_group, comparison_list, chosen, chosen_list, chosen_max_count
    
    for r in range(amount):
        # Simulation count
        print(f"Simulation: {r+1}")

        # Change the order for every simulation
        random.shuffle(people_group)
        print(f"Order: {people_group}")
        
        # Go through the people_group
        for date in people_group:

            # If person is within the first 37 
            if people_group.index(date) in range(comparison_group+1):
                comparison_list.append(date)
                continue

            # If person is rated higher than the highest in comparison group,
            # OR the person is the last
            if date>max(comparison_list) or date==people_group[-1]:

                # Count how many times we encountered the highest rated person among all simulations
                if date==100:
                    chosen_max_count+=1

                # Person will be our chosen
                chosen=date
                chosen_list.append(chosen)
                
                break
            
            # If person isn't higher than the highest in comparison group
            if date < max(comparison_list):
                continue
        
        print(f"Highest in comparison: {max(comparison_list)}\n")

        # Clear the list for the next simulation,
        # so as not to include ratings that shouldn't have been there
        comparison_list.clear()
        
    # Print details at the end of simulation
    print(f"Chosen Group: {chosen_list}")
    print(f"Times 100 is chosen: {chosen_max_count}")
    print(f"Median: {statistics.median(chosen_list)}")
    print(f"Average of chosen group: {sum(chosen_list)/len(chosen_list)}")


# Execution of the simulation
simulate(
        100
        # Replace the number with any number, bigger numbers will take longer to finish, 
        # so maybe cap it to 10,000
        )

    
