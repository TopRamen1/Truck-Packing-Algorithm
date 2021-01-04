from algorithm_data import *
import extra_functions as ex_fun
from typing import List, Tuple
import random
import matplotlib.pyplot as plt
from copy import deepcopy


class Individual:
    """Class containing individual chromosome and rating"""

    def __init__(self, ch_t_: List[int], ch_p_: List[int], prob_: float = 0):
        """
        :param ch_t_: part dedicated to showing which truck goes where
        :param ch_p_: part representing which package goes to which truck
        :param prob_: probability of choosing this individual
        """

        self.ch_t = ch_t_
        self.ch_p = ch_p_

        self.obj_fcn = 0
        self.prob = prob_

    def __str__(self):
        return str(self.ch_t) + ' ' + str(self.ch_p) + ' ' + str(self.prob) + ' ' + str(self.obj_fcn) + ' ' + \
               str(len(self.ch_p))


def genetic_alg(data: MainStorage, it_num: int, pop_size: int, cross: float, mut: float, div: List[int],
                debug: bool = False, plot: bool = False, desc: str = ""):
    """Implementation of genetic algorithm
    :return: printed solutions for each iteration and its plots"""

    av_sol_vec = []
    best_sol_vec = []

    pop = init_pop(data, pop_size)
    pop, best_sol, best_val, av_sol = fitness(data, pop)

    av_sol_vec.append(av_sol)
    best_sol_vec.append(best_sol.obj_fcn)

    pop = selection(data, pop)

    print_pop(pop, "Populacja po inicjalizacji:", debug)

    i = 1

    while i <= it_num:
        pop = cross_pop(data, pop, div, cross)

        pop = mutation(data, pop, mut)

        pop, it_best_sol, it_best_val, av_sol = fitness(data, pop)

        if it_best_sol.obj_fcn < best_sol.obj_fcn:
            best_sol = deepcopy(it_best_sol)

        av_sol_vec.append(av_sol)
        best_sol_vec.append(best_sol.obj_fcn)

        pop = selection(data, pop)

        print_pop(pop, "Populacja po iteracji: {}".format(i), debug)

        i += 1

    if plot:
        plt.plot(range(len(av_sol_vec)), av_sol_vec, label='średnia')
        plt.title("Średnia wartość funkcji celu dla {}".format(desc))
        plt.ylabel("wartość")
        plt.xlabel("iteracje")
        plt.show()
        plt.plot(range(len(best_sol_vec)), best_sol_vec, label='rozwiązania')
        plt.title("Wartość najlepszego rozwiązania {}".format(desc))
        plt.ylabel("wartość")
        plt.xlabel("iteracje")
        plt.show()

    return best_sol, best_sol_vec, av_sol_vec


def print_sol(data: MainStorage, best_sol):
    """Prints best solution"""

    p_to_t = {}

    for i in range(0, len(best_sol.ch_p)):
        if best_sol.ch_p[i] in p_to_t.keys():
            p_to_t[best_sol.ch_p[i]].append(i)
        else:
            p_to_t[best_sol.ch_p[i]] = [i]

    print("Koszt: ", best_sol.obj_fcn)
    address = -1

    for k, v in p_to_t.items():
        sum = 0
        for e in v:
            sum += data.list_of_packages[e].weight

        if address != data.list_of_packages[v[0]].address:
            address = data.list_of_packages[v[0]].address
            print(f"\nMagazyn: {address}:")

        print("Ciezarowka: ", data.list_of_trucks[k].load, ", paczki: ", v, " suma wag: ", sum)

    return p_to_t


def obj_fcn(data_mst: MainStorage, data_ind: Individual) -> float:
    """Calculate function which describes our problem
       :return: value of above function"""

    act_truck_pos = [i for i, m in enumerate(data_ind.ch_t) if m != -1]  # truck's id who has defined storage
    act_package_pos = [j for j, p in enumerate(data_ind.ch_p)]  # package's id
    sum_1, sum_2, sum_3 = 0, 0, 0

    # Sum_1:
    for i in act_truck_pos:
        sum_1 += data_mst.list_of_trucks[i].exp_cost

    # Sum_2:
    for i in act_truck_pos:
        sum_2 += data_mst.list_of_storages[data_ind.ch_t[i]].distance / 100 * data_mst.k * \
                 data_mst.list_of_trucks[i].min_fuel_use

    # Sum_3:
    for i in act_truck_pos:
        sum_packages = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_packages += data_mst.list_of_packages[j].weight
        sum_3 += data_mst.list_of_storages[data_ind.ch_t[i]].distance / 100 * data_mst.k * \
                 (data_mst.list_of_trucks[i].max_fuel_use - data_mst.list_of_trucks[i].min_fuel_use) * \
                 (sum_packages / data_mst.list_of_trucks[i].load)

    final_result = sum_1 + sum_2 + sum_3

    return final_result


class Exception1(Exception):
    def __init__(self, message="Przekroczono pierwszy warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


class Exception2(Exception):
    def __init__(self, message="Przekroczono drugi warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


class Exception3(Exception):
    def __init__(self, message="Przekroczono trzeci warunek ograniczający"):
        self.message = message
        super().__init__(self.message)


def check_lims(data_mst: MainStorage, data_ind: Individual):
    """Checks limits and raises exceptions"""

    act_package_pos = [j for j, p in enumerate(data_ind.ch_p)]
    act_truck_pos = [i for i, m in enumerate(data_ind.ch_t) if m != -1]
    sum_weights = 0

    """ Checking the first limit """
    for i in data_mst.list_of_packages:
        sum_weights += i.weight
    sum_loads = 0
    for j in data_mst.list_of_trucks:
        sum_loads += j.load
    if sum_weights > sum_loads:
        raise Exception1

    """ Checking the second limit """
    for i in act_truck_pos:
        sum_weights = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_weights += data_mst.list_of_packages[j].weight
        if sum_weights > data_mst.list_of_trucks[i].load:
            raise Exception2

    """ Checking the third limit """
    for i in data_ind.ch_p:
        if i == -1:
            raise Exception3


def random_chromosome(data: MainStorage):
    """Generates a random Chromosome for individual
    :return: random chromosome"""

    # Id lists for calculations
    storage_ids = list(range(0, len(data.list_of_storages)))
    truck_ids = list(range(0, len(data.list_of_trucks)))
    package_ids = list(range(0, len(data.list_of_packages)))

    # Init chromosome
    ch_t = [-1] * len(data.list_of_trucks)
    ch_p = [-1] * len(data.list_of_packages)

    # Sorted packages by address
    ids_by_address = [[] for i in range(len(storage_ids))]
    for p_id in package_ids:
        ids_by_address[data.list_of_packages[p_id].address].append(p_id)

    while package_ids:
        for p_to_add in ids_by_address:
            while p_to_add:
                if not truck_ids:
                    print("to many packages error")
                    return [0], [0]

                t = data.list_of_trucks[random.choice(truck_ids)]  # Random truck
                truck_ids.remove(t.id)

                p = data.list_of_packages[random.choice(p_to_add)]  # Random package

                ch_t[t.id] = p.address  # Adding truck address to chromosome

                weight_sum = 0
                while t.load >= weight_sum + p.weight:
                    weight_sum += p.weight

                    ch_p[p.id] = t.id  # Adding truck id for package in chromosome

                    package_ids.remove(p.id)
                    p_to_add.remove(p.id)

                    if p_to_add:
                        p = data.list_of_packages[random.choice(p_to_add)]
                    else:
                        break

    return ch_t, ch_p


def init_pop(data: MainStorage, pop_size: int) -> List[Individual]:
    """Function witch initializes population and returns it as a list of Individuals
    :return: random population"""

    population = []
    for i in range(0, pop_size):
        new_ch = random_chromosome(data)
        population.append(Individual(new_ch[0], new_ch[1]))
    return population


def fitness(data: MainStorage, pop: List[Individual]):
    """Calculate probability for every individual using objective fcn
       :return: rated population"""

    sum1 = 0
    sum3 = 0
    obj_fcn_vals = []
    for i in range(len(pop)):
        val = obj_fcn(data, pop[i])
        sum3 += val
        obj_fcn_vals.append((i, val))
        sum1 += i + 1

    obj_fcn_vals.sort(key=lambda e: e[1])
    av_sol = sum3 / len(obj_fcn_vals)

    sum2 = 0
    j = len(obj_fcn_vals)
    for i, val in obj_fcn_vals:
        pop[i].prob = j / sum1
        pop[i].obj_fcn = val
        sum2 += j / sum1
        j -= 1

    best_sol = deepcopy(pop[obj_fcn_vals[0][0]])
    best_val = best_sol.obj_fcn

    return pop, best_sol, best_val, av_sol


def selection(data: MainStorage, pop: List[Individual]):
    """Select individuals based on probability calculated by fitness
    :return: population to reproduce"""

    new_pop = []
    while len(new_pop) < len(pop):
        r = random.random()
        prob = 0
        for i in pop:
            prob += i.prob
            if prob > r:
                new_pop.append(i)
                break

    return new_pop


def crossover(data: MainStorage, ind1: Individual, ind2: Individual, num_cross_points: List[int]) -> \
        Tuple[Individual, Individual]:
    """Crossing specific parts of chromosome according to crossing points
       :param data: class object - MainStorage
       :param ind1: one of the parents who will be crossing with the other parent
       :param ind2: second one of the parents
       :param num_cross_points: number of crossing points (example:list [1,3,2] tells us that first element (gen) of one
                                parent part of chromosome (ch_p) will change places with the other parent, then 3 next
                                gens in ch_p in one parent will change places with 3 next gens in second parent, etc.)
       :return: children (new individual who is the part of the new population)"""

    pop = [ind1, ind2]
    # Dict of number of used storages and number of individual packages in used storages
    dict_of_used_p_s = data.get_used_sto_pack

    # Generate divisors for every part of chromosome (ch_p), parts are the number of storages
    list_divisors = ex_fun.ge_div(dict_of_used_p_s, num_cross_points)

    # Generate List of empty Lists
    ch_p1 = []  # empty package's chromosome
    for i, j in enumerate(list_divisors):
        for p, k in enumerate(j):
            ch_p1.append([] * k)
    ch_p2 = ch_p1[:]

    # Generate lists which tells you which genes to take from a particular parent
    rand_lst1, rand_lst2 = ex_fun.ge_rand(list_divisors, num_cross_points)

    # Generate start position of each part of package(split based on address) and number of cuts of chromosome(crossing)
    pos = ex_fun.get_position(dict_of_used_p_s)
    counter = ex_fun.get_counter(list_divisors)

    # Gain algorithm for crossover: generate children from chromosome of individual parents
    for num, it in enumerate(list_divisors):
        for i in rand_lst1[num]:
            pos_t = pos[num]
            ch_p1[i + counter[num]] = pop[0].ch_p[(pos_t + (it[i] * i)):(pos_t + (it[i] * (i + 1)))]
            ch_p2[i + counter[num]] = pop[1].ch_p[(pos_t + (it[i] * i)):(pos_t + (it[i] * (i + 1)))]

        for i in rand_lst2[num]:
            pos_t = pos[num]
            ch_p1[i + counter[num]] = pop[1].ch_p[(pos_t + (it[i] * i)):(pos_t + (it[i] * (i + 1)))]
            ch_p2[i + counter[num]] = pop[0].ch_p[(pos_t + (it[i] * i)):(pos_t + (it[i] * (i + 1)))]

    # Flattened function to do List from List of Lists
    ch_p1 = ex_fun.flat_list(ch_p1)
    ch_p2 = ex_fun.flat_list(ch_p2)

    # Make left part of chromosome: ch_t from right part of chromosome: ch_p
    ch_t1 = ex_fun.cht_from_chp(data.list_of_trucks, data.list_of_packages, ch_p1)
    ch_t2 = ex_fun.cht_from_chp(data.list_of_trucks, data.list_of_packages, ch_p2)

    # Fix all genes where occurs conflict
    ch_t1, ch_p1 = fix_ind(ch_t1, ch_p1, data)
    ch_t2, ch_p2 = fix_ind(ch_t2, ch_p2, data)

    children = (Individual(ch_t1, ch_p1), Individual(ch_t2, ch_p2))

    return children


def cross_pop(data: MainStorage, pop: List[Individual], num_cross_points: List[int], cross_factor: float):
    """Crossing children with old population
    :return: new population"""

    i = 0
    new_pop = []
    while i < len(pop) * cross_factor:
        p1 = crossover(data, pop[i], pop[i + 1], num_cross_points)
        new_pop.append(p1[0])
        new_pop.append(p1[1])
        i += 2
    while len(new_pop) < len(pop):
        r = random.random()
        prob = 0
        for i in pop:
            prob += i.prob
            if prob > r:
                new_pop.append(i)
                break
    return new_pop


def fix_ind(ch_t: List[List[int]], ch_p: List[int], data: MainStorage):
    """Fixes gens in chromosome ch_t
    :return: modified chromosomes with no doubled addresses"""

    # Remove double addresses
    for t_id in range(len(ch_t)):
        if len(ch_t[t_id]) > 1:
            a = random.choice(ch_t[t_id])
            ch_t[t_id] = [a]
            for p_id in range(len(ch_p)):
                if ch_p[p_id] == t_id and data.list_of_packages[p_id].address != a:
                    ch_p[p_id] = -1

    ch_t = ex_fun.flat_list(ch_t)

    # Compute cargo weights
    cargo_w = [] * len(ch_t)

    for t_id in range(len(ch_t)):
        w_sum = 0
        for p_id in range(len(ch_p)):
            if ch_p[p_id] == t_id:
                w_sum += data.list_of_packages[p_id].weight

        cargo_w.append(w_sum)

    # Remove packages from trucks if they are overloaded
    for t_id in range(len(ch_t)):
        if cargo_w[t_id] > data.list_of_trucks[t_id].load:
            p_to_truck = []
            for p_id in range(len(ch_p)):
                if ch_p[p_id] == t_id:
                    p_to_truck.append(p_id)

            while cargo_w[t_id] > data.list_of_trucks[t_id].load:
                # remove random package
                p_id = random.choice(p_to_truck)
                p_to_truck.remove(p_id)
                ch_p[p_id] = -1
                cargo_w[t_id] -= data.list_of_packages[p_id].weight

    # Put all packages to place
    for p_id in range(len(ch_p)):
        if ch_p[p_id] == -1:
            p = data.list_of_packages[p_id]

            for t_id in range(len(ch_t)):
                if ch_t[t_id] == p.address:
                    w_sum = 0
                    for p1_id in range(len(ch_p)):
                        if ch_p[p1_id] == t_id:
                            w_sum += data.list_of_packages[p1_id].weight

                    if data.list_of_trucks[t_id].load >= w_sum + p.weight:
                        ch_p[p_id] = t_id
                        break

            if ch_p[p_id] == -1:
                free_trucks = []
                for t_id in range(len(ch_t)):
                    if ch_t[t_id] == -1:
                        free_trucks.append(t_id)

                t_id = random.choice(free_trucks)
                ch_p[p_id] = t_id
                ch_t[t_id] = data.list_of_packages[p_id].address

    return ch_t, ch_p


def mutation(data: MainStorage, pop: List[Individual], mutation_factor: float) -> List[Individual]:
    """Mutates random gens with probability
    :return: population with small percentage of mutated individuals"""

    random_ind = []
    duplications = []
    probability = len(pop) * mutation_factor

    # Choose random individuals with probability
    while len(random_ind) < probability:
        for i in range(int(probability)):
            x = random.choice(range(0, len(pop), 1))
            if x not in duplications:
                random_ind.append(x)
                duplications.append(x)
            if len(random_ind) == probability:
                break

    ch_t_list = mutation_helper(pop, random_ind)

    # Mutate random gen in chromosome ch_p
    for id, i in enumerate(pop):
        for id2, j in enumerate(random_ind):
            if id == j:
                new_ch_p = i.ch_p.copy()
                gen_x = random.choice(range(0, len(data.list_of_packages), 1))
                x = random.choice(range(0, len(data.list_of_trucks), 1))
                new_ch_p[gen_x] = x
                ch_t_list[id2][x].append(data.list_of_packages[gen_x].address)
                i.ch_t, i.ch_p = fix_ind(ch_t_list[id2], new_ch_p, data)
    return pop


def mutation_helper(pop: List[Individual], random_ind: List[int]) -> List[List[List[int]]]:
    """Helper function"""

    new_ch_t = []
    for id, i in enumerate(pop):
        for j in random_ind:
            if id == j:
                help_list = []
                for e in i.ch_t:
                    help_list.append([e])
                new_ch_t.append(help_list)
    return new_ch_t


def print_pop(pop: List[Individual], text: str, p: bool):
    """Prints population"""

    if p:
        print(text)
        j = 0
        for i in pop:
            print(j, i)
            j += 1
        print('\n')
