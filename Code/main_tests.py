import unittest
import math
from algorithm import *
from algorithm_data import *


class AlgorithmTests(unittest.TestCase):
    def test_init_pop_1(self):
        n = 3  # population size
        storage = MainStorage(None)
        storage.list_of_packages.extend([Package(0, 2, 200), Package(1, 0, 200), Package(2, 1, 300),
                                         Package(3, 0, 500), Package(4, 2, 100)])
        storage.list_of_trucks.extend([Truck(0, "D", 1000, 2, 10, 15), Truck(1, "B", 1500, 3, 13, 20),
                                       Truck(2, "C", 700, 4, 18, 24), Truck(3, "A", 800, 5, 22, 29)])
        storage.list_of_storages.extend([Storage(0, 0, 200), Storage(1, 1, 400), Storage(2, 2, 600),
                                         Storage(3, 3, 800)])

        pop = init_pop(storage, n)
        self.assertEqual(len(pop), n)
        for i in pop:
            len_ch = len(i.ch_p)+len(i.ch_t)
            self.assertEqual(9, len_ch)

    def test_obj_fcn_1(self):
        storage = MainStorage(None)
        storage.k = 5
        storage.list_of_packages.extend([Package(0, 0, 200), Package(1, 0, 300), Package(2, 1, 300),
                                         Package(3, 0, 500), Package(4, 2, 100)])
        storage.list_of_trucks.extend([Truck(0, "D", 1000, 2, 10, 15), Truck(1, "B", 500, 3, 14, 19),
                                       Truck(2, "C", 700, 4, 18, 24), Truck(3, "A", 300, 5, 22, 29)])
        storage.list_of_storages.extend([Storage(0, 0, 100), Storage(1, 1, 200), Storage(2, 2, 300),
                                         Storage(3, 3, 400)])
        pop1 = Individual([0, 0, 1, 2], [0, 1, 2, 0, 3], 0)

        result = obj_fcn(storage, pop1)
        decimals = 3

        self.assertEqual((lambda n, dec: math.ceil(n * 10 ** dec) / (10 ** dec))(result, decimals), 737.215)

    def test_obj_fcn_2(self):
        storage = MainStorage(None)
        storage.k = 3
        storage.list_of_packages.extend([Package(0, 0, 400), Package(1, 1, 300), Package(2, 1, 200),
                                         Package(3, 0, 500), Package(4, 2, 100), Package(5, 3, 400)])
        storage.list_of_trucks.extend([Truck(0, "D", 800, 2, 10, 13), Truck(1, "B", 1000, 3.5, 12, 21),
                                       Truck(2, "C", 1100, 4.2, 12, 22), Truck(3, "A", 700, 5.5, 21, 25)])
        storage.list_of_storages.extend([Storage(0, 0, 200), Storage(1, 1, 600), Storage(2, 2, 900),
                                         Storage(3, 3, 400)])
        pop1 = Individual([0, 1, 2, 3], [0, 1, 1, 0, 2, 3], 0)

        result = obj_fcn(storage, pop1)
        decimals = 3

        self.assertEqual((lambda n, dec: math.ceil(n * 10 ** dec) / (10 ** dec))(result, decimals), 1020.425)


if __name__ == '__main__':
    unittest.main()
