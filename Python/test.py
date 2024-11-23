def get_subsets_only_from_all_sets(all_sets:dict):
    """
    STOPPED HERE
    1. Return a dict containing only subsets as keys & their respective (R,C) values.
    2. Example:
        1. all_sets = {'S^0': {'S^0_0': [(1, 0)]}, 'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}}
        2. return: {S^0_0: [(1, 0)], 'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}
            1. The main sets S^0 and S^1 have been removed, with only subsets remaining.
    """
    d = {}
    for main_set in all_sets.keys():
        for subset in all_sets[main_set]:
            d[subset]=all_sets[main_set][subset]

 

    return d



all_sets = {'S^0': {'S^0_0': [(1, 0)]}, 'S^1': {'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}, 'S^2': {'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)]}, 'S^3': {'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}}
all_main_sets = {'S^0': [(1, 0)], 'S^1': [(0.9, 30), (0.99, 60)], 'S^2': [(0.72, 45), (0.864, 60), (0.8928, 75)], 'S^3': [(0.36, 65), (0.432, 80), (0.54, 85), (0.648, 100)]}
all_subsets = {'S^0_0': [(1, 0)], 'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)], 'S^2_1': [(0.72, 45)], 'S^2_2': [(0.864, 60)], 'S^2_3': [(0.8928, 75)], 'S^3_1': [(0.36, 65), (0.432, 80)], 'S^3_2': [(0.54, 85), (0.648, 100)]}
                                                
d = {'S^2_1': [(0.72, 45), (0.6792, 75)], 'S^2_2': [(0.464, 60)], 'S^2_3': [(0.8928, 75)]}
a = [(0.72, 45), (0.5792, 75), (0.864, 60), (0.8928, 75)]

highest_r_in_last_device = (0.648, 100)
devices = 3

d = {'S^0_0': [(1, 0)]}
d2={'S^1_1': [(0.9, 30)], 'S^1_2': [(0.99, 60)]}


out = get_subsets_only_from_all_sets(all_sets=all_sets)
print(out)

