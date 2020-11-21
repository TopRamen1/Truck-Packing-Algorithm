from typing import List, Tuple
import numpy as np
from copy import deepcopy


class DataFromFile:
    def __init__(self, filename_1: str, filename_2: str, filename_3: str):
        self.filename1 = filename_1
        self.filename2 = filename_2
        self.filename3 = filename_3
        #self.id_dataset = id_dataset_[-1]

    #def __str__(self) -> str:
        #return f"ID of dataset: {self.id_dataset} -> Name: '{self.filename}'".format(self=self)

    #@classmethod
    #def from_file_id(cls, filename_1):
        #return cls(filename_1, [int(i) for i in filename_1 if i.isdigit()])

    def get_package_data(self) -> List[Tuple[int, int, float]]:
        """ Extract data from .txt file into list of tuples, tuples contain information about packages: ID,
        address and weight """
        data_package = []
        with open(self.filename1, "r") as reader:
            id_p = 1
            for line in reader.readlines():
                data_temp = line.strip()
                address, weight = data_temp.split(':')
                package_tuple = id_p, int(address), float(weight)
                data_package.append(package_tuple)
                id_p += 1
        return data_package

    def get_truck_data(self) -> List[Tuple[int, str, float, float, float, float]]:
        """ Extract data from .txt file into list of tuples, tuples contain information about trucks: ID, type, load,
        exploitation, minimal combustion, maximum combustion """
        truck_package = []
        with open(self.filename2, "r") as reader:
            id_t = 1
            for line in reader.readlines():
                data_temp = line.strip()
                type_t, load, exp_cost, min_fuel_use, max_fuel_use = data_temp.split(':')
                truck_tuple = id_t, type_t, float(load), float(exp_cost), float(min_fuel_use), float(max_fuel_use)
                truck_package.append(truck_tuple)
                id_t += 1
        return truck_package

    def get_storage_data(self) -> List[Tuple[int, int, float]]:
        """ Extract data from .txt file into list of tuples, tuples contain information about storages: ID, address,
        distance from main storage """
        storage_package = []
        with open(self.filename3, "r") as reader:
            id_s = 1
            for line in reader.readlines():
                data_temp = line.strip()
                address, distance = data_temp.split(':')
                storage_tuple = id_s, int(address), float(distance)
                storage_package.append(storage_tuple)
                id_s += 1
        return storage_package


class Package:
    def __init__(self, id_: int, address_: int, weight_: float):
        self.id = id_
        self.address = address_
        self.weight = weight_

    def __str__(self) -> str:
        return f"Package no. {self.id}, Address: {self.address}, Weight: {self.weight}".format(
            self=self)

    @property
    def info_package(self):
        return f"Package no. {self.id}, Address: {self.address}, Weight: {self.weight}"


class Truck:
    def __init__(self, id_: int, type_t_: str, load_: float, exp_cost_: float, min_fuel_use_: float, max_fuel_use_: float):
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
    def __init__(self, id_: int, address_: int, distance_: float):
        self.id = id_
        self.distance = distance_
        self.address = address_

    def __str__(self) -> str:
        return f"Storage no. {self.id}, Address: {self.address}, Distance: {self.distance}".format(self=self)

    @property
    def info_storage(self):
        return f"Storage no. {self.id}, Address: {self.address}, Distance: {self.distance}".format(self=self)

#####################################################################################################################
# TODO: to co ponizej:
class MainStorage:
    def __init__(self, data_init_: DataFromFile):
        data_init = data_init_
        data_package_ = data_init.get_package_data()
        truck_package_ = data_init.get_truck_data()
        storage_package_ = data_init.get_storage_data()
        self.list_of_packages = []
        self.list_of_trucks = []
        self.list_of_storages = []
        for i in data_package_:
            new_package = Package(i[0],i[1],i[2])
            self.list_of_packages.append(new_package)
        for i in truck_package_:
            new_truck = Truck(i[0],i[1],i[2],i[3],i[4],i[5])
            self.list_of_trucks.append(new_truck)
        for i in storage_package_:
            new_storage = Package(i[0],i[1],i[2])
            self.list_of_storages.append(new_storage)

    def __iter__(self):
        return iter(self.list_of_packages)

    def __str__(self):
        return f"Number of packages: {len(self.list_of_packages)}\nNumber of trucks: {len(self.list_of_trucks)}\nNumber of storages: {len(self.list_of_storages)}".format(self=self)


    @property
    def info_main_storage(self):
        return f"Number of packages: {len(self.list_of_packages)}\nNumber of trucks: {len(self.list_of_trucks)}\nNumber of storages: {len(self.list_of_storages)}".format(self=self)

class AlgorythmData:
    def __init__(self, t_load_: np.array, t_exp_cost_, t_min_fuel_use_, t_max_fuel_use_, p_weight_, s_distance_):
        # truck data
        # self.t_type = np.array(t_type_)
        self.t_load = np.array(t_load_)
        self.t_exp_cost = np.array(t_exp_cost_)
        self.t_min_fuel_use = np.array(t_min_fuel_use_)
        self.t_max_fuel_use = np.array(t_max_fuel_use_)
        # package data
        # self.p_address = np.array(p_address_)
        self.p_weight = np.array(p_weight_)
        # storage data
        self.s_distance = np.array(s_distance_)
        # self.s_address = np.array(s_address_)

        # self.x = np.zeros((len(self.t_type), len(self.p_address)))
        # self.y = np.zeros((len(self.t_type), len(self.s_address)))
        self.x = np.array([[1, 0, 1, 0, 0], [0, 1, 0, 1, 1]])
        self.y = np.array([[0, 0, 1], [1, 1, 0]])


def objective_function(data: AlgorythmData) -> float:
    k = 5
    sum1 = np.sum((data.t_exp_cost * data.y.T), axis=1)
    print(sum1)
    sum2 = data.s_distance * np.sum((k * data.t_min_fuel_use * data.y.T), axis=1)
    print(sum2)
    sum3 = np.sum((data.p_weight * data.x), axis=1)
    print(sum3)
    sum4 = data.s_distance * np.sum((k * sum3 / data.t_load * (data.t_max_fuel_use - data.t_min_fuel_use) * data.y.T),
                                    axis=1)
    print(sum4)
    sum5 = np.sum(sum1 + sum2 + sum4, axis=0)
    print(sum5)
    return sum5


if __name__ == '__main__':
    datas = DataFromFile("data_package1.txt", "data_truck1.txt", "data_storage1.txt")
    main2 = MainStorage(datas)
    for package in main2:
        print("Package ID: {}, Package address: {}, Package weight: {}".format(package.id,package.address,package.weight))
    print(main2.list_of_packages[0])
    print(main2)

