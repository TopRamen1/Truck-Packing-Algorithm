from algorithm_data import DataFromFile
from algorithm_data import MainStorage
import algorithm as al

if __name__ == '__main__':
    data = DataFromFile("data/test12/p.txt", "data/test12/t.txt", "data/test12/s.txt", 2)
    storage = MainStorage(data)

    sol = al.genetic_alg(storage, 20, 40, [1, 2, 2], False, False)

    print(sol)
