from algorithm_data import DataFromFile
from algorithm_data import MainStorage
import algorithm as al
import extra_functions as ex_fun
from tkinter import *
from tkinter.font import Font

if __name__ == '__main__':
    root = Tk()
    root.title("Truck Packing Algorithm GUI")
    root.geometry("1000x400")
    label1 = Label(root, text="\nEnter the data for the algorithm to work...")
    label1.pack()

    #  Variables to storage necessary information about algorithm from Enter function
    name_test_num = StringVar()
    name_num_it = StringVar()
    name_pop_it = StringVar()
    name_div = StringVar()

    data, storage, d, = None, None, None  # d is a dictionary of used storages and packages
    iter_al, pop_al, cross_al = None, None, None  # variables to regular working algorithm
    logic_val1, logic_val2, logic_val3, logic_val4 = False, False, False, False  # all should be True to start algorithm


    def submit1():
        """Command responsible for read data file (.txt)"""
        global data, storage, d, logic_val1
        ind = name_test_num.get()
        if ind.isnumeric():
            #  Display small window in NE position to represent information about number of storages and packages part 1
            root2 = Tk()
            root2.title("List of used packages and storages")
            root2.geometry("300x200+1005+0")
            Label(root, text=f"\tConfirmation: Your data set is: test{ind}.txt\t\t\t").place(x=560, y=80)

            data = DataFromFile(f"data/test{ind}/p.txt", f"data/test{ind}/t.txt", f"data/test{ind}/s.txt", int(ind))
            storage = MainStorage(data)
            d = storage.get_used_sto_pack

            it = 10
            for i, j in d.items():
                Label(root2, text=f"Number of packages to storage no. {i}:\t{j}").place(x=10, y=it)
                it += 20
            logic_val1 = True
        else:
            Label(root, text="Enter correct data, the name should be a number\t").place(x=600, y=80)


    def submit2():
        """Command responsible for number of algorithm iteration"""
        global logic_val2, iter_al
        ind = name_num_it.get()
        if ind.isnumeric():
            Label(root, text=f"Confirmation: Number of algorithm iteration is: {ind}\t\t\t\t").place(x=600, y=117.5)
            logic_val2 = True
            iter_al = ind
        else:
            Label(root, text="Enter correct data, the name should be a number\t").place(x=600, y=117.5)


    def submit3():
        """Command responsible for number of population in algorithm"""
        global logic_val3, pop_al
        ind = name_pop_it.get()
        if ind.isnumeric():
            Label(root, text=f"\tConfirmation: Number of population is: {ind}\t\t\t").place(x=580, y=160)
            logic_val3 = True
            pop_al = ind
        else:
            Label(root, text="\tEnter correct data, the name should be a number\t").place(x=550, y=160)


    def submit4():
        """Command responsible for number of number of cuts in algorithm"""
        global logic_val4, cross_al
        ind = name_div.get()

        dict_of_cuts = ex_fun.find_divisors(d)
        data_temp = ind.strip()
        temp = data_temp.split(',')
        checking_list = []
        for i in temp:
            checking_list.append(int(i))
        if len(checking_list) < len(d):
            Label(root, text=f"\t\tToo low number of cuts\t\t\t\t\t").place(x=550, y=210)
        elif len(checking_list) > len(d):
            Label(root, text=f"\t\tToo much number of cuts\t\t\t\t\t").place(x=550, y=210)
        elif len(checking_list) == len(d):
            counter = 0
            for i, val in enumerate(checking_list):
                if val in dict_of_cuts[i]:
                    counter += 1
            if counter == len(d):
                Label(root, text=f"\tConfirmation: Number of crossing points is: {ind}\t\t\t\t").place(x=530, y=210)
                logic_val4 = True
                # Change list of strings to list of ints
                cross_al = []
                for i, j in enumerate(temp):
                    cross_al.append(int(j))
            else:
                Label(root, text=f"\t\tOne or more of cut(s) is incorrect\t\t\t\t\t").place(x=520, y=210)


    def submit5():
        """Command responsible for check if every variable has been entered"""
        logic_tuple = logic_val1, logic_val2, logic_val3, logic_val4
        logic_final = all(logic_tuple)
        if logic_final:
            al.genetic_alg(storage, int(iter_al), int(pop_al), cross_al)  # start working algorithm


    # Display interface responsible for number of test
    Label(root, text="Test number in the library: /Code/data:  ").place(x=10, y=80)
    Label(root, text="test").place(x=290, y=80)
    Label(root, text=".txt").place(x=355, y=80)
    Entry(root, textvariable=name_test_num, width=3).place(x=320, y=77.5)
    Button(root, text="Submit", command=submit1).place(x=450, y=77.5)

    # Display interface responsible for number of algorithm iteration
    Label(root, text="Number of algorithm iteration:  ").place(x=10, y=120)
    Entry(root, textvariable=name_num_it, width=3).place(x=320, y=117.5)
    Button(root, text="Submit", command=submit2).place(x=450, y=117.5)

    # Display interface responsible for number of population in algorithm
    Label(root, text="Number of population:  ").place(x=10, y=160)
    Entry(root, textvariable=name_pop_it, width=3).place(x=320, y=157.5)
    Button(root, text="Submit", command=submit3).place(x=450, y=157.5)

    # Display interface responsible for number of crossing points in algorithm
    Label(root, text="Enter number of crossing points (decline ").place(x=10, y=200)
    Label(root, text="the values with commas:").place(x=10, y=220)
    Entry(root, textvariable=name_div, width=10).place(x=320, y=207)
    Button(root, text="Submit", command=submit4).place(x=450, y=207)

    # Display interface responsible for starting algorithm work
    newFont = Font(family="Courier New", size=25, weight="bold")
    alg_button = Button(root, font=newFont, text="Start algorithm", command=submit5,
                        ).place(x=340, y=300)

    root.mainloop()
