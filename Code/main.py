from algorithm_data import DataFromFile
from algorithm_data import MainStorage
from algorithm import init_pop

if __name__ == '__main__':

    """
    data = DataFromFile("data/test1/p.txt", "data/test1/t.txt", "data/test1/s.txt")

    storage = MainStorage(data)

    print(storage)

    pop = init_pop(storage, 3)

    for i in pop:
        print(i)

    """
    data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt")

    storage = MainStorage(data)

    print(storage)

    pop = init_pop(storage, 3)

    for i in pop:
        print(i)









