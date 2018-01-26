from random import randint

def random_numbers(number_of_numbers):
    list_of_nums = [randint(1, 100) for x in range(number_of_numbers)]
    return list_of_nums
