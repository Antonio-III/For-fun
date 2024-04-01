import csv

#Primary function
# Algorithm of `create_mod_file`: 
    # 0.    (1) Input directory and or file name of a csv. 
    #       (2) Input name of the created modified file. 
    #       (3) Input column numbers of included columns in a list object. 
    #       (4) Input column numbers who contain conditions you want to check (optional). Must be in a list object. 
    #       (5) Input `str` of what those conditions should be. Must be in a list object.
    # 1. Offset by 1 to have zero-based index.
    # 1. Open inputted file.
    # 2. Make `writer` object of said file, so we can access `writerow` method for later.
    # 3. Iterate through a returned object from `filtered_rows`. `entry` is the reference.
    # 4. Make a generator object consisting of the current iteration's elements, but only including the column numbers that the user included. 
    # 5. Pass this generator object to `writerow` method of the `writer` object, essentially wiriting new text to the new `.csv` file.
    # 6. Return `writer` object (optional), if you need it for something else. 

def create_mod_file( input_csv_file_dir: str, name_new_file: str, include_columns: list, col_num_of_conds: list = [], conds_must_be: list = [], 
                    skip_first_line: bool = True ):

    incl_col_offset = [ (i - 1) for i in include_columns ] # Hard coded 

    with open( name_new_file, "w", newline="" ) as mod:
        created_file = csv.writer( mod )
        for entry in filtered_rows( input_csv_file_dir, col_num_of_conds, conds_must_be, skip_first_line ):
            created_file.writerow(  [ entry[i] for i in incl_col_offset ] )
            

    return created_file # optional



# Algorithm of `get_avg`
    # 0.    (1) Input csv file name and or directory. Input column number to get the average of. Column number must be numeric only. 
    #       (2) Input column numbers of conditions (optional), in a list object. 
    #       (3) Input what the respective conditions should be in a list object (optional). Both these arguments, while optional, MUST be the same length. 
    #       (4) Input integer to be rounded (defaults to nearest `int`, optional).
    # 1. Create reference to returned list object from `filtered_rows`
    # 2. 

def get_avg( input_csv_file_dir: str, col_num_to_get_avg_of: int, col_num_of_conds: list = [], conds_must_be: list = [], rounded_to: int = 0  ):
    
    rows = filtered_rows( input_csv_file_dir, col_num_of_conds, conds_must_be )

    target = []
    column_index = col_num_to_get_avg_of - 1 
    
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
# This is for stripping unwanted columns, or just get the row's values.
def filtered_rows( input_csv_file_dir: str, col_num_of_conds: list = [], conds_must_be: list = [], skip_first_line: bool = True ):
    special_conditions = {"not": "!=", "greater_than": ">", "less_than": "<"}

    result = []

    with open( input_csv_file_dir, "r" ) as opened_file:
        opened_file = csv.reader(opened_file)
        
        if skip_first_line:
            next(opened_file)

        for row in opened_file:
            
            conditions_met = True
            
            
            for column, condition in zip( col_num_of_conds, conds_must_be ):
                column_index = column - 1 # Users will input the column number starting from 1. We offset by 1. Hard coded

                splitted_condition = condition.lower().split( "-" ) # Will look like: ["not", "abc"] or ["abc"] when passed ["not-abc"] or ["abc"]
                splitted_condition[ len(splitted_condition)-1 ] = [ ord(i) for i in splitted_condition[-1] ] # "abc" will be like [1,2,3]. Note that it became a list as well. It is also hard coded in a way the last element ought to be the value we're looking for

                # special_condition at this point will be: [ "not", [1,2,3] ] or [ 1,2,3 ]

                # `condition` from `for` loop reassigned
                special_word, condition = splitted_condition if len( splitted_condition ) >= 2 else ( None, splitted_condition[-1] )

                val_in_col_nums = [ ord(i) for i in row[column_index].lower() ] # "abc" will be like [1,2,3]

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
def create_avg_csv(input_csv_file_dir: str, file_name: str, header: list, col_num_to_get_avg_of: int, get_uniq_val_in_this_cols: list,  ):
    with open( file_name, "w", newline="" ) as mod:
        created_file = csv.writer( mod )

        created_file.writerow( header )

        create_nested_loops() 

def create_nested_loops( starting_index: int = 0, starting_list: list = [] ):
    # write your function nigga
    pass


# Primary Function
def round_values(input_csv_file_dir: str, output_csv_file: str, target_col_num: int, skip_first_line: bool = True, rounded_to: int = 0, header: list = []):
    col_index = target_col_num - 1 # Offset. Hard coded


    with open(output_csv_file, "w", newline="") as file_write:
        file_write = csv.writer(file_write)
        
        file_write.writerow(header) if header else None

        for entry in filtered_rows(input_csv_file_dir, skip_first_line = skip_first_line):
          
            file_write.writerow( [ entry[i] for i in range(col_index) ] + [ round( float( entry[col_index] ), rounded_to ) ] )


def colums_to_rows(input_csv_file_dir: str, output_csv_file: str):

    with open(output_csv_file, "w") as file_writer:
        file_writer = csv.writer( file_writer )

        for entry in filtered_rows(input_csv_file_dir):
            file_writer.writerow( entry[] )
round_values("no-0-avg.csv", "rounded.csv", 4, rounded_to= 0, header =["work_year", "experience_level", "job_title", "salary_in_usd"] )
#print(filtered_rows("no-0-avg.csv"))
