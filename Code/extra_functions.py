"""Additional file to define auxiliary functions"""
from typing import List, Tuple, Dict
import random


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
    """Generate lists which tells you which genes to take from a particular parent"""

    rand_lst1 = []  # shows which part of divided chromosome stay from parent 1
    rand_lst2 = []  # shows which part of divided chromosome stay from parent 2
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
    """Generate divisors for every part of chromosome (ch_p), parts are the number of storages"""

    # list of list where every list has divisors of right side of chromosome: ch_p
    list_divisors: List[List[int]] = [[] for i in range(len(num_cross_points_))]

    for key, value in dict_of_used_p_s_.items():
        val1 = int(value / num_cross_points_[key])
        list_divisors[key].extend([val1] * num_cross_points_[key])
        if value % num_cross_points_[key] != 0:
            list_divisors[key].append(value % num_cross_points_[key])
    del val1

    return list_divisors


def cht_from_chp(list_of_trucks_: List, list_of_packages_: List, ch_p: List[int]) -> List[List[int]]:
    """Make left part of chromosome: ch_t from right part of chromosome: ch_p"""
    ch_t = [[-1] for i in range(len(list_of_trucks_))]  # empty truck's chromosome
    for index, gen in enumerate(ch_p):
        if ch_t[gen] == [-1]:
            ch_t[gen] = [list_of_packages_[index].address]
        else:
            if list_of_packages_[index].address not in ch_t[gen]:
                ch_t[gen].append(list_of_packages_[index].address)

    return ch_t


def get_position(dict_of_used_p_s_: Dict[int, int]) -> List[int]:
    pos = [0]
    for key, value in dict_of_used_p_s_.items():
        value = pos[key] + value
        pos.append(value)
    del value

    return pos


def get_counter(list_divisors_: List[List[int]]) -> List[int]:
    counter = [0]
    for i, j in enumerate(list_divisors_):
        value = len(j)
        value = counter[i] + value
        counter.append(value)
    del value

    return counter


def find_divisors(dict_of_pack_sto: Dict[int, int]) -> Dict[int, List[int]]:
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


