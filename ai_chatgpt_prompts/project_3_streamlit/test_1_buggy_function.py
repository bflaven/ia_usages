
# python test_1_buggy_function.py
# list1 = [7, 8, 9, 10]\n list2 = \'Bruno\'\n result = list2.join(list1)\n print(result)

# def my_func(name, place):
  # print(f"Hello {name}! Are you from {place}?")
# buggy    
# print(f"Hello name}! Are you from {place}?")
# my_func("Prisca", "Paris")

# Good corrected by chat GPT
def my_func(name, place):
 print(f'Hello {name}! Are you from {place}?')
# test
my_func("Prisca", "Paris")
