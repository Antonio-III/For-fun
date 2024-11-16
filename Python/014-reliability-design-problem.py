
COLUMNS=4
HEADER_COLS = ["D_i","C_i","r_i","u_i"]
DEVICES_TESTING = 3 # REMOVE LATER
ROUND_N_PLACES=4
STARTING_SET = {"S^0": {"S^0_0": [(1,0)]} }

def main():
    output = solv_reliability_design(c=105, devices=3, cost=[30,15,20],reliability_list=[.9,.8,.5],starting_set=STARTING_SET)
    print(output)

def solv_reliability_design(c:int,devices:int,cost:list,reliability_list:list,starting_set:dict):

    def get_rc_for_all_devices(devices:int,c_i:list,r_i:list,u_i:list,starting_set:dict):
        all_sets = starting_set
        for d in range(devices):
            curr_subset = {}

            curr_set_num=f"S^{d+1}"
            prev_set_num=f"S^{d}"

            
            for j in range(u_i[d]):
                copy_in_curr_d = j+1

                subset_name = f"{curr_set_num}_{copy_in_curr_d}"
                curr_subset[subset_name] = []
                
                r_of_curr_item=1-(1-r_i[d])**copy_in_curr_d
                c_of_curr_item = c_i[d]*copy_in_curr_d

                
                len_of_prev_main_set = len(all_sets[prev_set_num])

                for l in range(len_of_prev_main_set):
                    copy_in_prev_set=l+1

                    prev_subset_obj = all_sets[prev_set_num][f"{prev_set_num}_{copy_in_prev_set if not d_first_key_is_k(d=all_sets,k=prev_set_num) else 0}"]

                    len_of_prev_subset = len(prev_subset_obj)

                    for k in range(len_of_prev_subset):
                    
                        kth_tuple_in_prev_subset=prev_subset_obj[k]
                        
                        r_of_kth_tuple_in_prev_subset = kth_tuple_in_prev_subset[0]
                        c_of_kth_tuple_in_prev_subset = kth_tuple_in_prev_subset[1]


                        R, C =  round(r_of_kth_tuple_in_prev_subset*r_of_curr_item,ROUND_N_PLACES), c_of_kth_tuple_in_prev_subset+c_of_curr_item 

                        c_of_curr_and_next_item= C if d+1==devices else C+c_i[d+1]

                        if c_of_curr_and_next_item<=c:
                            curr_subset[subset_name].append((R,C))

            merged_n_purged_subset = apply_dominance_rule(d=curr_subset)
            d_cleaned = del_dict_key_w_empty_val(d=merged_n_purged_subset)

            all_sets[curr_set_num] = d_cleaned
            
        return all_sets
    def copy_for_all_devices(devices:int,highest_r_rc_pair:tuple,all_main_sets:dict,all_subsets:dict):
        d = {}
        prev_rc_pair = highest_r_in_last_device
        copy = subset_of_rc_pair(rc_pair=highest_r_rc_pair,all_subsets=all_subsets)
        d[f"D{devices}"] = copy

        
        for i in range(devices-1,0,-1):
            index_of_prev_rc_pair = find_rc_pair_index_in_all_subsets(rc_pair=prev_rc_pair,all_subsets=all_subsets)
            next_rc_pair = all_main_sets[f"S^{i}"][index_of_prev_rc_pair]
            copy = subset_of_rc_pair(rc_pair=next_rc_pair,all_subsets=all_subsets)
            d[f"D{i}"]=copy
            prev_rc_pair = next_rc_pair
        return d
    
    D_i = [f"D_{i}" for i in range(1,devices+1)]
    U_i = find_upper_bound(c=c,cost=cost)

    table = create_table(devices+1,COLUMNS)

    table = replace_row(table=table,pos=1,value=HEADER_COLS)

    table = replace_col(table=table,pos=1,value=D_i,ignore_header=True)
    table = replace_col(table=table,pos=2,value=cost,ignore_header=True)
    table = replace_col(table=table,pos=3,value=reliability_list,ignore_header=True)
    table = replace_col(table=table,pos=4,value=U_i,ignore_header=True)

    c_i = extract_col(table=table,n=2,ignore_header=True)
    r_i = extract_col(table=table,n=3,ignore_header=True)
    u_i = extract_col(table=table,n=4,ignore_header=True)
    
    all_sets = get_rc_for_all_devices(devices=devices,c_i=c_i,r_i=r_i,u_i=u_i,starting_set=starting_set)
    all_main_sets = get_main_set_from_all_sets(all_sets=all_sets)
    all_subsets = get_subsets_only_from_all_sets(all_sets=all_sets)

    highest_r_in_last_device = max(rc_pairs_in_nth_main_set(n=devices,all_sets=all_sets))
    copies=copy_for_all_devices(devices=devices,highest_r_rc_pair=highest_r_in_last_device,all_main_sets=all_main_sets,all_subsets=all_subsets)

    return copies,highest_r_in_last_device


def find_upper_bound(c:int,cost:list):
    """ 
    1. The functions fills in the values for the column `U_i` in the table:
        D_i | C_i | r_i | U_i
        ____|_____|_____|____
    """
    def inputs_are_valid(**kwargs):
        """ 
        1. Parent function will not run unless `c` is at least equal to the sum of `cost`.
        """
        if kwargs["c"]>=sum(kwargs["cost"]):
            return True
        else:
            raise ValueError("`c` should not be lower than the summation of `cost`.")

    if inputs_are_valid(c=c,cost=cost):
        sum_of_cost = sum(cost)
        return [ ((c-sum_of_cost)//c_i)+1  for c_i in cost]
    

def create_table(rows:int,columns:int):
    """
    1. Create a list containing `row` amount of child lists with `columns` amount of `0`  
    2. Example: create_table(2,3) returns:
        [[0,0,0],[0,0,0]]
            ^        ^
            |        |
            row 1    row 2

    3. The table can also be interpreted as:
        row 1 -> [[0,0,0],
        row 2 -> [0,0,0]]
    """
    return [ [0*j for j in range(columns)] 
            for i in range(rows)]

def replace_row(table:list,pos:int,value:list):
    """
    1. Replaces `pos-1`th row from `table`. 
        1. `pos` is 1-indexed. 
    2. To replace a row is to overwrite previous data in `table[pos-1]`
    3. Example: replace_row(table=table,pos=1,value=[1,2,3]) returns:
        [[1,2,3],
        [0,0,0]]
    """
    try:
        table[pos-1] = value
    except IndexError as r:
        raise r(f"Row {pos} in {table} does not exist. Cannot complete action.")
    else:
        return table
def insert_row(table:list,pos:int,value:list):
    """
    1. Insert a list in table's `pos-1`th index. 
        1. `pos` is 1-indexed.
    2. Performs `table.insert(pos-1,value)`, and returns table.
    """
    table.insert(pos-1,value)
    return table
def replace_col(table:list,pos:int,value:list,ignore_header:bool):
    """
    1. Replaces `pos-1`th column in table with `value` (list). 
        1. `pos` is 1-indexed.
    2. Has an option to ignore header.
        Ignoring header means to slice table as table[1:] instead of table[:].
    """
    for row,new_val in zip(table[1:] if ignore_header else table[:],value):
        row[pos-1]=new_val
    return table
def extract_col(table:list,n:int,ignore_header:bool):
    """
    1. Get a list of elements in `n-1`th position of every child list (rows).
        1. `n` is 1-indexed.
    2. Has an option to ignore the first row (ignore_header:bool).
    3. Example: extract_col(table=table,n=1,ignore_header=True):
        1. if table =  [[1,2,3],
                    [4,5,6],
                    [7,8,9]]
        2. return: [4,7].
    """
    return [ row[n-1] for row in (table[1:] if ignore_header else table[:]) ]

def d_first_key_is_k(d:dict,k):
    """
    1. Returns True if `k` is the first key in dict `d`, else False.
    """
    return list(d.keys())[0]==k

def apply_dominance_rule(d:dict):
    """
    1. Return `d` with removed (R,C) valuwa that end up having lower R & higher C when merged.
    2. In Reliability Design, (R,C) values in the merged set (not Python `set()` objects) that have a lower R & higher C than the next pair are removed.
    3. This function sorts all (R,C) values in `d` (usually a dict of subsets) in ascending order, and pairs who meet the condition for removal are removed from `d`.
        1. Example inputs: 
            1. {'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)]}
            2. {'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
    4. Example:
        1. d = {'S^3_1': [(0.36, 65), (0.4464, 95)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
        2. all_pairs = [(0.36, 65), (0.4464, 95), (0.54, 85), (0.648, 100)]
        3. bad_pairs = [(0.4464, 95)]
        4. return: {'S^3_1': [(0.36, 65)], 'S^3_2': [(0.54, 85), (0.648, 100)]}.
                1. (0.4464, 95) is gone from S^3_1.
    5. Example 2:
        1. d = {'S^3_2': [(0.54, 85), (0.648, 100)], 'S^3_3': [(0.63, 105)]}
        2. all_pairs = [(0.54, 85), (0.63, 105), (0.648, 100)]
        3. bad_pairs = [(0.63, 105)]
        4. return: {'S^3_2': [(0.54, 85), (0.648, 100)], 'S^3_3': []}
            1. (0.63, 105) is gone, and the key S^3_3 is left a list with no elements.
    """
    def get_all_pairs_in_asc_r(d:dict):
        """
        1. Returns an ascending list of (R,C) value in `d`.
        2. Example: 
            1. If d = {'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)]}
            2. return: [(0.72, 45), (0.864, 60), (0.8928, 75)].
        """
        return sorted([rc_pair for subset in d.keys() for rc_pair in d[subset] ])
    
    def get_bad_pairs(asc_r_pairs:list):
        """
        1. Get a list of pairs in the ascending pairs list who have lower R & higher C than the next pair.
        2. Example:
            1. if asc_r_pairs = [(.56, 65), (0.432, 80), (0.4464, 95), (0.54, 85)]
            2. return: [(0.4464, 95)].
                This is because this pair has lower R & higher C than the next pair ((0.54, 85)).
        """
        bad_pairs = []

        for i in range(len(asc_r_pairs)):
            curr_pair=asc_r_pairs[i]
            prev_pair=(0,0) if i==0 else asc_r_pairs[i-1]

            curr_r=curr_pair[0]
            curr_c=curr_pair[1]

            prev_r=prev_pair[0]
            prev_c=0 if i==0 else prev_pair[1]
            
            if (prev_c>=curr_c) and (prev_r<=curr_r):
                bad_pairs.append(min(curr_pair,prev_pair))

        return bad_pairs   

    def remove_bpairs_from_d(d:dict,bad_pairs:list):
        """
        1. If a pair in `d` appears in the `bad_pairs` list, it is removed from `d`.
        2. The bad (R,C) value is also removed from the d[subset] & bad_pairs list. 
        3. Example:
            1. d = {'S^3_1': [(0.36, 65), (0.432, 80), (0.4464, 95)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
            2. bad_pairs = [(0.4464, 95)]
            3. return: {'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}.
                1. (0.4464, 95) is gone from S^3_1.
        """
        for subset in d.values():
            for rc_pair in subset[:]:
                if rc_pair in bad_pairs[:]:
                    subset.remove(rc_pair)
                    bad_pairs.remove(rc_pair)

        return d
    
    all_pairs = get_all_pairs_in_asc_r(d=d)
    bad_pairs = get_bad_pairs(asc_r_pairs=all_pairs)

    return remove_bpairs_from_d(d=d,bad_pairs=bad_pairs)

def del_dict_key_w_empty_val(d:dict):
        """
        1. Returns `d` with removed {k:v} pairs if v is empty.
            1. "Empty" means len(v)==0.
        2. Example:
            1. d = {1: [1], 2: []}
            2. return: {1: [1]}
                1. Since d[2] refers to an empty list, this pair is now removed.
        """
        for subset in d.copy().keys():
            if len(d.copy()[subset])==0:
                del d[subset]
        return d

def rc_pairs_in_nth_main_set(n:int,all_sets:dict):
    """
    1. Gets all the (R,C) values of a subset under the `n`th main set, and return all the collected pairs in a list.
    2. Example:
        1. n = 2
        2. all_sets = {
        'S^0': 
            {'S^0_0': 
                [(1, 0)]
            }, 
        'S^1': 
            {'S^1_1': 
                [(0.9, 30)], 
            'S^1_2': 
                [(0.99, 60)]
            }, 
        'S^2': 
            {'S^2_1': 
                [(0.72, 45), (0.792, 75)], 
            'S^2_2': 
                [(0.864, 60)]
            }
        }
        3. return: [(0.72, 45), (0.792, 75), (0.864, 60)].
            1. These values were under the subsets that belong to the second main set (`S^2`).
    """
    def inputs_are_valid(n:int, all_sets:dict):
        """
        1. Check if `n` is at most, equal to the `len(all_sets)-1`. 
            1. Returns True if True, else raise ValueError.
        """
        if n<=len(all_sets)-1:
            return True
        else:
            raise ValueError("`n` value cannot be equal to length of `all_sets`.")
        
    if inputs_are_valid(n=n, all_sets=all_sets):
        l=[]
        main_set_name=f"S^{n}"
        for subset in all_sets[main_set_name]:
            l+=all_sets[main_set_name][subset]
            
        return l

def get_subsets_only_from_all_sets(all_sets:dict):
    """
    STOPPED HERE
    1. Return a dict containing only subsets as keys & their respective (R,C) values.
    2. Example:
        1. all_sets = {'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}}
        2. return: {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}
            1. The main set S^1 has been removed, with only subsets remaining.
    """
    d = {}
    for main_set in all_sets.keys():
        for subset in all_sets[main_set]:
            d[subset]=all_sets[main_set][subset]

    # FIX
    for i in range(len(all_sets.keys())):
        pass

    return d

def get_main_set_from_all_sets(all_sets:dict):
    main_set = "S^"
    return {f"{main_set}{i}": rc_pairs_in_nth_main_set(n=i,all_sets=all_sets) for i in range(len(all_sets)) }

def main_set_of_rc_pair(rc_pair:tuple,all_main_sets:dict):
    for main_set in all_main_sets:
        if rc_pair in all_main_sets[main_set]:
            return int(main_set[-1])
        
def subset_of_rc_pair(rc_pair:tuple,all_subsets:dict):
    for subset in all_subsets:
        if rc_pair in all_subsets[subset]:
            return int(subset[-1])

def find_rc_pair_index_in_all_subsets(rc_pair:tuple,all_subsets:dict):
      for subset in all_subsets:
          if rc_pair in all_subsets[subset]:
              return all_subsets[subset].index(rc_pair)
          
def get_subsets_only_under_nth_main_set(n:int,all_sets:dict):
        d = {}
        main_set_name = f"S^{n}"
        for subset_key in all_sets[main_set_name]:
            d[subset_key]=all_sets[main_set_name][subset_key]

        return d
if __name__ == "__main__":
    main()