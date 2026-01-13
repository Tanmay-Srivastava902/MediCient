
'''Handles the table structure'''

# database specific
def show_all_tables(conn):
    #  all table names in our table
    query = f"Show tables ;"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(table1,),(table2,)]
    for table_tuple in result: # (table1)
      print(table_tuple)
    pass
def is_table_exists(conn,table):
    query = f"Show tables ;"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(table1,),(table2,)]
    for table_tuple in result: # (table1)
        if table in table_tuple:
            print(True)
            return
    else:
        print(False)
def create_table(conn,table,struct):
    query = f"create table {table}({struct}) ; "
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

def _desc_table(conn , table):
    query = f"desc {table};"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(table1,),(table2,)]
    for table_tuple in result: # (table1)
      print(table_tuple)
    cursor.close()
    pass
def _show_create_table(conn,table): 

     #  all table names in our table
    query = f"Show create table {table} ;"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(table1,),(table2,)]
    for table_tuple in result: # (table1)
      print(table_tuple)
    cursor.close()
    pass # to find fk_values if lost

# takes conn from caller (depends on executor (utils))
def _alter_table(conn,table,remaining_query):
    # sample struct 'alter table {table} {remaining_query}
    query = f"alter table {table} {remaining_query}"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def _truncate_table(conn , table):
    query = f"truncate table {table};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

# alter specific (Required add / drop in query)
# no any existence required except the table itself
def _is_column_exists(conn,table,column):
    query = f"desc {table} ;"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall() # [(table1,),(table2,)]
    for table_tuple in result: # (table1)
        if column in table_tuple or table_tuple[0] == column:
            print(table_tuple[0])
            print(True)
            return
    else:
        print(False)
    pass

def _is_constraint_exists(root_conn,table,constraint_name):
    '''It Requires Root Connection Connected Without Using any database'''
    query = f"select * from information_schema.TABLE_CONSTRAINTS  where CONSTRAINT_NAME = %s and TABLE_NAME = %s;"
    params = (constraint_name,table)
    cursor = conn.cursor()
    print(query,params)
    cursor.execute(query,params)
    result = cursor.fetchall() # [(table1,),(table2,)]
    print(result)
    return len(result) > 0   # returns true if found else false

def rename_table(conn,old_name,new_name):
    query = f"alter table {old_name} rename to {new_name} ;"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

def change_auto_increment(conn,table,auto_increment_value):
    # sample 'auto_increment = value ' reset send to alter
    query = f"alter table {table} AUTO_INCREMENT = {auto_increment_value} ;"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass 
def _drop_table(conn,table):
    query = f"drop table {table};"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

# column specific
# no column existence required
def add_column(conn,table,new_column_config,after_column=None,first_in_table=False):
    #  add new column (whole name + config)
    query = f"alter table {table} add column {new_column_config} "
    
    # position of inserted column
    if after_column :
        query += f"AFTER {after_column}"
    elif first_in_table:
        query += f"FIRST"
    
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

# column existence also required
def modify_column(conn,table ,old_column_name,new_config):
    # change (column_config only ) 
    query = f"alter table {table} modify column {old_column_name} {new_config};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def change_column(conn,table,old_column_name,new_column_config):
    #  change (name + config ) 
    query = f"alter table {table} change column {old_column_name} {new_column_config};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def drop_column(conn,table,column):
      # change (column_config only ) 
    query = f"alter table {table} drop column {column};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

# constraints specific 
def _add_constraint(conn,table,constraint_name,constraint_config):
    #  sample alter table {table} add constraint {constraint_config}
    query = f"alter table {table} add constraint {constraint_name} {constraint_config};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass


def add_primary_key(conn,table,constraint_name , column):
    #sample  'primary key (name)' 
    query = f"alter table {table} add constraint {constraint_name} primary key {column};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def add_unique_key(conn,constraint_name,table,column):
    # sample 'unique (column)'
    query = f"alter table {table} add constraint {constraint_name} unique key {column};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def add_foreign_key(conn,table,fk_config_list:list[tuple]):

    # fk_name can be fk_{column_name} for easy access
    # fk_config_list  = [(constraint_name , key_column , reference_table , reference_column ) ]
    fk_statement_list = []
    for fk_config_tuple in fk_config_list: 
        #  (constraint_name , key_column , reference_table , reference_column ) 
        fk_config = f" add constraint {fk_config_tuple[0]} foreign key  ({fk_config_tuple[1]}) references {fk_config_tuple[2]}({fk_config_tuple[3]}) "
        fk_statement_list.append(fk_config)

    query = f"alter table {table} {','.join(fk_statement_list)};"
        
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def add_index(conn,index_name,table,column):
    # 
    query = f"alter table {table} add index {index_name} ({column});"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
    pass
def drop_primary_key(conn,table):
    #sample  'primary key' 
        #sample  'primary key (name)' 
    query = f"alter table {table} drop primary key ;"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def drop_unique_key(conn,table,constraint_name):
    # sample 'unique (column)' 
    query = f"alter table {table} drop  index  {constraint_name};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def drop_foreign_key(conn,table,fk_name):
    #  foreign key (column) references (references)
    # fk_name can be fk_{column_name} for easy access
    query = f"alter table {table} drop foreign key {fk_name};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass
def drop_index(conn,table,index_name):
    #  'index {column}
    query = f"alter table {table} drop index  {index_name};"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    pass

# defaults 
def add_default(conn,table ,column,column_data_type,default_value):
    query = f"alter table {table} modify column {column} {column_data_type} default %s;"
    params = (default_value,)
    print(query,params)
    cursor = conn.cursor()
    cursor.execute(query,params)
    conn.commit()
    cursor.close()
def drop_default(conn,table ,column):
    query = f"alter table {table} alter column {column} drop default;"
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    
if __name__ == '__main__':
        from mysql.connector import connect
        conn = connect(host='localhost', user='root', password='SecurePass@1201',database='TEST')
#         print("--- Running full table management test suite ---")
#         # 1. Create table
#         create_table(conn, 'test_table', 'id int primary key, name varchar(50)')
#         # 2. Show all tables
#         show_all_tables(conn)
#         # 3. Check table exists
#         is_table_exists(conn, 'test_table')
#         # 4. Describe table
#         _desc_table(conn, 'test_table')
#         # 5. Show create table
#         _show_create_table(conn, 'test_table')
#         # 6. Add column
#         add_column(conn, 'test_table', 'extra_col int')
#         # 7. Modify column
#         modify_column(conn, 'test_table', 'extra_col', 'int default 42')
#         # 8. Change column (rename)
#         change_column(conn, 'test_table', 'extra_col', 'renamed_col int')
#         # 9. Add unique key
#         add_unique_key(conn, 'uk_name', 'test_table', '(name)')
#         # 10. Add index
#         add_index(conn, 'idx_name', 'test_table', 'name')
#         # 11. Add default value
#         add_default(conn, 'test_table', 'name', 'varchar(50)', 'default_name')
#         # 12. Drop default value
#         drop_default(conn, 'test_table', 'name')
#         # 13. Add constraint (check)
#         _add_constraint(conn, 'test_table', 'chk_id_positive', 'check (id > 0)')
#         # 14. Drop index
#         drop_index(conn, 'test_table', 'idx_name')
#         # 15. Drop unique key
#         drop_unique_key(conn, 'test_table', 'uk_name')
#         # 16. Drop column
#         drop_column(conn, 'test_table', 'renamed_col')
#         # 17. Truncate table
#         _truncate_table(conn, 'test_table')
#         # 18. Drop table
#         # _drop_table(conn, 'test_table')
#         print("--- Table management test suite complete ---")
        print(_is_constraint_exists(conn,'test2','test2_ibfk_1'))
        show_all_tables(conn)
        conn.close()