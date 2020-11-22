from algorithm_data import MainStorage
from typing import List
import random


class Individual:
    def __init__(self, ch_t: List[int], ch_p: List[int]):
        """
        Class Fields: two parts of chromosome
        ch_t - part dedicated to showing which truck goes where
        ch_p - part representing which package goes to which truck
        """

        self.ch_t = ch_t
        self.ch_p = ch_p

    def __str__(self):
        return str(self.ch_t) + ' ' + str(self.ch_p)

    def get_ch_len(self):
        return len(self.ch_t) + len(self.ch_p)


def genetic_alg(main_storage: MainStorage):
    """    """
    pass


# TODO: funkcja celu
def obj_fcn(data: MainStorage):
    return -1


# TODO: ograniczenia
def chcek_lims(data: MainStorage):
    return True


def random_chromosome(data: MainStorage):
    """ Generates a random Chromosome for individual """
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
    """
    population = []

    for i in range(0, pop_size):
        new_ch = random_chromosome(data)
        population.append(Individual(new_ch[0], new_ch[1]))

    return population


# TODO: Funkcja oceniająca osobniki (na podstawie funkcji celu)
def fitness(data: MainStorage):
    pass


def crossover(data: MainStorage):
    pass


def mutation(data: MainStorage):
    pass


# TODO: Wybiera na podstawie oceny osobniki do mutacji
def selection():
    pass


if __name__ == '__main__':
    pass
