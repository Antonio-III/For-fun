import csv

# Python script to interact with `.csv` files.


def main():
    while True:
        print("What function do you want to call? Press `ctrl+c` to exit")

        try:
            feature = input("(1) create_mod_file    (2) round_values    (3) columns_to_rows\n")

            input_file = input("Input directory and file name of target file (case-sensitive)\n")
            output_file = input("Input name of output file\n")
            keep_header = True if input("Keep header? y/n\n").lower() =="y" else False

            match feature:
                case "1":
                    incl_col_nums_input = input("Input column numbers to be included. Ex: 1, 2, 5.\n")
                    incl_col_nums = [ int( entry.strip() ) for entry in incl_col_nums_input.split(",") ] if len(incl_col_nums_input)>0 else []

                    incl_col_cond_nums_input = input("Input column numbers of conditions (opt.). Ex: 3, 4, 7. Press `Enter` to leave it empty.\n")
                    incl_col_cond_nums = [ int( entry.strip() ) for entry in  incl_col_cond_nums_input.split(",") ] if len(incl_col_cond_nums_input)>0 else []

                    conds_should_be_input = input("Input what those conditions should be (opt.). Ex: not-, Data Scientist-or-scientist, greater_than-42. All entries will be converted to lowercase. `not-` is converted to `!=''`; different from `not- ` (!=' '). Press `Enter` to leave it empty.\n")
                    conds_should_be = [ entry for entry in conds_should_be_input.split(",") ] if len(conds_should_be_input)>0 else []

                    create_mod_file(input_file, output_file, incl_col_nums, incl_col_cond_nums, conds_should_be, keep_header)
                
                case "2":

                    target_col = int( input("Input column number to get the average off of\n") )

                    custom_header = [ entry.strip() for entry in input("Input custom header. The input file's header is ignored since it may not contain numeric values. Ex. Date, Time, Place, Location\n").split(",") ]
                    rounded_to = int( input("Rounded to? Defaults to ones place.\n") )

                    round_values(input_file, output_file, target_col, custom_header, keep_header, rounded_to)
                
                case "3":
                    columns_to_rows(input_file, output_file, keep_header)

                case _:
                    print("Invalid feature")
                    continue

        except KeyboardInterrupt:
            print("Exit successful")
            break

        except ValueError:
            print("Some of the values you wrote cannot be converted to the data type they should be. Try again.")
            continue

        
            
        print(f"Function call complete. {output_file} is created.")


# Used to strip unwanted columns, but it doesn't have to.
# NEEDS AN UPDATE: TRY/EXCEPT CLAUSE
# Algorithm of `create_mod_file`: 
    # 0.    0. Input the directory and file name of the target file, in `str` type. Can just be the file name if it's already in the same directory as this file.
    #       1. Input the name of the output file, in `str` format. 
    #       2. Input column numbers of columns you want to include. `Int` objects in a `list`. 
    #       3. Input column numbers of columns who contain conditions you want to check (optional). `Int` objects in a `list`.
    #       4. Input `str` objects of what those conditions should be (optional). `Str` objects in a `list`.
    #       5. Input `bool` object whether to skip the first line of the inputted file (optional. Will skip by default).
    # Arguments 3 and 4 should both have inputs or none at all, and the same length. They exist in case you want to strip unwanted columns. 
    # 1. Create a reference to all the contents of the input file. This is so that having the same input and output file is supported.
    # 2. Create variable that holds #0.2's list but all values are offset by 1. `Int` objects in a `list`.
    # 3. Open inputted file.
    # 4. Make `writer` object of said file, so we can access `writerow` method for later.
    # 5. Iterate through a returned `list` object from `filtered_rows`, passing #0.0; and #0.3~5 for further filtering. `entry` is the reference for the iterated values.
    # 6. Make a `generator` object consisting of the current iteration's elements, but only including the column numbers that the user included. 
    # 7. Pass this generator object to `writerow` method of the `writer` object, essentially writing new text to the output file.
    # 8. Return 
# Summary: Rewrite the inputted file into a new file. Can remove columns.

                    #0
def create_mod_file( input_file_dir: str, output_file_name: str, include_columns: list, col_num_of_conds: list = [], conds_must_be: list = [], keep_header: bool = True ):
    #1.
    input_file = filtered_rows( input_file_dir, col_num_of_conds, conds_must_be, keep_header )
    #2.
    incl_col_index = [ (n - 1) for n in include_columns ] # Hard coded 

    #3.
    with open( output_file_name, "w", newline="" ) as opened_file: # remove newlines (by default it writes a newline, but our inputted csv should aready have newlines)
        error = False
        #4.
        write_file = csv.writer( opened_file )
        #5.
        for entry in input_file:
            try:
                            #7.         #6.
                write_file.writerow(  [ entry[index] for index in incl_col_index ] )

            except IndexError:
                error = True
                print("ERROR: Included columns has a column number that doesn't exist in the input file. Output file will instead copy all of input file.")
                break
        
        if error:
            for entry in input_file:
                write_file.writerow( [ entry[ index ] for index in range( len( entry ) ) ] )

    #8.
    return


# Used in other functions. Too niche to be used as a stand-alone.
# Algorithm of `get_avg`
    # 0.    0. Input the directory and file name of the target file, in `str` type. Can just be the file name if the file's already in the same directory as this script.
    #       1. Input the column numbers of the columns whose rows we want the average of. The column's values must be numeric only. `Int` object.
    #       2. Input the column numbers of the columns who have conditions we want to check (optional). `Int` objects in a `list`
    #       3. Input what the respective conditions should be in a `list` object (optional). `Str` objects in a `list`
    # Arguments 2 and 3 must both have inputs or none at all, and the same length. They exist in case your inputted csv is more generalized.
    #       4. Input integer to be rounded (defaults to 'ones' place, optional). `Int` object
    # 1. Reference holding a returned `list` object from `filtered_rows`.
    # 2. Reference holding an empty `list` object. To be used later.
    # 3. Reference holding #0.1 being offset by 1. `Int` object.
    # 4. Iterate through #1's list.
    #   5. Obtain the current iteration's value using #3 as the index. `Str` object.
    #   6. Append #5 to #2's list.
    # 7. Create a generator object holding `int` objects of #2's list. Then obtain the sum of all the items in this `generator`. `Int` object.
    # 8. Get the length of #2's list. `Int` object.
    # 9. Return the quotient of #7/#8. `Int` object.
    # 10 In the case of errors, their respective information will be displayed, and return `0` instead.
# Summary: Obtain the averages of rows whose columns match a condition (if any), else just obtain averages of all rows (top to bottom) from a certain column.

            #0.
def get_avg( input_file_dir: str, col_num_to_get_avg_of: int, col_num_of_conds: list = [], conds_must_be: list = [], rounded_to: int = 0  ):
    #1.
    rows = filtered_rows( input_file_dir, col_num_of_conds, conds_must_be )
    #2.
    averages = []
    #3.
    column_index = col_num_to_get_avg_of - 1 
    #4.
    for element in rows:
        #6.             #5.                
        averages.append( element[column_index] ) # element[column_index] MUST be an int

    
    try:
        #9.                 #7.                     #8.
        return sum( [int(i) for i in averages] ) / len( averages )
    #10.
    except ValueError:
        print(f"The values in column {col_num_to_get_avg_of} aren't all numeric")
        return 0
    #10.
    except ZeroDivisionError:
        print(f"No values added in column {col_num_to_get_avg_of}")
        return 0
  




# If you want to have non-equal comparisons, use `greater_than`, `less_than`, `not`, separated by `-`. 
# Ex: filtered_rows("test.csv", "4", "less_than-0").
    # This returns rows with values that are `value < 0` in column `4`. 
# This is for stripping unwanted columns, or just get the row's values.
def filtered_rows( input_file_dir: str, col_num_of_conds: list = [], conds_must_be: list = [], keep_header: bool = True ):
    spec_conds = {"not": "!=", "greater_than": ">", "less_than": "<"}
    
    result = []

    try:
        opened_file = open( input_file_dir, "r" ) 

    except FileNotFoundError:
        print(f"{input_file_dir} does not exist. An empty file is written instead.")
        return []
    
    else:
        with opened_file:
            reader_file = csv.reader(opened_file)

            if keep_header:
                # Add support to `csv` separated by ';'. Bruh
                # [ 'ind;id', 'name' ] (x) becomes [ 'ind', 'id', 'name' ] (y), but (y) becomes (y). i.e. it only fixes rows with ';' separator.
                result.append( ";".join( next(reader_file) ).split(";") ) 
                
            for row in reader_file:
                row = ";".join(row).split(";") # Just reassign the variable. This is what `row` is intended to be, accounting for the bad `csv`s

                conditions_met = True
                
                
                for column, statement in zip( col_num_of_conds, conds_must_be ):
                    column_index = column - 1 # Users will input the column number starting from 1. We offset by 1. Hard coded

                    try:
                        col_val = row[column_index].lower()
                    except IndexError:
                        print(f"Some included column numbers don't exist in the inputted file: {input_file_dir}.")
                        return []
                    
                    # Add support for `or` filtering
                    if "-or-" in statement:
                        if or_check(col_val, statement):
                            continue
                        else:
                            conditions_met = False
                            break
                    else:
                        split_statement = statement.lower().split( "-" ) # Will look like: ["not", "abc"] or ["abc"] when passed ["not-abc"] or ["abc"]

                        # Converted to `float` so that number-like entries (7, 1.2, 5.888, NOT 1.2.3) from user inputs and the `csv` to have at least 1 decimal place; for comparison purposes.
                        # Converted to `str` because some `csv`s have no data in the column whereas the user might want to filter out those empty entries. And we can't compare `float`s to `str`s.
                        # Zfill is so that a `str` 99.0 becomes 099.0 when being compared to 100.0. Not having a zfill will lead to the evaluation that 99.0 is greater than 100.0.
                        if is_decimal_num( split_statement[-1] ): # This is from user input
                            split_statement[-1] = str( float( split_statement[-1] ) ).zfill( len(col_val) )
                        
                        if is_decimal_num( col_val ): # This is from the `csv`
                            col_val = str( float( col_val ) ).zfill( len(split_statement[-1]) )

                        opr_kwrd, cond = split_statement if len( split_statement ) >= 2 else ( None, split_statement[-1] )
                        opr_sign = spec_conds.get(opr_kwrd, '==')
               
                        if eval(f"col_val {opr_sign} cond"):
                            continue

                        else:
                            conditions_met = False
                            break
                   
                    
                if conditions_met:
                    result.append( row )
        
        return result

        
def get_unique_values( input_file_dir: str, target_column: int,  ):
    names = []
    column_index = target_column - 1

    with open(input_file_dir, "r", ) as file:

        for index, row in enumerate(file):
            row = row.strip().split(",")
            
            if index == 0:
                continue

            names.append( row[column_index] )

    return sorted( set(names) )

# step 2 (the only good thing in this script): write a csv file with the calculated column_4s 
def create_avg_csv(input_file_dir: str, file_name: str, header: list, col_num_to_get_avg_of: int, get_uniq_val_in_this_cols: list,  ):
    with open( file_name, "w", newline="" ) as mod:
        write_file = csv.writer( mod )

        write_file.writerow( header )

        create_nested_loops() 

def create_nested_loops( starting_index: int = 0, starting_list: list = [] ):
    # write your function nigga
    pass


# Primary Function
def round_values(input_file_dir: str, output_csv_file: str, target_col_num: int, header: list = [], keep_header: bool = True, rounded_to: int = 0):
    col_index = target_col_num - 1 # Offset. Hard coded


    with open(output_csv_file, "w", newline="") as file_write:
        file_write = csv.writer(file_write)
        
        file_write.writerow(header) if header else None

        for entry in filtered_rows(input_file_dir, keep_header = keep_header):
          
            file_write.writerow( [ entry[i] for i in range(col_index) ] + [ round( float( entry[col_index] ), rounded_to ) ] )


# For when your data's values are sorted by columns and want to convert it to rows. 
# Example:
#   --
# Date  Name    Id
# 2024  Jo      0
#   --
# The data above will convert to:
#   --
# Date  2024
# Name  Jo
# Id    0
#   --
# Algorithm of `columns_to_rows`
    # 0.    0. Input the directory and file name of the target file, in `str` type. Can just be the file name if it's already in the same directory as this file.
    #       1. Input the name of the output file, in `str` format. 
    #       2. Input `bool` object whether to skip the first line of the inputted file (optional. Will not skip by default).
    # 1. Create a reference to all the contents of the input file. This is so that having the same input and output file is supported.
    # 2. Write to a file.
    # 3. Create `writer` object
    # 4. Get returned list from `filtered_rows` (It will return the contents of the input file in a `list` object with no modifications)
    # 5. Unpack the contents of this list, meaning all its elements will be used as arguments when passed to `zip`.
    # 6. Iterate through #4.'s zip object.
    # 7. Create `generator` object consisting of elements from the current iteration.
    # 8. Write the contents of #6's object to the output file.
# Summary: `zip()` outputs a group of tuples whereby the first argument's elements are index 0, the 2nd argument's will be index 1... of these outputted tuples. Essentially converting the data from being sorted by columns to being sorted by rows. Then write these outputted data into an output file.

                    #0.
def columns_to_rows(input_file_dir: str, output_file_name: str, keep_header: bool = False):
    #1.
    input_file = filtered_rows(input_file_dir, keep_header = keep_header)
                                #2.
    with open(output_file_name, "w", newline="") as opened_file:
        #3.
        file_writer = csv.writer( opened_file )
        
        #6.             #5.         #4. 
        for entry in zip( *input_file ):
                        #8.         #7.
            file_writer.writerow( [values for values in entry] )

    return    
# Future feature: add rows from inputted files. The code below is adding the values of `goog, meta, aapl--_mod.csv` to data_set_3. Including data_set_3's data, which is `dates`
# goog = filtered_rows("goog_mod.csv",keep_header=False) 
# meta = filtered_rows("meta_mod.csv",keep_header=False)
# aapl = filtered_rows("aapl_mod.csv",keep_header=False)
# dates = filtered_rows("dates.csv",keep_header=False)
# with open("data_set_3.csv", "w", newline="") as opened_file:
#     writer_file = csv.writer(opened_file)
    
#     for data in [dates, goog, meta, aapl]:
#         for entry in data:
#             writer_file.writerow( [element for element in entry] )
                

# OR check algorithm

def or_check(target: str, filter: str, index: int = 0):
    cond = filter.split("-or-")
  
    if index == len(cond):
        return False
        
    return target == cond[index] or or_check(target, filter, index + 1)


# Check `filtered_rows`
def is_decimal_num(n: str, index = 0):
    new_n = n.replace(".","")
    if len(new_n) == index or new_n[index].isdecimal() == False:
        return False
    
    return new_n[index].isdecimal() or is_decimal_num(n, index+1) # supports `.2` decimals 

main()


