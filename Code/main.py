
from functions import get_package_data
from typing import List
from copy import deepcopy
import numpy as np

class DataFromFile:
    def __init__(self, filename):
        self.filename = filename
        self.address_id_weight_package = get_package_data(filename)
        #self.load_id_trucks = fun.get_load_id_trucks(filename)

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
    def __init__(self, datafromfile: DataFromFile):

        # get_package_num
        # for
        #     p = Package(get_package_data(i))

        self.package_list = deepcopy(package_list_)
        self.truck_list = deepcopy(truck_list_)
        self.storage_list = deepcopy(storage_list_)

        self.x = [[0 for t in range(len(self.truck_list))] for p in range(len(self.package_list))]
        self.y = [[0 for t in range(len(self.truck_list))] for s in range(len(self.storage_list))]

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
    suma1 = sum(data.t_exp_cost.*data.y, axis=1)
    suma2 = sum(data.s_distance.*k.*data.t_min_fuel_use.*data.y, axis=1)
    suma3 = sum(data.p_weight.*data.x, axis=0)
    suma4 = sum(data.s_distance.*k*suma3/data.t_load.*(data.t_max_fuel_use-data.t_min_fuel_use).*data.y, axis=1)
    suma5 = sum(suma1+suma2+suma4, axis=0)
    return suma5


if __name__ == '__main__':
    # getdatafromfile1 = DataFromFile("data_1.txt")
    # dict_address_id_weight_package = getdatafromfile1.address_id_weight_package
    # package_list = []
    # for k, v in dict_address_id_weight_package.items():
    #     package_list.append(Package(k, v[0], v[1]))
    #
    # print(package_list[0])

    alg1 = AlgorythmData([200, 100], [20, 10], [30, 20], [50, 40], [1, 1, 2, 2, 2], [10, 20])
    sum1 = objective_function(alg1)
    print(sum1)
# class TooManyProductsFoundError(Exception):
#     """ Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów """
#
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#
#
# class Server(ABC):
#     n_max_returned_entries: int = 6
#
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#
#     @abstractmethod
#     def get_entries(self, n_letters: int) -> List[Product]:
#         pass
#
#     @staticmethod
#     def find_products_from_list(product_list: List[Product], n_letters: int = 1) -> List[Product]:
#         re_letters = r'^[a-zA-Z]'
#         re_n = r'{}'.format(n_letters)
#         re_number = r'[0-9]{2,3}$'
#         re_total = re_letters + "{" + re_n + "}" + re_number
#         filtered_products = [p for p in product_list if re.search(re_total, p.name)]
#         if filtered_products and len(filtered_products) > Server.n_max_returned_entries:
#             raise TooManyProductsFoundError
#         return filtered_products
#
#
# class ListServer(Server):
#     def __init__(self, list_of_products: List[Product], *args, **kwargs):
#         self.products: List[Product] = deepcopy(list_of_products)
#         super().__init__(*args, **kwargs)
#
#     def __str__(self) -> str:
#         it = len(self.products)
#         final_string: str = ''
#         for i in range(0, it):
#             final_string += "Name: {}    ->    Price: {} PLN \n".format(self.products[i].name, self.products[i].price)
#         return final_string
#
#     def get_entries(self, n_letters: int) -> List[Product]:
#         selected_product = self.find_products_from_list(self.products, n_letters)
#         return sorted(selected_product)
#
#
# class MapServer(Server):
#     def __init__(self, list_of_products: List[Product], *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         dict_of_products = {list_of_products[i].name: list_of_products[i] for i in range(0, len(list_of_products))}
#         self.products: Dict[str, Product] = dict_of_products
#
#     def __str__(self) -> str:
#         final_string: str = ''
#         for key, value in self.products.items():
#             final_string += "Name: {}    ->    Object contains: {}\n".format(key, value)
#         return final_string
#
#     def get_entries(self, n_letters: int) -> List[Product]:
#         temp_products_list = list(self.products.values())
#         selected_product = self.find_products_from_list(temp_products_list, n_letters)
#         return sorted(selected_product)
#
#
# class Client:
#     def __init__(self, server: Server, *args, **kwargs):
#         self.server: Server = server
#         super().__init__(*args, **kwargs)
#
#     def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
#         try:
#             list_product_final = self.server.get_entries(n_letters)
#             total_price: int = 0
#             if list_product_final:
#                 for i in list_product_final:
#                     total_price += i.price
#                 return total_price
#             else:
#                 return None
#         except TooManyProductsFoundError:
#             return None
