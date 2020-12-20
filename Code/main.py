from algorithm_data import DataFromFile, create_testfile
from algorithm_data import MainStorage
import algorithm as al
import algorithm_data as al_d
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # create_testfile(10, 10, [10, 1000], 4, [10, 1000])  # dla 5 magazynów 10 testów
    data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt", 2)
    storage = MainStorage(data)

    av_best_sols = np.zeros(21)

    best_sols = []
    av_sols_vec = []
    params = al_d.csv_reader("params/algorythm_data_test2.csv")

    j = 0
    while j < 100:
        # params :                                     data, its, pop, cross, mut , div_pts, debug, plot
        sol, best_sol_val, av_sol_val = al.genetic_alg(storage, 20, 50, 0.9, 0.1, [1, 2, 2], False, False, "param 1")

        # save best sols on every iteration
        best_sols.append(best_sol_val)
        #
        best_sol_val = np.array(best_sol_val)
        # add
        av_best_sols = av_best_sols + best_sol_val
        j += 1

    av_best_sols = av_best_sols / 100
    print("The best solution in every iteration: ", best_sols)
    std_der_best_sols = np.std(best_sols, ddof=1, axis=0)

    # 1 arg: number of data instance, 2 arg: number of data parameters, 3 and more args: dict
    al_d.csv_writer(1, 2, {" average best sol": av_sol_val}, {"num pop": params[0]})

    plt.scatter(range(len(av_best_sols)), av_best_sols, label='średnia')

    plt.scatter(range(len(std_der_best_sols)), av_best_sols - std_der_best_sols, label='średnia')
    plt.scatter(range(len(std_der_best_sols)), av_best_sols + std_der_best_sols, label='odch')
    plt.title("Średnia naj wartość {}".format(0))
    plt.ylabel("wartość")
    plt.xlabel("iteracje")
    plt.show()

    # sol_1, best_sols_1, av_sols_1 = al.genetic_alg(storage, 40, 100, 0.7, 0.05, [1, 2, 2], False, True, "param 1")
    #
    # sol2 = al.genetic_alg(storage, 40, 20, 0.5, 0.45, [1, 2, 2], False, True, "param 2")
    #
    # print('\n')
    #
    # for key, value in sol2.items():
    #     print(key, ' : ', value)
    #
