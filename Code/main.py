from algorithm_data import DataFromFile, create_testfile
from algorithm_data import MainStorage
import algorithm as al

if __name__ == '__main__':
    #create_testfile(10, 5)  # dla 5 magazynów 10 testów
    data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt", 2)
    storage = MainStorage(data)

    # params :            data, its, pop, cross, mut , div_pts, debug, plot
    sol1 = al.genetic_alg(storage, 40, 100, 0.7, 0.05, [1, 2, 2], False, True, "param 1")

    sol2 = al.genetic_alg(storage, 40, 20, 0.5, 0.45, [1, 2, 2], False, True, "param 2")


    for key, value in sol1.items():
        print(key, ' : ', value)

    print('\n')

    for key, value in sol2.items():
        print(key, ' : ', value)

