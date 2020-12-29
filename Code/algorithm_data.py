from typing import List, Tuple, Dict
import os
import random
import pandas as pd
import numpy as np


class DataFromFile:
    """Class needed for work with files (.txt), which contains class function to return data from specific .txt file"""

    def __init__(self, filename_p: str, filename_t: str, filename_s: str, id_dataset_: int):
        """
        :param filename_p: filename with information about packages
        :param filename_t: filename with information about trucks
        :param filename_s: filename with information about storages
        :param id_dataset_: dataset id
        """
        self.filename1 = filename_p
        self.filename2 = filename_t
        self.filename3 = filename_s
        self.id_dataset = id_dataset_

    def __str__(self) -> str:
        return f"ID of dataset: {self.id_dataset} -> Names: '{self.filename1},'{self.filename2}','{self.filename3}'" \
            .format(self=self)

    def get_package_data(self) -> List[Tuple[int, int, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about packages: ID,
           address and weight """

        data_package = []
        with open(self.filename1, "r") as reader:
            id_p = 0
            for line in reader.readlines():
                data_temp = line.strip()
                address, weight = data_temp.split(':')
                package_tuple = id_p, int(address), float(weight)
                data_package.append(package_tuple)
                id_p += 1
        return data_package

    def get_truck_data(self) -> List[Tuple[int, str, float, float, float, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about trucks: ID, type, load,
           exploitation, minimal combustion, maximum combustion"""

        truck_package = []
        with open(self.filename2, "r") as reader:
            id_t = 0
            for line in reader.readlines():
                data_temp = line.strip()
                type_t, load, exp_cost, min_fuel_use, max_fuel_use = data_temp.split(':')
                truck_tuple = id_t, type_t, float(load), float(exp_cost), float(min_fuel_use), float(max_fuel_use)
                truck_package.append(truck_tuple)
                id_t += 1
        return truck_package

    def get_storage_data(self) -> List[Tuple[int, int, float]]:
        """Extract data from .txt file into list of tuples, tuples contain information about storages: ID, address,
           distance from main storage"""

        storage_package = []
        with open(self.filename3, "r") as reader:
            id_s = 0
            for line in reader.readlines():
                data_temp = line.strip()
                address, distance = data_temp.split(':')
                storage_tuple = id_s, int(address), float(distance)
                storage_package.append(storage_tuple)
                id_s += 1
        return storage_package


class Package:
    """Class needed for create packages and information about them"""

    def __init__(self, id_: int, address_: int, weight_: float):
        """
        :param id_: package id
        :param address_: package address, information where specific package should be delivered
        :param weight_: package weight
        """
        self.id = id_
        self.address = address_
        self.weight = weight_

    def __str__(self) -> str:
        return f"Package no. {self.id}, Address: {self.address}, Weight: {self.weight}".format(self=self)

    @property
    def info_package(self):
        return f"Package no. {self.id}, Address: {self.address}, Weight: {self.weight}"


class Truck:
    """Class needed for create trucks and information about them"""

    def __init__(self, id_: int, type_t_: str, load_: float, exp_cost_: float, min_fuel_use_: float,
                 max_fuel_use_: float):
        """
        :param id_: truck id
        :param type_t_: type of truck (example: "A", "B:, ...)
        :param load_: maximum load of truck
        :param exp_cost_: virtual indicator which shows cost value of employment and operation of trucks
        :param min_fuel_use_: min. combustion of trucks
        :param max_fuel_use_: max. combustion of trucks
        """
        self.id = id_
        self.type_t = type_t_
        self.load = load_
        self.exp_cost = exp_cost_
        self.min_fuel_use = min_fuel_use_
        self.max_fuel_use = max_fuel_use_

    def __str__(self) -> str:
        return f"Truck no. {self.id}, Type: {self.type_t}, Load: {self.load}, Exploitation: {self.exp_cost}, Min. " \
               f"combustion: {self.min_fuel_use}, Max. combustion: {self.max_fuel_use}".format(self=self)

    @property
    def info_truck(self):
        return f"Truck no. {self.id}, Type: {self.type_t}, Load: {self.load}, Exploitation: {self.exp_cost}, Min. " \
               f"combustion: {self.min_fuel_use}, Max. combustion: {self.max_fuel_use}".format(self=self)


class Storage:
    """Class needed for create storages and information about them"""

    def __init__(self, id_: int, address_: int, distance_: float):
        """
        :param id_: storage id
        :param address_: storage address (example: package with address: 1 goes to storage with address: 1)
        :param distance_: distance from main storage to storage
        """
        self.id = id_
        self.address = address_
        self.distance = distance_

    def __str__(self) -> str:
        return f"Storage no. {self.id}, Address: {self.address}, Distance: {self.distance}".format(self=self)

    @property
    def info_storage(self):
        return f"Storage no. {self.id}, Address: {self.address}, Distance: {self.distance}".format(self=self)


class MainStorage:
    """Class needed for create main storage and all information about other smaller storages, trucks and packages"""

    def __init__(self, data_init_: DataFromFile = None):
        """
        :param data_init_: object class DataFromFile needed to initialize below Lists (example: list_of_packages - List
                           of object class Package)
        """
        self.list_of_packages = []
        self.list_of_trucks = []
        self.list_of_storages = []
        self.k = 4.5  # fuel price

        if data_init_:
            for i in data_init_.get_package_data():
                self.list_of_packages.append(Package(i[0], i[1], i[2]))

            for i in data_init_.get_truck_data():
                self.list_of_trucks.append(Truck(i[0], i[1], i[2], i[3], i[4], i[5]))

            for i in data_init_.get_storage_data():
                self.list_of_storages.append(Storage(i[0], i[1], i[2]))

    def __iter__(self):
        return iter(self.list_of_packages)

    def __str__(self):
        return f"Number of packages: {len(self.list_of_packages)}\nNumber of trucks: {len(self.list_of_trucks)}\n" \
               f"Number of storages: {len(self.list_of_storages)}".format(self=self)

    @property
    def info_main_storage(self):
        return f"Number of packages: {len(self.list_of_packages)}\nNumber of trucks: {len(self.list_of_trucks)}\n" \
               f"Number of storages: {len(self.list_of_storages)}".format(self=self)

    @property
    def get_used_sto_pack(self) -> Dict[int, List[int]]:
        """Create dictionary which contain number of used storages (key) and number of package's addresses (value)
           :return: above dictionary - Dict[int, List[int]]"""

        list_of_used_addresses = []
        list_of_used_storages = []  # List of active storages in case of there is a chance that there are storages
        # without any set of packages

        for package in self.list_of_packages:
            list_of_used_addresses.append(package.address)
        for storage in self.list_of_storages:
            if storage.address in list_of_used_addresses:
                list_of_used_storages.append(storage.address)
        del list_of_used_addresses

        counters = [[0] * len(list_of_used_storages)]
        for s in list_of_used_storages:
            for p in self.list_of_packages:
                if p.address == s:
                    counters[0][s] += 1

        dict_of_used_p_s = {}  # Dict of number of used storages and counters :Dict: {storage: counter}
        counters = counters[0][:]  # List of numbers of package's addresses
        for s in list_of_used_storages:
            for i, c in enumerate(counters):
                if s == i:
                    dict_of_used_p_s[s] = c

        return dict_of_used_p_s


def create_testfile(num_of_tests: int, num_of_packages: int, package_intervals: List[int], num_of_storages: int,
                    storage_intervals: List[int]):
    """Creates dictionary with .txt files containing data"
    :params: amount of dictionaries, that will be created
             number of packages
             intervals of packages weights
             number of storages
             intervals of storages distances"""

    for i in range(num_of_tests):
        directory = 'data_random/test%d' % (i + 1)
        try:
            os.mkdir(directory)
            print("Directory ", 'test%d' % (i + 1), " created ")
        except FileExistsError:
            print("Directory ", 'test%d' % (i + 1), " already exists")
        f = open("%s/p.txt" % directory, "w+")
        f2 = open("%s/t.txt" % directory, "w+")
        f3 = open("%s/s.txt" % directory, "w+")

        for e in range(num_of_storages):
            f3.write("%d:%e\n" % (e, random.randint(storage_intervals[0], storage_intervals[1])))

        for a in range(num_of_packages):
            f.write("%d:%e\n" % (
            random.randint(0, num_of_storages - 1), random.randint(package_intervals[0], package_intervals[1])))
            x = random.randint(1, 4)
            if x == 1:
                f2.write("A:1000.0:4.23:14.0:19.56\n")
            if x == 2:
                f2.write("B:1500.0:4.78:21.3:32.0\n")
            if x == 3:
                f2.write("C:2000.0:5.1:24.0:35.32\n")
            if x == 4:
                f2.write("D:2500.0:5.16:26.4:39.8\n")


def csv_reader_param(directory: str) -> List[List[int]]:
    """Read parameters from .csv file"""

    cols = ["Iteration", "Population", "Crossing", "Mutation", "Crs1", "Crs2", "Crs3"]
    col_reader = pd.read_csv(directory, delimiter=';', names=cols)
    it = col_reader.Iteration.to_list()
    pop = col_reader.Population.to_list()
    cross = col_reader.Crossing.to_list()
    mut = col_reader.Mutation.to_list()
    crs1 = col_reader.Crs1.to_list()
    crs2 = col_reader.Crs2.to_list()
    crs3 = col_reader.Crs3.to_list()
    del (pop[0], it[0], cross[0], mut[0])
    return [it, pop, cross, mut, crs1, crs2, crs3]


def csv_reader_outputs(directory: str):
    """Read outputs from .csv files"""

    cols = ["P: Iteration"]
    col_reader = pd.read_csv(directory, delimiter=',').T
    a = col_reader.to_dict('split')

    return a["data"][1], a["data"][2]


def csv_writer(ins: int, num_param: int, *args):
    """Create final file with all values created from the operation of the algorithm
       :param ins: number of data instance
       :param num_param: number of data parameters
       :param args: dicts which contain name and list of values - Dict[str: List[int (or str)]]"""

    data = ()
    columns = []
    for i in args:
        for key, value in i.items():
            columns.append(key)
            data += (value,)

    df = pd.DataFrame(list(data)).T

    # For all parameters fill empty cells char: "
    for k, i in enumerate(args):
        for key, value in i.items():
            if len(value) == 1:
                df[k].replace(np.nan, ' " ', inplace=True)

    index = df.index
    index.name = "Iteration"
    df.to_csv(f'outputs/instance{ins}_param{num_param}.csv', header=columns)