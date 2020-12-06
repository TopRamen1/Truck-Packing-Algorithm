from algorithm_data import DataFromFile
from algorithm_data import MainStorage

from algorithm import init_pop, fitness, selection, print_pop, cross_pop, mutation, genetic_alg

if __name__ == '__main__':
    """
    data = DataFromFile("data/test1/p.txt", "data/test1/t.txt", "data/test1/s.txt")

    storage = MainStorage(data)

    print(storage)

    pop = init_pop(storage, 3)

    for i in pop:
        print(i)

    """

    """
        data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt", 2)
    storage = MainStorage(data)

    pop = init_pop(storage, 20)

    # print_pop(pop, "Populacja po inicjalizacji:")

    pop = fitness(storage, pop)

    print_pop(pop, "Populacja po ocenie:")

    pop = selection(storage, pop)

    print_pop(pop, "Populacja po selekcji:")

    pop = cross_pop(storage, pop, [2, 2, 2])

    print_pop(pop, "Population after cross:")

    # newest_pop = mutation(storage, pop)
    #
    # print_pop(newest_pop, "Population after mutation:")
    """

    data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt", 2)
    storage = MainStorage(data)


    genetic_alg(storage, 20, 100)










