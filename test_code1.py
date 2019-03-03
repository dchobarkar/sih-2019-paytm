import pandas as pd
df = pd.read_csv('travel_time.csv', usecols=['time', 'distance', 'speed'])
data = df.values.tolist()
df1 = pd.read_csv('travel_time.csv', usecols=['distance', 'speed'])
data2 = df1.values.tolist()
threshold_distance = 3000
speed_threshold = 10

list1 = []

for i in range(len(data)):
        value = data[i][0]
        value1 = value[0:2]
        value1 = int(value1)
        value2 = value[3:]
        value2 = int(value2)
        value1 = value1*6
        value2 = int(value2/10)
        list1.append(value1+value2)

list2 = []
for i in range(len(data2)-1):
        value =  int(round(float(data2[i][0])))
        value1 = int(round(float(data2[i+1][0]))) 
        speed1 = int(round(float(data2[i][1])))
        speed2 = int(round(float(data2[i+1][1])))
        
        if abs(value1 - value) >= threshold_distance and abs(speed1 - speed2) >=speed_threshold :
                  x = (data[i][0], data[i+1][0])                      
                  list2.append(x)

from collections import OrderedDict
list3 = OrderedDict((x, True) for x in list2).keys()
print(list3)    
#listx = list(set(list2))