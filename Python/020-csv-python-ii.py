def main(dir:str,col_num:int)->None:
    table=get_csv_data(dir)
    scores=extract_col(table,col_num,False)
    new_scores=modify_column(scores)
    table=replace_col(table,col_num,new_scores,False)

    replace_csv_data(dir,table)
    input("Process completed. Press 'enter' to exit.\n")

def get_csv_data(dir:str)->list[str]:
    """
    1. Collects file data from the given directory.
    2. It is otherwise considered a generic "get all data from file" function, but slightly modified to fit the formatting of csv files.
    """
    csv_data=[]
    with open(dir,"r") as file_reader:
        # csv files have a "\n" at the end so we strip it.
        csv_data+=[row.strip().split(",") for row in file_reader]
    return csv_data

def replace_csv_data(dir:str,new_content:list[str])->None:
    """
    1. Writes data into a truncated file in the given directory.
    2. Function name uses the name csv for the purposes of this script. It is otherwise considered a generic "write to file" function.
    """
    write_to_file(dir,new_content)
    return None

def modify_column(column:list)->list[str]:
    """
    1. User instructions on how to modify the target column.
    """
    return [score.replace(" / 20","") for score in column]



# imported functions
def replace_col(table:list,pos:int,new_value:list,ignore_header:bool)->list[any]:
    """
    1. Replaces `pos-1`th column in table with `value` (list). 
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Has an option to ignore header.
        Ignoring header means to slice table as table[1:] instead of table[:].
    """
    pos-=1
    for row,new_val in zip(table[1:] if ignore_header else table[:],new_value):
        row[pos]=new_val
    return table
def extract_col(table:list,pos:int,ignore_header:bool)->list[any]:
    """
    1. Return a list of elements in the `n-1`th position of every row.
        1. `pos` is 1-indexed as an argument and is adjusted to be 0-indexed. Any reference to `pos` from this point on is 0-index.
    2. Has an option to ignore the first row (ignore_header:bool).
    3. Example: extract_col(table=table,n=1,ignore_header=True):
        1. if table =  [[1,2,3],
                       [4,5,6],
                       [7,8,9]]
        2. return: [4,7].
    """
    pos-=1
    return [ row[pos] for row in (table[1:] if ignore_header else table[:]) ]
def write_to_file(dir:str,new_content:list)->None:
    """
    This is a modified version of the original function.
    1. Truncates (clears) the file in the given directory.
    2. Writes contents into the file, with a "\n" at the end.
    """

    with open(dir,"w") as file_handler:
        for row in new_content:
            row_contents=",".join(row)
            file_handler.write(row_contents+"\n")
    return None

if __name__=="__main__":
    input("You have to make the instruction yourself on how the selected column is to be modified. Press 'enter' to continue.\n")
    DIR=input("Enter directory of the csv file you want to modify:\n")
    COL_NUM=int(input("Enter column number (1-indexed) that you want to modify:\n"))
   
    main(fr"{DIR}",COL_NUM)