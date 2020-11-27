from algorithm_data import MainStorage
from typing import List
import random


class Individual:
    """
    Class containing individual chromosome and rating
    """

    def __init__(self, ch_t: List[int], ch_p: List[int], prob: float = 0):
        """
        :param ch_t: part dedicated to showing which truck goes where
        :param ch_p: part representing which package goes to which truck
        :param prob: probability of choosing this individual
        """

        self.ch_t = ch_t
        self.ch_p = ch_p

        self.prob = prob

    def __str__(self):
        return str(self.ch_t) + ' ' + str(self.ch_p) + ' ' + str(self.prob)

    def get_ch_len(self):
        return len(self.ch_t) + len(self.ch_p)


def genetic_alg(data: MainStorage, it_num: int):
    """

    """
    pop = init_pop(data, 8)

    print_pop(pop, "Populacja po inicjalizacji:")

    pop = fitness(data, pop)

    pop = selection(data, pop)

    i = 0

    while i < it_num:
        pop = crossover(data, pop)

        pop = mutation(data, pop)

        print_pop(pop, "Populacja po ocenie:")

        pop = selection(data, pop)

        print_pop(pop, "Populacja po selekcji:")

        i += 1

    pass


def obj_fcn(data_mst: MainStorage, data_ind: Individual):
    act_truck_pos = [i for i, m in enumerate(data_ind.ch_t) if m != -1]  # truck's id who has defined storage
    act_package_pos = [j for j, p in enumerate(data_ind.ch_p)]  # package's id
    sum_1, sum_2, sum_3 = 0, 0, 0

    # sum_1:
    for i in act_truck_pos:
        sum_1 += data_mst.list_of_trucks[i].exp_cost

    # sum_2:
    for i in act_truck_pos:
        sum_2 += data_mst.list_of_storages[data_ind.ch_t[i]].distance * data_mst.k * \
                 data_mst.list_of_trucks[i].min_fuel_use

    # sum_3:
    for i in act_truck_pos:
        sum_packages = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_packages += data_mst.list_of_packages[j].weight
        sum_3 += data_mst.list_of_storages[data_ind.ch_t[i]].distance * data_mst.k * \
                 (data_mst.list_of_trucks[i].max_fuel_use - data_mst.list_of_trucks[i].min_fuel_use) * \
                 (sum_packages / data_mst.list_of_trucks[i].load)

    final_result = sum_1 + sum_2 + sum_3

    return final_result


class NewException:
    def __init__(self):
        pass

    def __str__(self):
        return "Przekroczono warunek ograniczający"

    @property
    def lim1(self):
        return 'Przekroczono pierwszy warunek'

    def lim2(self):
        return 'Przekroczono drugi warunek'

    def lim3(self):
        return 'Przekroczono trzeci warunek'

    def lim4(self):
        return 'Przekroczono czwarty warunek'


def check_lims(data_mst: MainStorage, data_ind: Individual):
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
        raise NewException.lim1

    """ Checking the second limit """
    for i in act_truck_pos:
        sum_weights = 0
        for j in act_package_pos:
            if i == data_ind.ch_p[j]:
                sum_weights += data_mst.list_of_packages[j].weight
        if sum_weights > data_mst.list_of_trucks[i].load:
            raise NewException.lim2

    """ Checking the third limit """
    for i in data_ind.ch_p:
        if i == -1:
            raise NewException.lim3


def random_chromosome(data: MainStorage):
    """
    Generates a random Chromosome for individual
    :return: random chromosome
    """
    # id lists for calculations
    storage_ids = list(range(0, len(data.list_of_storages)))
    truck_ids = list(range(0, len(data.list_of_trucks)))
    package_ids = list(range(0, len(data.list_of_packages)))

    # init chromosome
    ch_t = [-1] * len(data.list_of_trucks)
    ch_p = [-1] * len(data.list_of_packages)

    # sorted packages by address
    ids_by_address = [[] for i in range(len(storage_ids))]
    for p_id in package_ids:
        ids_by_address[data.list_of_packages[p_id].address].append(p_id)

    while package_ids:
        for p_to_add in ids_by_address:
            while p_to_add:
                if not truck_ids:
                    print("to many packages error")
                    return [0], [0]

                t = data.list_of_trucks[random.choice(truck_ids)]  # random truck
                truck_ids.remove(t.id)

                p = data.list_of_packages[random.choice(p_to_add)]  # random package

                ch_t[t.id] = p.address  # adding truck address to chromosome

                weight_sum = 0
                while t.load >= weight_sum + p.weight:
                    weight_sum += p.weight

                    ch_p[p.id] = t.id  # adding truck id for package in chromosome

                    package_ids.remove(p.id)
                    p_to_add.remove(p.id)

                    if p_to_add:
                        p = data.list_of_packages[random.choice(p_to_add)]
                    else:
                        break

    return ch_t, ch_p


def init_pop(data: MainStorage, pop_size: int) -> List[Individual]:
    """
    Initialize population
    Function witch initializes population and returns it as a list of Indivituals
    :return: random population
    """
    population = []

    for i in range(0, pop_size):
        new_ch = random_chromosome(data)
        population.append(Individual(new_ch[0], new_ch[1]))

    return population


def fitness(data: MainStorage, pop: List[Individual]):
    """
    Calculate probability for every individual using objective fcn
    :return: rated population
    """
    sum1 = 0
    sum2 = 0
    for i in pop:
        sum1 += obj_fcn(data, i)

    for i in pop:
        i.prob = obj_fcn(data, i) / sum1
        sum2 += i.prob

    return pop


def selection(data: MainStorage, pop: List[Individual]):
    """
    Select individuals based on probability calculated by fitness
    :return: population to reproduce
    """
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


# TODO: krzyżowanie - KAMIL
def crossover(data: MainStorage, pop: List[Individual], num_cross_points: List[int]) -> List[Individual]:
    print_pop(pop, "Population to crossover:")

    list_divisors: List[List] = [[] for i in range(len(num_cross_points))]  # list of list where every list has
    # divisors of right side of chromosome: ch_p
    dict_of_used_p_s = data.get_used_sto_pack
    print(dict_of_used_p_s)
    if len(num_cross_points) != len(dict_of_used_p_s):
        pass
        # TODO throw exception

    for key, value in dict_of_used_p_s.items():
        val1 = int(value / num_cross_points[key])
        list_divisors[key].extend([val1] * num_cross_points[key])
        if value % num_cross_points[key] != 0:
            list_divisors[key].append(value % num_cross_points[key])

    rand_lst1 = []  # shows which part of divided chromosome stay from parent 1
    rand_lst2 = []  # shows which part of divided chromosome stay from parent 2
    for i, j in enumerate(list_divisors):
        temp = random.sample(range(len(j)), int(num_cross_points[i] / 2))
        rand_lst1.append(temp)
        temp2 = []
        for p, k in enumerate(j):
            if p not in temp:
                temp2.append(p)
        rand_lst2.append(temp2)
    del temp, temp2

    empty_ch_p1 = []
    for i, j in enumerate(list_divisors):
        for p, k in enumerate(j):
            empty_ch_p1.append([] * k)
    print(empty_ch_p1)
    empty_ch_p2=empty_ch_p1[:]
    print(empty_ch_p2)

    print("lista diviosrs",list_divisors)
    print(rand_lst1)
    print(rand_lst2)

    pos=[0, 12, 14]
    cou=[0, 4, 6, 8]
    for num, it in enumerate(list_divisors):
        for i in rand_lst1[num]:
            pos_t = pos[num]
            empty_ch_p1[i+cou[num]] = pop[0].ch_p[(pos_t+(it[i]*i)):(pos_t+(it[i]*(i+1)))]
            empty_ch_p2[i+cou[num]] = pop[1].ch_p[(pos_t+(it[i]*i)):(pos_t+(it[i]*(i+1)))]

        for i in rand_lst2[num]:
            pos_t = pos[num]
            empty_ch_p1[i + cou[num]] = pop[1].ch_p[(pos_t + (it[i] * i)):(pos_t + (it[i] * (i + 1)))]
            empty_ch_p2[i+cou[num]] = pop[0].ch_p[(pos_t+(it[i]*i)):(pos_t+(it[i]*(i+1)))]

    print(empty_ch_p1)
    print(empty_ch_p2)


    # children = (Individual(ch_t, ch_p), Individual(ch_t, ch_p))

    return 0


# TODO: naprawa populacji - NICOLAS
def fix_pop(data: MainStorage, pop: List[Individual]):
    return pop


# TODO: Mutacja - WOJTEK
def mutation(data: MainStorage, pop: List[Individual]):
    return pop


def print_pop(pop: List[Individual], text: str):
    print(text)

    for i in pop:
        print(i)

    print('\n')


if __name__ == '__main__':
    pass
