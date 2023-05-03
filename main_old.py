# import os #For lesson15
# import re #For lesson16

# Lesson 15
# shell_name = os.environ["SHELL"]
# if shell_name == "/bin/bash":
#     print("Greetings BASH")
# else:
#     print("Hello " + shell_name[5:])

# Lesson 16
# Решение
# Формирование списка словарей
# start_sum = ["1_1000", "2_30000", "3_100000", "8_100", "5_11111", "9_14124124124", "6_444", "4_123456",
#              "7_100000000000", "10_81214"]
# rate = ["1_10", "2_11", "3_8", "4_13", "5_11", "6_6", "7_9", "8_11", "9_13", "10_12"]
# term = ["1_1", "2_2", "3_2", "4_6", "5_8", "6_20", "7_9", "8_11", "9_13", "10_12"]
# start_sum.sort(); start_sum.append(start_sum[0]); start_sum.pop(0)
# n = 0
# idn_list = []
# for n in start_sum:
#     # print(n + '\n')
#     idn = re.match(r'\d\d?\d?', n).group(0)
#     # print(x + '\n')
#     exec("idn_dict_%s = {'id': int(re.split(r'_', n)[0]), 'start_sum': int(re.split(r'_', n)[1])}" % idn)
#     exec('idn_list.append(idn_dict_%s)' % idn)
# for n in rate:
#     idn = re.match(r'\d\d?\d?', n).group(0)
#     exec("idn_dict_%s.update(rate = int(re.split(r'_', n)[1]))" % idn)
# for n in term:
#     idn = re.match(r'\d\d?\d?', n).group(0)
#     exec("idn_dict_%s.update(term = int(re.split(r'_', n)[1]))" % idn)
# # расчёт сложного процента
# def pow(x,y):
#     i = 1
#     power = 1
#     for i in range(y):
#         power = power * x
#         i += i
#     return power
# percent = lambda f_sum, f_perc: f_sum * f_perc
# for d_perc in idn_list:
#     st_sum = d_perc['start_sum']
#     perc = 1 + d_perc['rate'] / 100
#     prof = pow(perc, d_perc['term'])
#     raw_sum = percent(st_sum, prof)
#     end_sum = float('{:.2f}'.format(raw_sum))
#     d_perc.update(end_sum=float(end_sum))
# print(idn_list)