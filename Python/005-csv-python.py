import csv
from io import TextIOWrapper

# step 1 (optional): create a filtered file 
def create_mod_file( input_csv_file_dir: str, name_new_file: str, include_columns: list, columns_where_the_conditions_are: list = [], conditions_must_be: list = [] ):

    

    with open( name_new_file, "w", newline="" ) as mod:
        created_file = csv.writer( mod )

        for entry in filtered_rows( input_csv_file_dir, columns_where_the_conditions_are, conditions_must_be ):
            created_file.writerow(  [ entry[i] for i in include_columns ] )

    return created_file # optional

# Algorithm of `create_mod_file`:
    # 0. Input directory and or file name of a csv. Input name of the created modified file. Input included columns. Input column numbers (int) who contain conditions you want to check (optional). Must be in a list object. Input `str` of what those conditions should be. Must be in a list object.`
    # 1. Open file
    # 2. Make `writer` object of said file, so we can access `writerow` method for later.
    # 3. Iterate through a returned object from `filtered_rows`
    # 4. Make generator object consisting of the current iteration's (named `entry`) elements. 
    # 5. Pass this generator object to `writerow` method of the `writer` object, essentially creating 

def get_avg( input_csv_file_dir: str, column_to_get_avg_of: int, columns_where_the_conditions_are: list = [], conditions_must_be: list = [], rounded_to: int = 0  ):
    
    rows = filtered_rows( input_csv_file_dir, columns_where_the_conditions_are, conditions_must_be )

    target = []
    column_index = column_to_get_avg_of - 1
    
    for element in rows:
        target.append( element[column_index] ) # element[column_index] MUST be an int

    numerator =  sum( [int(i) for i in target] )
    denominator = len( target )

    try:
        return round( numerator / denominator, rounded_to )
    except ZeroDivisionError:
        return 0

# If you want to have non-equal comparisons, use `greater_than`, `less_than`, `not`, separated by `-`. 
# Ex: filtered_rows("test.csv", "4", "less_than-0").
    # This returns rows with values that are `condition <0` in column `4`. 
def filtered_rows( input_csv_file_dir: str, columns_where_the_conditions_are: list = [], conditions_must_be: list = [], skip_first_line: bool = True ):
    result = []

    special_conditions = {"not": "!=", "greater_than": ">", "less_than": "<"}

    with open( input_csv_file_dir, "r" ) as opened_file:
        opened_file = csv.reader(opened_file)
        
        if skip_first_line:
            next(opened_file)

        for row in opened_file:
            
            conditions_met = True
            
            
            for column, condition in zip( columns_where_the_conditions_are, conditions_must_be ):
                column_index = column - 1 # Users will input the column number starting from 1. We offset by 1. Hard coded

                splitted_condition = condition.lower().split( "-" ) # Will look like: ["not", "abc"] or ["abc"] when passed ["not-abc"] or ["abc"]
                splitted_condition[ len(splitted_condition)-1 ] = [ ord(i) for i in splitted_condition[-1] ] # Will be like [123]. "abc" became `[int("123")]`. Note that it became a list as well. It is also hard coded in a way the last element ought to be the value we're looking for

                # special_condition will be: [ "not", [123] ] or [ 123 ]

                # reassigned `condition` from `line 55`
                special_word, condition = splitted_condition if len( splitted_condition ) >= 2 else ( None, splitted_condition[-1] )

                val_in_col_nums = [ ord(i) for i in row[column_index].lower() ]

                try:
                    if eval(f"""{val_in_col_nums} {special_conditions.get(special_word, "==")} {condition}"""):
                        continue # move to next iter of `line 55`
                    else:
                        conditions_met = False
                        break # move to `line 79`
                    
                except IndexError:
                    print( "Last 2 arguments must be the same length" )
                    return []
                
            if conditions_met:
                result.append( row )
        
        return result

        
def get_unique_values( input_csv_file_dir: str, target_column: int,  ):
    names = []
    column_index = target_column - 1

    with open(input_csv_file_dir, "r", ) as file:

        for index, row in enumerate(file):
            row = row.strip().split(",")
            
            if index == 0:
                continue

            names.append( row[column_index] )

    return sorted( set(names) )

# step 2 (the only good thing in this script): write a csv file with the calculated column_4s 
def create_avg_csv(input_csv_file_dir: str, file_name: str, header: list, column_to_get_avg_of: int, get_uniq_val_in_this_cols: list,  ):
    with open( file_name, "w", newline="" ) as mod:
        created_file = csv.writer( mod )

        created_file.writerow( header )

        create_nested_loops() 

def create_nested_loops( starting_index: int = 0, starting_list: list = [] ):
    # write your function nigga
    pass
    
print(filtered_rows("mod_ds_salaries.csv", [2,3],["MI","Data Scientist"]))