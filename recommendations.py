import pandas as pd
df = pd.read_csv('products.csv')
product_id = df['product_id']
parent_id = df['parent_id']
df1 = pd.read_csv('products.csv', usecols=['product_id', 'parent_id'])[:162]
data = df1.values.astype(int).tolist()
children = []
for i in product_id:
    list1 = []
    for j in range(len(data)):
        store = data[j][0]
        store1 = data[j][1]
        if i == store1:
            list1.append(store)
    children.append(list1)    

df['children'] = children
df.to_csv('products.csv')  
df2 = pd.read_csv('products.csv', usecols=['product_id', 'parent_id', 'children'])[1:162]
df2["parent_id"].fillna("0", inplace=True)
data2 = df2.values.tolist()
products = []
for i in range(len(data2)):
    data2[i][1] = int(data2[i][1])

#extracting elements which are prodcuts
import ast

for i in range(len(data2)):
    data2[i][2] = ast.literal_eval(data2[i][2])


for i in range(len(data2)):
    hold = data2[i][2]
    list3 = []
    if len(hold) == 0:
        list3 = data2[i]
    else:
        continue
    products.append(list3)

#ab mere pass actual products hai jinko ab apas mai values deni hai
answer = []


for i in range(len(products)):
    listx = []
    first_id = products[i][0]
    first_parent = products[i][1]
    for j in range(len(products)):
        second_id = products[j][0]
        second_parent = products[j][1]
        if second_id == first_id:
            factor = 1
            listx = [first_id, second_id, factor]
            answer.append(listx)
        elif second_parent == first_parent:
                factor = 0.6
                listx = [first_id, second_id, factor]
                answer.append(listx)


first_level = []            
#ab jinka papa zero hai na unko direct co-relation 0.1 kar dete
for i in range(len(data2)):
    listy = []
    first_id = data2[i][0]
    first_parent = data2[i][1]
    if first_parent == 0:
        for j in range(len(data2)):
            second_id = data2[j][0]
            second_parent = data2[j][1]
            if second_parent == 0:
                if second_id == first_id:
                    continue
                else :
                    factor = 0.01
                    listy = [first_id, second_id, factor]
                    answer.append(listy)
                    first_level.append(first_id)


first_level = list(set(first_level))            
#extracting second level categories(ye related hai thode kyuki)   
level2 = []              
for i in range(len(data2)):
    listz = []
    first_id = data2[i][0]
    first_parent = data2[i][1]
    total_childs = len(data2[i][2])
    
    if (first_parent != 0 and first_parent not in first_level) and (int(total_childs) > 0) :
        listz = data2[i]
        level2.append(listz)





#now setting relationship between their children
for i in range(len(level2)):
    lista = []
    first_id = level2[i][0]
    first_parent = level2[i][1]
    first_ch = level2[i][2]
    for j in range(len(level2)):
        second_id = level2[j][0]
        second_parent = level2[j][1]
        second_ch = level2[j][2]
        if second_id == first_id:
            continue
        elif second_parent == first_parent:
            for k in first_ch:
                for l in second_ch:
                    factor = 0.25
                    lista = [k, l, factor]
                    answer.append(lista)
            for k in second_ch:
                for l in first_ch:
                    factor = 0.25
                    lista = [k, l, factor]
                    answer.append(lista)        


#new table creation
df_new = pd.DataFrame(answer)
df_new.columns = ['product_1_id', 'product_2_id', 'factor']
df_new.to_csv('recommendations.csv', index=False)


        











