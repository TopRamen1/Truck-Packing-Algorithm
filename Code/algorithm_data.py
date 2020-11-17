from functions import get_package_data
from typing import List
from copy import deepcopy
import numpy as np


class DataFromFile:
    def __init__(self, filename):
        self.filename = filename
        self.address_id_weight_package = get_package_data(filename)
        # self.load_id_trucks = fun.get_load_id_trucks(filename)

    def __str__(self) -> str:
        return '{self.address_id_weight_package}'.format(self=self)


class Package:
    def __init__(self, id_: int, address_: int, weight_: float):
        self.id = id_
        self.address = address_
        self.weight = weight_

    def __str__(self) -> str:
        return 'Package no. {self.id}, Address: {self.address}, Weight: {self.weight}'.format(
            self=self)

    @property
    def info_package(self):
        return f"Package no. {self.id}, Address: {self.address}, Weight: {self.weight}"


class Truck:
    def __init__(self, id_: int, type_: str, load_: int, exp_cost_: float, min_fuel_use_: float, max_fuel_use_: float):
        self.id = id_
        self.type = type_
        self.load = load_
        self.exp_cost = exp_cost_
        self.min_fuel_use = min_fuel_use_
        self.max_fuel_use = max_fuel_use_

    def __str__(self) -> str:
        return 'Truck no. {self.id}'.format(
            self=self)


class Storage:
    def __init__(self, id_: int, distance_: float, address_: int):
        self.id = id_
        self.distance = distance_
        self.address = address_

    def __str__(self) -> str:
        return 'Storage no. {self.id}'.format(
            self=self)


class MainStorage:
    def __init__(self, package_list_: List[Package], truck_list_, storage_list_):
        self.package_list = deepcopy(package_list_)
        self.truck_list = deepcopy(truck_list_)
        self.storage_list = deepcopy(storage_list_)

        # self.x = [[0 for t in range(len(self.truck_list))] for p in range(len(self.package_list))]
        # self.y = [[0 for t in range(len(self.truck_list))] for s in range(len(self.storage_list))]

        del package_list_, truck_list_, storage_list_


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
    sum4 = data.s_distance * np.sum((k * sum3 / data.t_load * (data.t_max_fuel_use - data.t_min_fuel_use) * data.y.T), axis=1)
    print(sum4)
    sum5 = np.sum(sum1 + sum2 + sum4, axis=0)
    print(sum5)
    return sum5


if __name__ == '__main__':