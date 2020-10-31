import unittest
from collections import Counter
from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError


if __name__ == '__main__':
#  unittest.main()



# server_types = (ListServer, MapServer)
#
#
# class ServerTest(unittest.TestCase):
#     def test_get_entries_returns_proper_entries(self):
#         products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
#         for server_type in server_types:
#             server = server_type(products)
#             entries = server.get_entries(2)
#             self.assertEqual(Counter([products[2], products[1]]), Counter(entries))
#
#
# class ClientTest(unittest.TestCase):
#     def test_total_price_for_normal_execution(self):
#         products = [Product('PP234', 2), Product('PP235', 3)]
#         for server_type in server_types:
#             server = server_type(products)
#             client = Client(server)
#             self.assertEqual(5, client.get_total_price(2))
#
#
# ######################## WŁASNE TEST ########################
#
# class ServerTest2(unittest.TestCase):
#
#     def test_get_entries_returns_empty_list(self):
#         products = [Product('P12', 1), Product('PP2374', 2), Product('PP235', 1)]
#         for server_type in server_types:
#             server = server_type(products)
#             entries = server.get_entries(5)
#             self.assertEqual(entries, [])
#
#     def test_sorting_function_returns_proper_order(self):
#         products = [Product('P12', 1), Product('PP234', 2), Product('PT124', 12), Product('PW24', 23),
#                     Product('PP2', 13), Product('KWD12', 100), Product('PX432', 100)]
#         for server_type in server_types:
#             server = server_type(products)
#             self.assertSequenceEqual((products[1], products[2], products[3], products[6]), server.get_entries(2))
#
#
# class ServerTest3(unittest.TestCase):
#     def test_get_entries_exceptions(self):
#         products = [Product('P12', 1), Product('PP234', 2), Product('PT124', 12), Product('PW24', 23),
#                     Product('PP2', 13), Product('KWD12', 100), Product('PX432', 100), Product('RR432', 100),
#                     Product('PP302', 100), Product('XD420', 108)]
#         for server_type in server_types:
#             server = server_type(products)
#             with self.assertRaises(TooManyProductsFoundError):
#                 server.get_entries(2)
#
#
# class ClientTest2(unittest.TestCase):
#     def test_total_price_for_normal_execution(self):
#         products = [Product('PP2354', 2), Product('P235', 3)]
#         for server_type in server_types:
#             server = server_type(products)
#             client = Client(server)
#             self.assertEqual(None, client.get_total_price(2))
#
#
# class ClientTest3(unittest.TestCase):
#     def test_total_price_for_normal_execution(self):
#         products = [Product('PP354', 2), Product('PP235', 3), Product('PP154', 2), Product('PK35', 3),
#                     Product('PW54', 2), Product('P235', 3), Product('PW954', 2), Product('PS75', 3), Product('PS32', 1)]
#         for server_type in server_types:
#             server = server_type(products)
#             client = Client(server)
#             self.assertEqual(None, client.get_total_price(2))
#
 []

# grupa 1a: Burda (302827), Baradziej (302819)