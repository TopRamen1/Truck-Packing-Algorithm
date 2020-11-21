from algorithm_data import DataFromFile
from algorithm_data import MainStorage
from algorithm import init_pop

if __name__ == '__main__':
    data = DataFromFile("data/data_test1_p.txt", "data/data_test1_t.txt", "data/data_test1_s.txt")

    storage = MainStorage(data)

    print(storage)

    pop = init_pop(storage, 3)





