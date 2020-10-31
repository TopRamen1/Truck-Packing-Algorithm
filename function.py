
def get_address_id_weight_package(filename):
    f = open(filename, "r")
    for x in f:
        address_id_weight_package = {2: [x, 4]}
    return address_id_weight_package

