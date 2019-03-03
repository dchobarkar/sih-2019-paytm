

import pandas as pd
import numpy
import matplotlib.pyplot as plot
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('time_data.csv', usecols=['day_type',	'send_time',	'response_time'	 , 'action',	'no_of_noti'])
data = df.values.tolist()
df1 = pd.read_csv('time_data.csv', usecols=['send_time',	'response_time', 'action', 'no_of_noti'	])
df1["no_of_noti"].fillna(1, inplace=True)
data2 = df1.values.tolist()

#lets split
list1 = []
list2 = []
for i in range(len(data2)):
        value = data2[i][0]
        value1 = value[0:2]
        value1 = int(value1)
        value2 = value[3:]
        value2 = int(value2)
        value1 = value1*6
        value2 = int(value2/10)
        list1.append(value1+value2)

for i in range(len(data2)):
        value = data2[i][1]
        value1 = value[0:2]
        value1 = int(value1)
        value2 = value[3:]
        value2 = int(value2)
        value1 = value1*6
        value2 = int(value2/10)
        list2.append(value1+value2)  


min1 = min(list1)
min2 = min(list2)
min_last = min(min1, min2)
max1 = max(list1)
max2 = max(list2)
max_last = max(max1, max2)


min_range = int(min_last/10) * 10
max_range = (int(max_last/10) + 1) * 10               

            
range_list = []
for x in range(min_range, max_range + 10, 10):
        y = x + 1
        po = [y, y + 9, 0, 0]
        range_list.append(po)

for i in range(len(data2)):
        val1 = list1[i]
        val2 = list2[i]
        val3 = data2[i][2]
        val4 = data2[i][3]
        
        for j in range(len(range_list)):
                first = range_list[j][0]
                second = range_list[j][1]
                value = range_list[j][2]
                
                if val2 >= first and val2 <= second:
                        index = j
                        break
                
                                  
        for k in range(len(range_list)):
                first = range_list[k][0]
                second = range_list[k][1]
                value = range_list[k][2]    

                if val1 >= first and val1 <= second:
                        index1 = k
                        break
                                                                
        diff = abs(index - index1)
        store = -diff/(val4+1)
        if(val3 == 0):
                store = store/1.5
        
        range_list[index1][2] = store
        range_list[index][3]+=1          

max1 = 0
index = 0
for pop in range(len(range_list)):
        sum1 = 3*range_list[pop][2] + range_list[pop][3]
        if sum1 > max1:
                max1 = sum1
                index = pop      

min_comp = range_list[index][0]
max_comp = range_list[index][1]
count = 0
sum1 = 0

for i in range(len(list2)):
        val = list2[i]
        val = int(val)
        if val >= min_comp and val <= max_comp:
                sum1+=val
                count+=1

avg = sum1/count
avg = round(avg)

quo = int(avg/6)
rem = avg % 6
rem = rem*10
answer = str(quo) +':'+ str(rem) 
print(answer)      






