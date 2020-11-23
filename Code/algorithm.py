from algorithm_data import MainStorage
from typing import List
import random


class Individual:
    def __init__(self, ch_t: List[int], ch_p: List[int], p: float = 0):
        """
        Calss containing individual chromosome and rating
        :param ch_t: part dedicated to showing which truck goes where
        :param ch_p: part representing which package goes to which truck
        :param p: probability of choosing this individual
        """

        self.ch_t = ch_t
        self.ch_p = ch_p

        self.p = p

    def __str__(self):
        return str(self.ch_t) + ' ' + str(self.ch_p) + ' ' + str(self.p)

    def get_ch_len(self):
        return len(self.ch_t) + len(self.ch_p)


def genetic_alg(main_storage: MainStorage):
    """    """
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

                    ch_p[p.id] = t.id   # adding truck id for package in chromosome

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
        i.p = obj_fcn(data, i) / sum1
        sum2 += i.p

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
            prob += i.p
            if prob > r:
                new_pop.append(i)
                break

    return new_pop

# TODO: krzyżowanie
def crossover(data: MainStorage):
    pass


# TODO: Mutacja
def mutation(data: MainStorage):
    pass


def print_pop(pop: List[Individual], text: str):
    print(text)

    for i in pop:
        print(i)

    print('\n')


if __name__ == '__main__':
    pass
