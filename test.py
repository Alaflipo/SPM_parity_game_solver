import matplotlib.pyplot as plt

# formulas = ['infinite run no access', 'eventually fair shared access']
# data = [
#     [798, 5782, 28477, 110050], 
#     [4956, 58856, 219185, 3615389]
# ]
# x_values = [2, 3, 4, 5]

# for i in range(len(formulas)): 
#     plt.figure()
#     plt.xlabel('size')
#     plt.ylabel('lifts')
#     plt.title(f'Graph size vs amount of lifts for {formulas[i]}')
#     plt.plot(x_values, data[i], color='red')
#     plt.savefig(f'results/{formulas[i]}.png')

# formulas = ['invariantly inevitably eat', 'invariantly plato starves', 'invariantly possibly eat', 'plato infinitely often can eat']
# data = [
#     [22, 76, 273, 1027, 4112, 17414, 74337, 316653, 1332673, 5539214], 
#     [28, 89, 280, 955, 3004, 9634, 31553, 116128, 375110, 1345482], 
#     [33, 136, 1137, 1109, 42972, 331132, 2009450, 36599909, 151957423, 255084225], 
#     [24, 231, 1225, 4239, 44957, 196303, 1672609, 10698764, 74182973, 462037242], 
# ]
# x_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# for i in range(len(formulas)): 
#     plt.figure()
#     plt.xlabel('size')
#     plt.ylabel('lifts')
#     plt.title(f'Graph size vs amount of lifts for {formulas[i]}')
#     plt.plot(x_values, data[i], color='red')
#     plt.savefig(f'results/{formulas[i]}.png')

# formulas = ['1 elevators', '2 elevators']
# data = [
#     [161, 622, 2930, 16794, 115482, 914014], 
#     [161, 654, 3083, 17580, 118894, 930088], 
# ]
# x_values = [2, 3, 4, 5, 6, 7]

# for i in range(len(formulas)): 
#     plt.figure()
#     plt.xlabel('levels')
#     plt.ylabel('lifts')
#     plt.title(f'Levels vs amount of lifts for {formulas[i]}')
#     plt.plot(x_values, data[i], color='red')
#     plt.savefig(f'results/{formulas[i]}.png')
