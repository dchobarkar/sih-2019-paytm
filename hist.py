# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:04:53 2019

@author: Saurabh
"""
import pandas as pd
import random
df = pd.read_csv('Bayesbro.csv', usecols=['A', 'B', 'C', 'D', 'E', 'F'])
data = df.values.tolist()
grand_total = 148985
sum = 0
time_data = []
day_data = []
for i in range(5):
    x = random.randint(20000, 24830)
    time_data.append(x)
    sum += x
y = grand_total - sum
time_data.append(y)
sum = 0
for i in range(6):
    x = random.randint(20000, 21283)
    day_data.append(x)
    sum += x
y = grand_total - sum
day_data.append(y)
user_day_hist = [16, 10, 10, 11, 21, 26, 26]
user_time_hist = [11, 14, 10, 16, 40, 29]
user_total = 120
final_list = []
for i in range(len(data)):
    list1 = []
    for j in range(6):
        main_item = data[i][j]

        # ab denominator ka Bayes

        day_prob = (user_day_hist[j]/day_data[j]) * \
            (day_data[j]/grand_total) / (user_total/grand_total)

        final_prob = (main_item * (time_data[j]/grand_total))/day_prob
        list1.append(round(final_prob, 3))

    final_list.append(list1)

df_new = pd.DataFrame(final_list)
df_new.columns = ['A', 'B', 'C', 'D', 'E', 'F']
df_new.to_csv('bayesBro.csv', index=False)

# print(final_list)
