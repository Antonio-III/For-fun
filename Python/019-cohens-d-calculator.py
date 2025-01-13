def main(c:dict,e:dict)->None:
    """
    1. Prints Cohen's d (effect size) using data from Control and Experiment. Only usable if this is module is directly run.
        1. See most bottom line to see what the values are. 
    """
    n=[0,c["n"],e["n"]] # optional to update

    mean=[0,c["mean"],e["mean"]]
    std=[0,c["std"],e["std"]]
    pooled_std=pooled_std_for_cohen_d(std)

    effect_size=calculate_cohens_d(mean,pooled_std)
    print(f"Effect size: {effect_size}")

    return None

def pooled_std_for_cohen_d(std:tuple)->float:
    """
    1. Returns the pooled standard deviation of 2 groups.
    """
    return ((std[1]**2+std[2]**2)/2)**0.5
    
def pooled_std_for_cohen_d_alt(std:tuple,n:tuple)->float:
        """
        1. Returns the pooled standard deviation of 2 groups using an alternative formula. 
        """
        numerator=(n[1]-1)*(std[1]**2)+(n[2]-1)*(std[2]**2)
        denominator=n[1]+n[2]-2

        return (numerator/denominator)**0.5

def calculate_cohens_d(mean:tuple,pooled_std:float):
    """
    1. Effect size interpretation, though you should not be the standard for all contexts.
        1. Very small = 0.01
        1. Small = 0.2.
        2. Medium = 0.5.
        3. Large = 0.8.
        4. Very large = 1.2.
        5. Huge = 2.
    """
    return (abs(mean[1]-mean[2]))/pooled_std


if __name__=="__main__":
    # These data are from my csv file projects.
    C={"n":16,"mean":8.750000,"std":4.343578}
    E={"n":18,"mean":8.777778,"std":3.370382}
    main(C,E)