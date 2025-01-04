def main(c:dict,e:dict)->None:
    """
    1. Outputs the Cohen's d using data from C[ontrol] and E[xperiment].
    """
    n=(0,c["n"],e["n"])
    mean=(0,c["mean"],e["mean"])
    std=(0,c["std"],e["std"])
    
    equal_n,non_equal_n=calculate_pooled_std(std,n)
    pooled_std = equal_n if c["n"]==e["n"] else non_equal_n

    cohen_d=calculate_cohens_d(mean,pooled_std)
    print(cohen_d)

    return None

def calculate_pooled_std(std:tuple,n:tuple)->tuple:
    """
    1. Returns pooled standard devation of equal and non-equal-sized samples.
    """
    return pooled_std_equal(std),pooled_std_not_equal(std,n)

def pooled_std_equal(std:tuple)->float:
    """
    1. Use this function if you are assuming the sample sizes are equal.
    2. Returns the resulting pooled std by adding 2 groups' standard deviation squared and dividing by 2, and taking the square root of this number.
    """
    return ((std[1]**2+std[2]**2)/2)**0.5
    
def pooled_std_not_equal(std:tuple,n:tuple)->float:
        """
        1. Use this function if you are assuming the sample sizes aren't equal.
        """
        numerator=(n[1]-1)*(std[1]**2)+(n[2]-1)*(std[2]**2)
        denominator=n[1]+n[2]-2

        return (numerator/denominator)**0.5

def calculate_cohens_d(mean:tuple,pooled_std:float):
    """
    1. Size effect interpretation, though you should be flexible in interpretation of your Cohen's d instead of using this as the standard for all contexts.
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