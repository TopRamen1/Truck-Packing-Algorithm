"""Additional file to define auxiliary functions"""
from typing import List, Tuple, Dict
import random
from graphviz import Digraph


def flat_list(org_list_: List[List[int]]) -> List[int]:
    """Flattened function to do List from List of Lists"""

    flat_lst = []
    for sublist in org_list_:
        if isinstance(sublist, list):
            for item in sublist:
                flat_lst.append(item)
        else:
            flat_lst.append(sublist)

    return flat_lst


def ge_rand(list_divisors_: List[List[int]], num_cross_points_: List[int]) -> Tuple[List[List[int]], List[List[int]]]:
    """Generate lists which tells you which genes to take from a particular parent (used in function: crossover)"""

    rand_lst1 = []  # Shows which part of divided chromosome stay from parent 1
    rand_lst2 = []  # Shows which part of divided chromosome stay from parent 2
    for i, j in enumerate(list_divisors_):
        temp = random.sample(range(len(j)), int(num_cross_points_[i] / 2))
        rand_lst1.append(temp)
        temp2 = []
        for p, k in enumerate(j):
            if p not in temp:
                temp2.append(p)
        rand_lst2.append(temp2)
    del temp, temp2

    tup_of_rand_lst = (rand_lst1, rand_lst2)

    return tup_of_rand_lst


def ge_div(dict_of_used_p_s_: Dict[int, int], num_cross_points_: List[int]) -> List[List[int]]:
    """Generate divisors for every part of chromosome (ch_p), parts are the number of storages (used in function:
       crossover)"""

    # List of list where every list has divisors of right side of chromosome: ch_p
    list_divisors: List[List[int]] = [[] for i in range(len(num_cross_points_))]

    for key, value in dict_of_used_p_s_.items():
        val1 = int(value / num_cross_points_[key])
        list_divisors[key].extend([val1] * num_cross_points_[key])
        if value % num_cross_points_[key] != 0:
            list_divisors[key].append(value % num_cross_points_[key])
    del val1

    return list_divisors


def cht_from_chp(list_of_trucks_: List, list_of_packages_: List, ch_p: List[int]) -> List[List[int]]:
    """Make left part of chromosome: ch_t from right part of chromosome: ch_p (used in function: crossover)"""

    ch_t = [[-1] for i in range(len(list_of_trucks_))]  # empty truck's chromosome
    for index, gen in enumerate(ch_p):
        if ch_t[gen] == [-1]:
            ch_t[gen] = [list_of_packages_[index].address]
        else:
            if list_of_packages_[index].address not in ch_t[gen]:
                ch_t[gen].append(list_of_packages_[index].address)

    return ch_t


def get_position(dict_of_used_p_s_: Dict[int, int]) -> List[int]:
    """Functions needed for count position (used in function: crossover)"""

    pos = [0]
    for key, value in dict_of_used_p_s_.items():
        value = pos[key] + value
        pos.append(value)
    del value

    return pos


def get_counter(list_divisors_: List[List[int]]) -> List[int]:
    """Functions needed for count counter (used in function: crossover)"""

    counter = [0]
    for i, j in enumerate(list_divisors_):
        value = len(j)
        value = counter[i] + value
        counter.append(value)
    del value

    return counter


def find_divisors(dict_of_pack_sto: Dict[int, int]) -> Dict[int, List[int]]:
    """Generate divisors for outside user to avoid conflict (used in GUI.py), because divisors should be divisible by
       number of package which goes to one specific address (example: 15 packages to address: 1, possible divisors:
       [1,3,5,15])"""

    final_dict = {}
    for ind, item in dict_of_pack_sto.items():
        i = 1
        temp_list = []
        while i <= item:
            if item % i == 0:
                temp_list.append(i)
            i = i + 1
        final_dict[ind] = temp_list

    return final_dict


def visualisation(storage, p_to_t: Dict[int, List[int]]) -> None:
    """Generate .pdf and .txt with graph visualisation final result of working algorithm"""
    dict_st = storage.get_used_sto_pack  # dict of used storages and packages

    graph = Digraph(comment='Visualisation')
    graph.attr(label='Visualization of the algorithms work results')
    graph.attr(fontsize='20')

    # Main storage visualization
    graph.attr('node', shape='circle', style='filled', fillcolor='blue',
               fontcolor='black')

    graph.node('Main storage')

    # Storage visualization (nodes and edges)
    graph.attr('node', shape='circle', style='filled', fillcolor='lightblue2',
               fontcolor='black')

    for s in dict_st.keys():
        graph.node('Storage id. %d' % (s))
        graph.edge('Main storage', 'Storage id. %d' % (s),
                   label='Distance: %d km' % storage.list_of_storages[s].distance)

    # Truck visualisation (nodes and edges)
    counter_all_packages = 1
    for i, (t, p) in enumerate(p_to_t.items()):  # counter all trucks
        graph.attr('node', shape='box', style='filled', fillcolor='green',
                   fontcolor='black')
        temp_sum = 0
        for e in p:
            temp_sum += storage.list_of_packages[e].weight

        graph.node('truck%d' % i,
                   label=f'{i + 1}\nTruck id. {t}\nLoad: {storage.list_of_trucks[t].load}\nNumber of packages: {len(p)}'
                         f'\nSum of weights: {temp_sum}\n')

        # Package visualisation (nodes and edges)
        for pack in p:
            graph.attr('node', shape='box', style='filled', fillcolor='lightgreen',
                       fontcolor='black')
            graph.node('package%d' % counter_all_packages, label=f'{counter_all_packages}\nPackage id. {pack}\nWeight: '
                                                                 f'{storage.list_of_packages[pack].weight}')
            graph.edge('truck%d' % i, 'package%d' % counter_all_packages)
            counter_all_packages += 1

        graph.edge(f'Storage id. {storage.list_of_packages[p[0]].address}', 'truck%d' % i)

    graph.render("graph_visualisation")
    graph.view()
