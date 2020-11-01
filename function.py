
def get_address_id_weight_package(filename):
    num=[]
    with open(filename, "r") as reader:
        for line in reader.readlines():
            for word in line.split('\n'):
                for in_word in word.split(' '):
                    print(in_word)
                    if in_word.isdigit():
                        num.append(int(in_word))

    print(num)




if __name__ == '__main__':
    get_address_id_weight_package("data_1.txt")
