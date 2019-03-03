import os
import sqlite3
import pandas as pd


data_table = pd.read_csv('recommendations.csv', usecols=['product_1_id', 'product_2_id', 'factor'])
product_table = pd.read_csv('products.csv', usecols=['product_id', 'number_of_purchases','name', 'actual_price',
                'original_price', 'discount_percentage', 'number_of_offers', 'seller_name'])[:162]

product_table["number_of_purchases"].fillna("0", inplace=True)


df = pd.read_csv('time_data.csv', usecols=['day_type',	'send_time',	'response_time'	 , 'action',	'no_of_noti'])



# Add the data to our database

# Clear example.db if it exists
#if os.path.exists('example.db'):
 #   os.remove('example.db')
# Create a database
conn = sqlite3.connect('example.db')

def create_table(conn, create_table_sql):
        cur = conn.cursor()
        cur.execute(create_table_sql)

#storing search history results in database
sql_create_searches_table = """ CREATE TABLE IF NOT EXISTS searches (
                                        user_id integer,
                                        search1_id integer NULL,
                                        time_spent REAL NULL
                                    ); """


#for notifications category 1                
sql_create_notifications_table = """ CREATE TABLE IF NOT EXISTS notifications
                                        (
                                        user_id integer,
                                        product_id integer 
                                        time_of_sending integer,
                                        time_of_action integer,
                                        action integer
                                        );"""
# 0 for dismiss 1 for save_later and 2 for opted in
#one time user asking
sql_create_time_table = """ CREATE TABLE IF NOT EXISTS user_time
                                (
                                user_id integer,
                                notif_category integer,
                                time_id integer
                                );"""
                

sql_create_time_table_gaandu = """ CREATE TABLE IF NOT EXISTS user_side_notifications
                                (
                                user_id integer,
                                product_id integer,
                                time_id text
                                );"""                
                

create_table(conn, sql_create_searches_table)
create_table(conn, sql_create_time_table)
create_table(conn, sql_create_notifications_table)
create_table(conn, sql_create_time_table_gaandu)


# Add the data to our database
data_table.to_sql('data_table', conn, if_exists= 'append', dtype={
    'product_1_id':'INTEGER',
    'product_2_id':'INTEGER',
    'factor':'REAL'})

df.to_sql('time_data', conn, if_exists= 'append', dtype={
    'day_type':'VARCHAR(10)',
    'send_time':'VARCHAR(10)',
    'response_time':'VARCHAR(10)',
    'action':'INTEGER',
    'no_of_noti': 'INTEGER'
    })

        
        
                                                        
product_table.to_sql('product_table', conn, if_exists= 'append', dtype={
    'product_id':'INTEGER',
    'number_of_purchases':'INTEGER',
    'name':'VARCHAR(1000)',
    'actual_price': 'INTEGER',
    'original_price': 'INTEGER',
    'discount_percentage': 'INTEGER',
    'number_of_offers': 'INTEGER',
    'seller_name': 'VARCHAR(100)' }) 
        

        
        
        
        
    
conn.row_factory = sqlite3.Row

# Make a convenience function for running SQL queries
def sql_query(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(list(row))
    return data

def sql_edit_insert(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()
    return 1

def sql_delete(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    return 1

def sql_query2(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    #conn.commit()
    data = []
    rows = cur.fetchall()
    for row in rows:
            data.append([x for x in row])
    return data





