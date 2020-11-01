from abc import ABC, abstractmethod
from copy import deepcopy

import function as fun
from typing import Optional, List, Dict
import re


class GetDataFromFile:
    def __init__(self, filename):
        self.filename = filename
        self.address_id_weight_package = fun.get_address_id_weight_package(filename)
        #self.load_id_trucks = fun.get_load_id_trucks(filename)

    def __str__(self) -> str:
        return '{self.address_id_weight_package}'.format(self=self)

class Package:
    def __init__(self, package_id: int, package_address: int, package_weight: float):
        self.package_id = package_id
        self.package_address = package_address
        self.package_weight = package_weight

    def __str__(self) -> str:
        return 'Package no. {self.package_id}, Address: {self.package_address}, Weight: {self.package_weight}'.format(
            self=self)


if __name__ == '__main__':
    getdatafromfile1 = GetDataFromFile("data_1.txt")
    dict_address_id_weight_package = getdatafromfile1.address_id_weight_package
    package_list = []
    for k, v in dict_address_id_weight_package.items():
        package_list.append(Package(k, v[0], v[1]))

    print(package_list[0])

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
#
# # grupa 1a: Burda (302827), Baradziej (302819)
