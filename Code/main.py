from algorithm_data import DataFromFile, create_testfile
from algorithm_data import MainStorage
import algorithm as al
import algorithm_data as al_d
import matplotlib.pyplot as plt
import numpy as np
import time
from copy import deepcopy


def generate_stats(data_dir: str, param_dir: str, its: int, title, legend, param_num):
    data = DataFromFile(f"{data_dir}/p.txt", f"{data_dir}/t.txt", f"{data_dir}/s.txt", 2)
    storage = MainStorage(data)
    params = al_d.csv_reader_param(param_dir)

    """Main loop which start algorithm for every parameter for one, specific data instance"""
    iter_alg = its  # number of iteration (it's not iteration of algorithm) to average data
    for i in range(len(params[0])):
        best_sol_val_out = []
        av_sol_val_out = []
        av_time = 0
        best_sol = al.Individual([], [])

        j = 0

        div = []
        for e in enumerate(storage.list_of_storages):
            div.append(1)

        print(div)

        while j < iter_alg:
            # start timer
            start = time.time()

            # main algoritm function
            it_best_sol, best_sol_val_in, av_sol_val_in = al.genetic_alg(storage, int(params[0][i]) - 1, int(params[1][i]),
                                                               float(params[2][i]), float(params[3][i]), div,
                                                               False, False, "For data parameters: {}".format(i))
            elapsed = time.time() - start

            # calculate sum of times
            av_time += elapsed

            best_sol_val_out.append(best_sol_val_in)
            av_sol_val_out.append(av_sol_val_in)

            if not best_sol.ch_t:
                best_sol = deepcopy(it_best_sol)

            if it_best_sol.obj_fcn < best_sol.obj_fcn:
                best_sol = deepcopy(it_best_sol)

            print(j)
            j += 1

        # calculate av time
        av_time = av_time / j

        # Converting lists to arrays
        best_sol_m = np.array(best_sol_val_out)  # matrix of best solution (rows: alg it. from params[0], cols: out it.)
        av_sol_m = np.array(av_sol_val_out)  # matrix of average solution (rows: alg it. from params[0], cols: out it.)

        # Final vectors
        mean_best = np.mean(best_sol_m, axis=0)  # vector of best average solution
        mean_av = np.mean(av_sol_m, axis=0)  # vector of average of average solution

        al_d.csv_writer(1, i + 1, {"Average best solutions": mean_best}, {"Average of average solutions": mean_av},
                        {"P: Iteration": [params[0][i]]}, {"P: Population": [params[1][i]]},
                        {"P: Probability of crossing": [params[2][i]]}, {"P: Probability of mutation": [params[3][i]]},
                        {"P: No. crossing points": ["1,2,3"]}, {"Out: Average time": [av_time]})  # 1 arg: number of data instance, 2 arg: number of
        # data parameters, 3 and more args: dict

        # label=f"{legend} = {float(params[param_num][i])}"
        plt.plot(range(len(mean_best)), mean_best)

        print("Średni czas dla zestawu {} to: {}".format(i, av_time))

        al.print_sol(storage, best_sol)

        if i % len(params[0]) == len(params[0]) - 1:
            plt.title(title)
            plt.ylabel("wartość")
            plt.xlabel("iteracje")
            plt.legend()
            plt.show()


if __name__ == '__main__':
    data_dir_ = "data/simple_instance"  # data file
    param_dir_ = "parameters/instance3.csv"  # parameter file
    title_ = "Średnie najlepsze wartości od iteracji"  # plot title
    legend_ = ""  # legend text
    param_num_ = 1  # var for legend
    its_ = 100 # num of iterations

    generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)

    # data = DataFromFile("data/instance1/p.txt", "data/instance1/t.txt", "data/instance1/s.txt", 2)
    # storage = MainStorage(data)
    #
    # sol, best_sol_val_in, av_sol_val_in = al.genetic_alg(storage, 30, 100, 0.9, 0.15, [1, 1, 1], False, True, "For data parameters: {}".format(33))
    #
    # print(sol.obj_fcn)
    # print(best_sol_val_in[-1])
    #
    # print(al.print_sol(storage, sol))

    """
    param for pop
    """
    # data_dir_ = "data/instance1"
    # param_dir_ = "parameters/instance1_pop.csv"
    # title_ = "zmienna populacja"
    # legend_ = "populacja"
    # param_num_ = 1
    # its_ = 50
    #
    # generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)


    """
    param for cross
    """
    # data_dir_ = "data/instance1"
    # param_dir_ = "parameters/instance1_cross.csv"
    # title_ = "zmienne prawdopodobieństwo krzyrzowania"
    # legend_ = "Pr cross"
    # param_num_ = 2
    # its_ = 10
    #
    # generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)

    """
    param for cross points
    """
    # data_dir_ = "data/instance1"
    # param_dir_ = "parameters/instance1_cross_pts.csv"
    # title_ = "Zmiana ilości punktów krzyżowania"
    # legend_ = "punkty krzyżowania"
    # param_num_ = 4
    # its_ = 20
    # generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)

