from algorithm_data import DataFromFile, create_testfile
from algorithm_data import MainStorage
import algorithm as al
import algorithm_data as al_d
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    data = DataFromFile("data/test2/p.txt", "data/test2/t.txt", "data/test2/s.txt", 2)
    storage = MainStorage(data)
    params = al_d.csv_reader("parameters/instance1_param1.csv")

    """Main loop which start algorithm for every parameter for one, specific data instance"""
    av_best_sols = np.zeros(21)
    best_sols = []
    av_sols_vec = []

    print(params)
    iter_alg = 10  # number of iteration (it's not iteration of algorithm) to average data
    for i in range(len(params[0])):
        j = 0
        while j < iter_alg:
            print(int(params[0][i]))
            sol, best_sol_val, av_sol_val = al.genetic_alg(storage, int(params[0][i]), 50, 0.9, 0.1, [1, 2, 2], False,
                                                           False, "param 1")

            # save best sols on every iteration
            best_sols.append(best_sol_val)
            #
            best_sol_val = np.array(best_sol_val)
            # add
            av_best_sols = av_best_sols + best_sol_val
            j += 1

        print(len(best_sols), len(best_sol_val), len(av_best_sols))
        av_best_sols = av_best_sols / iter_alg
        print("The best solution in every iteration: ", best_sols)
        std_der_best_sols = np.std(best_sols, ddof=1, axis=0)

        # 1 arg: number of data instance, 2 arg: number of data parameters, 3 and more args: dict
        al_d.csv_writer(1, i+1, {"Average best solutions": av_best_sols}, {"Average of average solutions": best_sol_val},
                        {"P: Iteration": [params[0][i]]}, {"P: No. crossing points": ["1,2,3"]})

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
