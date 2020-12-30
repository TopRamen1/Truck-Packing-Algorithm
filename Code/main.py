from algorithm_data import DataFromFile, create_testfile
from algorithm_data import MainStorage
import algorithm as al
import algorithm_data as al_d
import extra_functions as ex_fun
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
        while j < iter_alg:
            # Start timer
            start = time.time()

            # Main algorithm function
            it_best_sol, best_sol_val_in, av_sol_val_in = al.genetic_alg(storage, int(params[0][i]) - 1, int(params[1][i]),
                                                               float(params[2][i]), float(params[3][i]), [1, 2, 2],
                                                               False, False, "For data parameters: {}".format(i))
            elapsed = time.time() - start

            #temporary POTEM USUNAC
            p_to_t = al.print_sol(storage, it_best_sol)
            ex_fun.visualisation(storage, p_to_t)
            #############
            # Calculate sum of times
            av_time += elapsed

            best_sol_val_out.append(best_sol_val_in)
            av_sol_val_out.append(av_sol_val_in)

            if not best_sol.ch_t:
                best_sol = deepcopy(it_best_sol)

            if it_best_sol.obj_fcn < best_sol.obj_fcn:
                best_sol = deepcopy(it_best_sol)

            j += 1

        # Calculate av time
        av_time = av_time / j

        # Converting lists to arrays
        best_sol_m = np.array(best_sol_val_out)  # Matrix of best solution (rows: alg it. from params[0], cols: out it.)
        av_sol_m = np.array(av_sol_val_out)  # Matrix of average solution (rows: alg it. from params[0], cols: out it.)

        # Final vectors
        mean_best = np.mean(best_sol_m, axis=0)  # Vector of best average solution
        mean_av = np.mean(av_sol_m, axis=0)  # Vector of average of average solution

        al_d.csv_writer(1, i + 1, {"Average best solutions": mean_best}, {"Average of average solutions": mean_av},
                        {"P: Iteration": [params[0][i]]}, {"P: Population": [params[1][i]]},
                        {"P: Probability of crossing": [params[2][i]]}, {"P: Probability of mutation": [params[3][i]]},
                        {"P: No. crossing points": ["1,2,3"]}, {"Out: Average time": [av_time]})  # 1 arg: number of data instance, 2 arg: number of
        # Data parameters, 3 and more args: dict

        plt.plot(range(len(mean_best)), mean_best, label=f"{legend} = {float(params[param_num][i])}")

        print("Średni czas dla zestawu {} to: {}".format(i, av_time))

        al.print_sol(storage, best_sol)

        if i % len(params[0]) == len(params[0]) - 1:
            plt.title(title)
            plt.ylabel("wartość")
            plt.xlabel("iteracje")
            plt.legend()
            plt.show()


if __name__ == '__main__':
    data_dir_ = "data/instance1"  # Data file
    param_dir_ = "parameters/instance1.csv"  # Parameter file
    title_ = "zmienna populacja"  # Plot title
    legend_ = "populacja"  # Legend text
    param_num_ = 1  # Var for legend
    its_ = 1  # Number of iterations

    generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)

    # data = DataFromFile("data/instance1/p.txt", "data/instance1/t.txt", "data/instance1/s.txt", 2)
    # storage = MainStorage(data)
    #
    # sol, best_sol_val_in, av_sol_val_in = al.genetic_alg(storage, 30, 1000, 0.9, 0.2, [1, 2, 2], False, True, "For data parameters: {}".format(33))
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
    # its_ = 100
    #
    # generate_stats(data_dir_, param_dir_, its_, title_, legend_, param_num_)



    # data = DataFromFile("data/instance1/p.txt", "data/instance1/t.txt", "data/instance1/s.txt", 2)
    # storage = MainStorage(data)
    # params = al_d.csv_reader_param("parameters/instance1_mute.csv")
    #
    # """Main loop which start algorithm for every parameter for one, specific data instance"""
    # iter_alg = 100  # number of iteration (it's not iteration of algorithm) to average data
    # for i in range(len(params[0])):
    #     best_sol_val_out = []
    #     av_sol_val_out = []
    #     av_time = 0
    #
    #     j = 0
    #     while j < iter_alg:
    #
    #         # start timer
    #         start = time.time()
    #
    #         # main algoritm function
    #         _, best_sol_val_in, av_sol_val_in = al.genetic_alg(storage, int(params[0][i]) - 1, int(params[1][i]),
    #                                                            float(params[2][i]), float(params[3][i]), [1, 2, 2],
    #                                                            False, False, "For data parameters: {}".format(i))
    #         elapsed = time.time() - start
    #
    #         # calculate sum of times
    #         av_time += elapsed
    #
    #         best_sol_val_out.append(best_sol_val_in)
    #         av_sol_val_out.append(av_sol_val_in)
    #         j += 1
    #
    #     # calculate av time
    #     av_time = av_time / j
    #
    #     # Converting lists to arrays
    #     best_sol_m = np.array(best_sol_val_out)  # matrix of best solution (rows: alg it. from params[0], cols: out it.)
    #     av_sol_m = np.array(av_sol_val_out)  # matrix of average solution (rows: alg it. from params[0], cols: out it.)
    #
    #     # Final vectors
    #     mean_best = np.mean(best_sol_m, axis=0)  # vector of best average solution
    #     mean_av = np.mean(av_sol_m, axis=0)  # vector of average of average solution
    #
    #     al_d.csv_writer(1, i + 1, {"Average best solutions": mean_best}, {"Average of average solutions": mean_av},
    #                     {"P: Iteration": [params[0][i]]}, {"P: Population": [params[1][i]]},
    #                     {"P: Probability of crossing": [params[2][i]]}, {"P: Probability of mutation": [params[3][i]]},
    #                     {"P: No. crossing points": ["1,2,3"]})  # 1 arg: number of data instance, 2 arg: number of
    #     # data parameters, 3 and more args: dict
    #
    #     plt.plot(range(len(mean_best)), mean_best, label="Pr mutacji = {}".format(float(params[3][i])))
    #
    #     print("Średni czas dla zestawu {} to: {}".format(i, av_time))
    #
    #     if i % len(params[0]) == len(params[0]) - 1:
    #         plt.title("Wyniki dla zmiennego prawdopodobieństwa mutacji")
    #         plt.ylabel("wartość")
    #         plt.xlabel("iteracje")
    #         plt.legend()
    #         plt.show()

        # std_der_best_sol = np.std(best_sol_m, ddof=1, axis=0)
        # plt.scatter(range(len(mean_best)), mean_best - std_der_best_sol, label='średnia')
        # plt.scatter(range(len(mean_best)), mean_best + std_der_best_sol, label='odch')
        # plt.title("Średnia naj wartość zestaw: {}".format(i))
        # plt.ylabel("wartość")
        # plt.xlabel("iteracje")

    # plt.title("Średnia naj wartość zestaw: {}".format(i))
    # plt.ylabel("wartość")
    # plt.xlabel("iteracje")
    # plt.legend()
    # plt.show()

    # print(len(best_sols), len(best_sol_val), len(av_best_sols))
    # av_best_sols = av_best_sols / iter_alg
    # print("The best solution in every iteration: ", best_sols)
    # std_der_best_sols = np.std(best_sols, ddof=1, axis=0)

    # plt.scatter(range(len(av_best_sols)), av_best_sols, label='średnia')
    #
    # plt.scatter(range(len(std_der_best_sols)), av_best_sols - std_der_best_sols, label='średnia')
    # plt.scatter(range(len(std_der_best_sols)), av_best_sols + std_der_best_sols, label='odch')
    # plt.title("Średnia naj wartość {}".format(0))
    # plt.ylabel("wartość")
    # plt.xlabel("iteracje")
    # plt.show()
