
from flask import Flask, request, redirect, render_template, jsonify
import pandas as pd
import math

app = Flask(__name__)



@app.route('/sendDynamicTest', methods=["POST"])
def send_dyanamic_test():
        from pyfcm import FCMNotification
       # from functions.sqlquery import sql_query
        import schedule
        import time

        push_service = FCMNotification(api_key="AAAAYNJto2I:APA91bEHdYbm2mhUfGfBIWseFzintaOJgJDifgSyzJdfcZrCyUdLD9XPwSKlX6IMaOeXNMkdTSs52mGKVequsJ_JtdZcq-6e15L9UzjHhs2JaMhcHmpDPgBu0D0bmPyXO2pqHa2Q0q0d")
         
        #registration_id = "e-nFqTWX25w:APA91bE2X84_I30e2XZE4assg0qWea0VZjRr_liIREzYMWviaxg67Fh13iIp44-Wwi4XynZnMveC98hOEaWf3BTy1mEvF3FpEY8LXLfrY8ipZO2JGGwyw4_UAmr0yNv2matfY20UJ9Ow"
        registration_id = "f8bLCD9kaoI:APA91bGN7uLHIZyefhLFBLa_HvHedRH7sq-o-LFKelIEkV9NS_ZGCrFVUePsySHjaeZZoWREfRkwF6LEcF-Z1vYpzfybfGJb7hMIwfdknVQzPcneWMsBpFsLDIlw4A7QAzFSS9vO9lVL"
        message_title = ["We think you will love","Indipendance Day Sale","Sunday Special","Happy Birthday"]
        message_body = ["Boat bassheadz earphones (Frosty White)","Celebrate independance day with Rs.100 off","Enjoy your holiday with Rs. 1000 off","Celebrate your Birthday with Rs. 50 off"]
        
       
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title[1], message_body=message_body[1])
        return jsonify(result)






@app.route('/') 
def sql_database():
     from functions.sqlquery import sql_query
     results = sql_query(''' SELECT * FROM data_table''')
     import getMeMyTime
     sk = getMeMyTime()
     return jsonify(sk)
 

@app.route('/sendTest', methods=["POST"])
def send_test():
        from pyfcm import FCMNotification
       # from functions.sqlquery import sql_query
        import schedule
        import time

        push_service = FCMNotification(api_key="AAAAYNJto2I:APA91bEHdYbm2mhUfGfBIWseFzintaOJgJDifgSyzJdfcZrCyUdLD9XPwSKlX6IMaOeXNMkdTSs52mGKVequsJ_JtdZcq-6e15L9UzjHhs2JaMhcHmpDPgBu0D0bmPyXO2pqHa2Q0q0d")
         
        #registration_id = "e-nFqTWX25w:APA91bE2X84_I30e2XZE4assg0qWea0VZjRr_liIREzYMWviaxg67Fh13iIp44-Wwi4XynZnMveC98hOEaWf3BTy1mEvF3FpEY8LXLfrY8ipZO2JGGwyw4_UAmr0yNv2matfY20UJ9Ow"
        registration_id = "f8bLCD9kaoI:APA91bGN7uLHIZyefhLFBLa_HvHedRH7sq-o-LFKelIEkV9NS_ZGCrFVUePsySHjaeZZoWREfRkwF6LEcF-Z1vYpzfybfGJb7hMIwfdknVQzPcneWMsBpFsLDIlw4A7QAzFSS9vO9lVL"
        message_title = "We think you will love"
        message_body = "Boat bassheadz earphones (Frosty White)"
        
        def job():
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        schedule.every().day.at("01:49").do(job)

        while 1:
                schedule.run_pending()
                time.sleep(1)       
        return jsonify(result)
 
#ye baaki hai        
@app.route('/getRecom/<id>', methods=["GET"])
def getRecom(id):
    store = id
    #results = []
    from functions.sqlquery import sql_query2
    final_answer = []
    results = sql_query2(''' SELECT product_2_id FROM data_table WHERE product_1_id = ? and factor > 0.5''', (store,))
    #sirf dikhaneke liye

    for i in range(len(results)):
        var = results[i][0]
        answer = sql_query2(''' SELECT * FROM product_table WHERE product_id = ?''', (var,))
        final_answer.append(answer)
    return jsonify(final_answer)

@app.route('/getDetails/<id>', methods = ["GET"])
def getDetails(id):
    store = id
    from functions.sqlquery import sql_query2
    results = sql_query2(''' SELECT * FROM product_table WHERE product_id = ?''', (store,))
    return jsonify(results[0])

@app.route('/pushData', methods=["POST"])
def push_Data():
    user_id = request.form['user_id']
    time_array = ['if_opted_in', 'if_zoomed_in', 'if_checked_details', 'if_checked_reviews']
    time_dict = {'if_opted_in':2, 'if_zoomed_in':2, 'if_checked_details':3, 'if_checked_reviews':3}
    total_time = 0
    for k in range(len(time_array)):
            var = int(request.form[time_array[k]])
            if var != 0:
                    total_time+=time_dict.get(time_array[k])

    search_id = request.form['search_id']
    from functions.sqlquery import sql_edit_insert, sql_query
    results = sql_edit_insert(''' INSERT INTO searches (user_id,search1_id, time_spent) VALUES (?,?,?)''', (user_id,search_id, total_time))
    answer = sql_query(''' SELECT * from searches''')
    df_new = pd.DataFrame(answer)
    df_new.columns = ['user_id', 'search1_id', 'time_spent']
    df_new.to_csv('user_history.csv', index=False)
    return jsonify(results)


@app.route('/getData', methods=["GET"])   
def getData():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM searches''')
    results = results[-10:]
    return jsonify(results)


@app.route('/getUserSuitedTime', methods=["POST"])
#ye hai hi nahi or baadmai karenge
def getUserTime():
        user_id = request.form['user_id']
        notif_category = request.form['notif_category']
        #ab time_id ek hi aana chaiye nahi to agar multiple aaya to algo waise aayega
        #abhi lets take only one for each category and overwrite agar jyaada liya to
        #ek hi aayega number mere pass
        time_id = request.form['time_id']
        #time_ids are derived from time_slot.csv
        from functions.sqlquery import sql_query2
        results = sql_query2(''' INSERT INTO user_time (user_id, notif_category, time_id) VALUES (?,?,?)''', (user_id, notif_category, time_id))
        results2 = sql_query2(''' SELECT * from user_time WHERE user_id = ? ''', (user_id,))
        return jsonify(results2)
        

@app.route('/mapUserTimeAndAction', methods=["POST"])
#ye bhi baaki hai
#this is for notification category 1 mapping user intent
def mapUserTime():
        #return jsonify("Success")
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        jo_mera_hai = int(product_id)
        time_of_sending = request.form['time_of_sending']
        time_of_action = request.form['time_of_action']
        action = int(request.form['action'])
        #0 for dismiss ,1 for save later, 2 for opt_in 
        from functions.sqlquery import sql_query2, sql_query
        results = sql_query2(''' INSERT INTO notifications (user_id, product_id, time_of_sending, time_of_action,action) VALUES (?,?,?,?,?)''', (user_id, product_id, time_of_sending, time_of_action, action))
        results2 = sql_query2(''' SELECT * from notifications WHERE user_id = ? ''', (user_id,))
        
        #if action is dismissed- get a better product.
        if action == 0:
                
                #ab ye kya karega, like time ye log jo decide karenge tab tak rukega 
                #but will punish the original product ki wo kaise aaya aise
                #from functions.sqlquery import sql_query2, sql_query
                results = sql_query2(''' SELECT search1_id, time_spent from searches where user_id = ?''',  (user_id,)) 
                results = results[-10:] 
                
                df = pd.read_csv('products.csv', usecols=['product_id', 'number_of_purchases','name', 'actual_price',
                                'original_price', 'discount_percentage', 'number_of_offers', 'seller_name'])[1:162]
                df["number_of_purchases"].fillna("0", inplace=True) 
                df2 = pd.read_csv('products.csv', usecols=['product_id', 'number_of_purchases'])[1:162]
                df2["number_of_purchases"].fillna("1", inplace=True) 
                
                main_data = df.values.tolist() 
                data2 = df2.values.tolist()
                
                for i in range(len(data2)):
                        data2[i][0] = int(data2[i][0])
                        data2[i][1] = int(data2[i][1])
                
                df3 = pd.read_csv('recommendations.csv')
                data3 = df3.values.tolist()
                for i in range(len(data3)):
                        data3[i][0] = int(data3[i][0])
                        data3[i][1] = int(data3[i][1])                   
                total = 0 
                for i in range(len(data2)):
                        total+=data2[i][1]               
                max_value = 0
                final_id = 1 
                
                scale_factor = []
                x = 512
                for t in range(10):
                        scale_factor.append(x)
                        x = int(x/2) 
                
                
                #for the product dismissed, the scale factor for it should be set properly
                #phir hi wo aage nahi aayega
           
                result_list = []
                scale_index = 0
                
                for i in range(len(data2)):
                        pro_id = data2[i][0]   
                        final_prob = 0
                        every_result = []
                        for j in range(len(results)):
                                #return jsonify(len(scale_factor))
                                second_id = results[j][0]
                                time_value = results[j][1]
                                #ab inka intersection nikaalna padta
                                intersect_value = sql_query2(''' SELECT factor from 
                                data_table where product_1_id = ? 
                                and product_2_id = ?''',  (pro_id,second_id)) 
                                
                                if not intersect_value:
                                        value = 0.1
                                else:
                                        value = intersect_value[0][0]
                                        
                                #time aayega abhi bas
                                      
                                quantity_value = sql_query2(''' SELECT number_of_purchases from 
                                product_table where product_id = ? ''', (second_id,))
                                quantity = quantity_value[0][0]
                               
                                # bayes_prob = probability of A intersection B * probability of purchase b
                                ratio = quantity/total
                                computed_value = math.log10(quantity)
                                time_log = math.log10(time_value)
                                #log of denominator jaruri nahi hai because nonetheless it manages
                                #itself by minusing itself from
                                if pro_id == jo_mera_hai:
                                        #return jsonify("idhar hai kuch to")
                                        #merepe hi scale factor lagega
                                        bayes_prob = (computed_value)*(value)*(time_log)
                                        bayes_prob = bayes_prob/scale_factor[scale_index]
                                        scale_index = scale_index + 1
                                else:
                                        bayes_prob = (computed_value)*(value)*(time_log)
                                
                               
                                final_prob+=bayes_prob
                                
                         
                                
                                
                        shevat = sql_query2(''' SELECT name from 
                                product_table where product_id = ? ''', (pro_id,))
                        every_list = [shevat[0][0], final_prob]
                        
                        result_list.append(every_list)
                        
                        
        #                if final_prob > max_value:
        #                        max_value = final_prob
        #                        final_id = pro_id
                     
                #ab we have that product with us. Lets see kya aaya 
                from operator import itemgetter
                result_list = sorted(result_list, key=itemgetter(1))
                
                return jsonify(result_list[-1])
        
        else:   
                return jsonify("Damn")

@app.route('/deleteHistory', methods=["DELETE"])
def deleteData():
        user_id = request.form['user_id']
        from functions.sqlquery import sql_delete
        results = sql_delete(''' DELETE from searches where user_id = ?''', (user_id,)) 
        return jsonify(results)


        

@app.route('/getBest', methods=["GET"])
def getBest():
        #should implement after set period
        from pyfcm import FCMNotification
        user_id = int(request.form['user_id'])
        from functions.sqlquery import sql_query2, sql_query
        results = sql_query2(''' SELECT search1_id, time_spent from searches where user_id = ?''',  (user_id,)) 
        results = results[-10:] 
        
        df = pd.read_csv('products.csv', usecols=['product_id', 'number_of_purchases','name', 'actual_price',
                        'original_price', 'discount_percentage', 'number_of_offers', 'seller_name'])[1:162]
        df["number_of_purchases"].fillna("0", inplace=True) 
        df2 = pd.read_csv('products.csv', usecols=['product_id', 'number_of_purchases'])[1:162]
        df2["number_of_purchases"].fillna("1", inplace=True) 
        
        main_data = df.values.tolist() 
        data2 = df2.values.tolist()
        
        for i in range(len(data2)):
                data2[i][0] = int(data2[i][0])
                data2[i][1] = int(data2[i][1])
        
        df3 = pd.read_csv('recommendations.csv')
        data3 = df3.values.tolist()
        for i in range(len(data3)):
                data3[i][0] = int(data3[i][0])
                data3[i][1] = int(data3[i][1])
                       
        total = 0 
        for i in range(len(data2)):
                total+=data2[i][1]  
                
        max_value = 0
        final_id = 1 
        result_list = []
        for i in range(len(data2)):
                pro_id = data2[i][0]   
                final_prob = 0
                every_result = []
                for j in range(len(results)):
                        second_id = results[j][0]
                        time_value = results[j][1]
                        #ab inka intersection nikaalna padta
                        intersect_value = sql_query2(''' SELECT factor from 
                        data_table where product_1_id = ? 
                        and product_2_id = ?''',  (pro_id,second_id)) 
                        
                        if not intersect_value:
                                value = 0.1
                        else:
                                value = intersect_value[0][0]
                                
                        #time aayega abhi bas
                              
                        quantity_value = sql_query2(''' SELECT number_of_purchases from 
                        product_table where product_id = ? ''', (second_id,))
                        quantity = quantity_value[0][0]
                       
                        # bayes_prob = probability of A intersection B * probability of purchase b
                        ratio = quantity/total
                        computed_value = math.log10(quantity)
                        time_log = math.log10(time_value)
                        #log of denominator jaruri nahi hai because nonetheless it manages
                        #itself by minusing itself from
                        
                        bayes_prob = (computed_value)*(value)*(time_log)
                        final_prob+=bayes_prob
                 
                        
                        
                shevat = sql_query2(''' SELECT name from 
                        product_table where product_id = ? ''', (pro_id,))
                every_result = [shevat[0][0], final_prob]
                
                result_list.append(every_result)
                
                if final_prob > max_value:
                        max_value = final_prob
                        final_id = pro_id
                       
        #prod_id = sql_query2(''' SELECT name from product_table where product_id = ?''', (final_id,))
        #prod_id = prod_id[0][0]  
        #return jsonify(prod_id)
        #ab we have that product with us. Lets see kya aaya 
        from operator import itemgetter
        result_list = sorted(result_list, key=itemgetter(1))
        
        
        time_id = str(get_time())
        time = time_id[0:2] + time_id[3:5]
            
        from functions.sqlquery import sql_edit_insert
        return_value = sql_edit_insert('''  INSERT INTO user_side_notifications (user_id, product_id, time_id) VALUES (?,?,?) ''', (user_id, final_id, time))
        #ye idhar hi end hoga 
        return jsonify(result_list)
        
@app.route('/getTime', methods=["GET"])
def get_time():
        #user_id = request.form['user_id']
        #df = pd.read_csv('time_data.csv', usecols=['send_time',	'response_time'	 , 'action',	'no_of_noti'])
        #data = df.values.tolist()
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
        return answer


@app.route('/sendBestNotifications', methods=["GET"])
def send_product_notification():
        from functions.sqlquery import sql_query2
        from pyfcm import FCMNotification
        user_id = request.form['user_id']
        prod_id = sql_query2(''' SELECT * from user_side_notifications where user_id = ?''', (user_id,))
        prod_id = prod_id[-1][1]
        #time = prod_id[0][1]
       # return jsonify(time)
        
        best_product = sql_query2(''' SELECT name from product_table where product_id =?''', (prod_id,))
        best_product = best_product[-1][0]
        
        time_id = get_time()
  
       # return "hora hai"
        push_service = FCMNotification(api_key="AAAAYNJto2I:APA91bEHdYbm2mhUfGfBIWseFzintaOJgJDifgSyzJdfcZrCyUdLD9XPwSKlX6IMaOeXNMkdTSs52mGKVequsJ_JtdZcq-6e15L9UzjHhs2JaMhcHmpDPgBu0D0bmPyXO2pqHa2Q0q0d")
        registration_id = "f8bLCD9kaoI:APA91bGN7uLHIZyefhLFBLa_HvHedRH7sq-o-LFKelIEkV9NS_ZGCrFVUePsySHjaeZZoWREfRkwF6LEcF-Z1vYpzfybfGJb7hMIwfdknVQzPcneWMsBpFsLDIlw4A7QAzFSS9vO9lVL"
        message_title = "We think you will love"
        message_body = best_product # + time_id
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return jsonify(result)
                
    

if __name__ == "__main__":
    app.run(debug=True)

