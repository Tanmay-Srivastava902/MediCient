'''HOLDS DATABASE SPECIFIC LOGIC'''

# all requires connection made with specifying database already
# requires root_conn 
def create_db(conn,db):
    query = f"create database {db} ; "
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
def show_db(conn,like_value=None):
    if like_value:
        query = f"show databases  Like %s ;"
        params = (like_value,)
    else:
        query = f"show databases;"
        params = tuple()
    
    cursor = conn.cursor()
    cursor.execute(query,params)
    for i in cursor.fetchall():
        print(i)
        
    conn.commit()
    cursor.close()
    pass
def is_db_exists(conn,db):
    query = f"Show databases ;"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(db_name1,),(db_name2,)]
    for db_tuple in result: # (db_name1)
        if db in db_tuple:
            print(True)
            return
    else:
        print(False)
# not to be accessed by the way for super protection
def __drop_db(conn,db):
    query = f"drop database {db};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    # from mysql.connector import connect
    # conn = connect(host = 'localhost',user='root',password='SecurePass@1201')
    # create_db(conn,'hello')
    # print()
    # show_db(conn)
    # print()
    # show_db(conn,like_value='T%')
    # print()
    # show_db(conn,like_value='%_schema')
    # print()
    # is_db_exists(conn,'medicient')
    # print()
    # is_db_exists(conn,'TESTs')
    # print()
    # __drop_db(conn,'hello')
    # print()
    # show_db(conn)

    # conn.close()
    pass
