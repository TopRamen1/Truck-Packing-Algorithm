from .algorithm_data import *
from typing import List
import random


class Individual:
    def __init__(self, ch_t: List[int] , ch_p: List[int]):
        """
        Class Fields: two parts of chromosome
        ch_t - part dedicated to showing which truck goes where
        ch_p - part representing which package goes to which truck
        """

        self.ch_t = ch_t
        self.ch_p = ch_p


def genetic_alg(main_storage: MainStorage):
    """    """
    pass

# TODO: ograniczenia i funkcja celu
def obj_fcn():
    return -1


def chcek_lims():
    return True



def random_chromosome(data: MainStorage):
    """ Generates a random Chromosome for individual """
    storage_ids = list(range(0, len(data.storage_list)))
    truck_ids = list(range(0, len(data.truck_list)))
    package_ids = list(range(0, len(data.package_list)))

    p_len = len(package_ids)
    weight_sum = 0

    ch_t = [-1] * len(data.truck_list)
    ch_p = [-1] * len(data.package_list)

    s = data.storage_list[random.choice(storage_ids)]
    ids_by_address = [[] * len(storage_ids)]

    # sorted packages by id
    for p_id in package_ids:
        ids_by_address[data.package_list[p_id].address].append(p_id)

    while package_ids:
        for p_to_add in ids_by_address:
            t = data.truck_list[random.choice(truck_ids)]  # random truck
            p = data.package_list[random.choice(p_to_add)]  # random package

            ch_t[t.id] = p.address

            weight_sum = 0

            while t.load >= weight_sum + p.weight:
                weight_sum += p.weight
                ch_p[p.id] = t.id

                package_ids.pop(p.id)
                p_to_add.pop(p.id)
                p = data.package_list[random.choice(p_to_add)]

    return ch_t, ch_p


def init_pop(data: MainStorage, pop_size: int) -> List[Individual]:
    """
    Initialize population
    Function witch initializes population and returns it as a list of Indivituals
    """
    population = []

    for i in range(0, pop_size):
        new_ch = random_chromosome(data)
        population.append(Individual(new_ch[0], new_ch[1]))

    return population


def fitness():
    pass


def crossover():
    pass


def mutation():
    pass


def selection():
    pass





