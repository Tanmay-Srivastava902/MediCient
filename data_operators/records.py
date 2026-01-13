'''Handles the crud operation of data on table'''
# depend on cmd executor(utils) only 
# no dependency at all 
def insert_record(conn,table,column_order:tuple,values_list:list[tuple]):
    # sample INSERT INTO {table} ({column_order}) values (value);
    values= []
    params = []
    for value_tuple in values_list:
        # placeholder += len(value_tuple)
        values.append(f'{('%s',)*len(value_tuple)}'.replace('\'',''))  # f'(%s,%s)'
        params.extend(value_tuple)
    params = tuple(params)
    query = f"insert into {table} ({','.join(column_order)}) values {','.join(values)};"
    print(query,'\n',params)
    # cursor = conn.cursor()
    # cursor.execute(query,params)
    # conn.commit()
    # cursor.close()

def update_record(conn,table,set_clause:dict,where_clause:list[dict],with_or=False):
    # sample update table {table} set {set_clause} where {where_clause}
    # with_in : where_clause = [{'column':(value,value)}]
    set_list = [f"{column} = %s" for column in set_clause.keys()]
    set_values = [value for value in set_clause.values()] 

    where_list  = []
    where_values = []
    for where_dict in where_clause:
        # {column:value}
        for column,value in where_dict.items():

            if isinstance(value,(tuple,list)): 
                # if 'tuple' in "<class 'tuple'>" -> True
                in_clause = f"{('%s',)*len(value)}".replace('\'','') 
                # f"('%s','%s')".replace('\'','') -> f"(%s,%s)"
                where_list.append(f"{column} in {in_clause}")
                where_values.extend(value)
            else:
                # values in the where dict are not tuple just strings or numbers etc
                where_list.append(f"{column} = %s")
                where_values.append(value)

    params = tuple(set_values + where_values)
    conjuction = ' or ' if with_or else ' and '
    
    query = f"update  {table} set {','.join(set_list)} where {conjuction.join(where_list)} ;"
    print(query , '\n' , params)
    # cursor = conn.cursor()
    # cursor.execute(query,params)
    # conn.commit()
    # cursor.close()

def delete_record(conn,table,where_clause:list[dict] , with_or:bool=False):
    # sample INSERT INTO 
    where_list  = []
    where_values = []
    for where_dict in where_clause:
        # {column:value}
        for column,value in where_dict.items():

            if isinstance(value,(tuple,list)): 
                # if 'tuple' in "<class 'tuple'>" -> True
                in_clause = f"{('%s',)*len(value)}".replace('\'','') 
                # f"('%s','%s')".replace('\'','') -> f"(%s,%s)"
                where_list.append(f"{column} in {in_clause}")
                where_values.extend(value)
            else:
                # values in the where dict are not tuple just strings or numbers etc
                where_list.append(f"{column} = %s")
                where_values.append(value)
    params = tuple(where_values)
    conjuction = ' or ' if with_or else ' and '
    query = f"delete from {table} where {conjuction.join(where_list)};"
    print(query,params)
    # cursor = conn.cursor()
    # cursor.execute(query,params)
    # conn.commit()
    # cursor.close()

# version 5 with manual in + order by + like
def select_record(conn,table,columns_list:list,where_clause:list[dict]=[],with_or=False,with_like=False,order_by_column=None,order='asc',limit=None,offset=None):
    # user ['*'] for all columns
    
    query = f"select {','.join(columns_list)} from {table} "
    params = ()

    # if where in query 
    if where_clause or where_clause != [] :
        where_list  = []
        where_values = []
        for where_dict in where_clause:
            # {column:value}
            for column,value in where_dict.items():

                auto_detect_in = isinstance(value,(tuple,list)) # here instance value (type tuple ) is an instance of class tuple hence True else false
                auto_detect_like = True if '%' in value or '_' in value else False  # true if value ('_%s_','%_') is in value -> true 

                if auto_detect_in : 
                    in_clause = f"{('%s',)*len(value)}".replace('\'','') 
                    # f"('%s','%s')".replace('\'','') -> f"(%s,%s)"
                    where_list.append(f"{column} in {in_clause}")
                    where_values.extend(value)
                elif auto_detect_like and with_like : 
                    # like %s -> like 't%' ;
                    where_list.append(f"{column} like %s")
                    where_values.append(value)
                else:
                    # values in the where dict are not tuple just strings or numbers etc
                    where_list.append(f"{column} = %s")
                    where_values.append(value)

        params = tuple(where_values)
        conjuction = ' or ' if with_or else ' and '
        
        query += f" where {conjuction.join(where_list)} "
   
    # order by 
    if order_by_column:
        query +=  f" order by {order_by_column} {order} "

    # limit offset
    if limit and offset:
        query += f' limit {limit} offset {offset}'
    elif limit and not offset:
        query += f' limit {limit}'
 

    # execution
    print(query,'\n',params)
    cursor = conn.cursor()
    cursor.execute(query,params)
    result = cursor.fetchall()
    for i in result :
        print(i)
    cursor.close()

    pass
if __name__ == '__main__':
    from mysql.connector import connect
    conn = connect(host = 'localhost',user='root',password='SecurePass@1201',db='information_schema')
    # # insert_record(conn,'user',('uname','uaddress'),[('hello','testing_address1'),('bye','testing_address3')])
    # update_record('conn','user',{'uaddress':'nyaipur','uname':'tested_now'},[{'uid':(16,17)},{'uname':('bye','hello')}],with_or=True)
    # delete_record(conn, 'user',where_clause=[{'uid' : 3},{'uid': 10}],with_or=False) # not deleted (3 and 10) 
    # delete_record('conn', 'user',where_clause=[{'uid' : (3,6)},{'uid': 10}],with_or=True) # deleted 10  (3 or 10) 
    # delete_record(conn, 'user',where_clause=[{'uid' : 7},{'uid': 15}],with_or=True)# deleted both 7 and 15
    # insert_record(conn,'user',('uname','uid','uaddress'),[('tanmay',10,'nyaipur'),('shruti',15,'jaipur')]) # inserted 2 records in table users
    # insert_record(conn,'user_test',('uname','uid'),[('tanmay',10,),('shruti',15)]) # inserted 2 record in table user_test (leaving tid to A_I)
    # select_record('conn','user',['*'])
    # select_record('conn','user',['uname','uaddress'])
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':15},{'uid':19}],with_or=True)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':15},{'uid':19}],with_or=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':15},{'uid':19}],with_or=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':(13,14)},{'uname':('bye','shruti')}],with_or=False,with_in=True)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':(13,14)},{'uname':('bye','shruti')}],with_or=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':12},{'uname':('bye','shruti')}],with_or=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':(14,56)},{'uname':'shruti'}],with_or=False,order_by_column='uid')
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uid':(14,56)},{'uname':'shruti'}],with_or=False,order_by_column='uid',order='desc')
    # select_record(conn,'user',['uname','uaddress'],where_clause=[{'uaddress':'nyaipur'},{'uname':'d\\_%'}],with_or=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uaddress':'nyaipur'},{'uname':('t%',5)}],with_or=True ,with_like=False)
    # select_record('conn','user',['uname','uaddress'],where_clause=[{'uaddress':('nyaipur','wrong')},{'uname':'t%'}],with_or=True,order_by_column='uid',order='desc')
    # select_record(conn,'user',['uname','uaddress'],where_clause=[{'uaddress':('nyaipur','wrong')},{'uname':'t%'}],with_or=True,order_by_column='uid',order='desc',offset=3)
    # select_record(conn,'user',['uname','uaddress'],where_clause=[{'uaddress':('nyaipur','wrong')},{'uname':'t%'}],with_or=True,order_by_column='uid',order='desc',limit=2 , offset=3)
    # select_record(conn,'user',['*'],where_clause=[{'uid': 'between 10 and 17' }],with_or=True,order_by_column='uid',order='desc',limit=5 , offset=2)
    select_record(conn,'TABLE_CONSTRAINTS',['*'],[{'CONSTRAINT_NAME':'fk_user_patient'},{'TABLE_NAME':'patient'}])

    # conn.close()
    pass