
'''Handles the table structure'''
from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector.errors import DatabaseError,ProgrammingError,InterfaceError,Error
from utils import executors
import errors
# database specific
def show_all_tables(cursor:MySQLCursorAbstract)->list[str]:
    #  all table names in our table
    try:
        query = f"Show tables ;"
        result =  executors.mysql_executor(cursor,query) # [('user',), ('doctor',), ('patient',)]
        return [table[0] for table in result] # returning tables list
    except DatabaseError as e :
        raise errors.TableError(f'could not list tables: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e :
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e : 
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def is_table_exists(cursor:MySQLCursorAbstract,table:str)->bool:
    try:
        query = f"Show tables ;"
        result = executors.mysql_executor(cursor,query) 
        tables = [table[0] for table in result]
        return table in tables
    except DatabaseError as e:
        raise errors.TableError(f'could not check table existence: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def create_table(cursor:MySQLCursorAbstract,table,struct:str)->None:
    try:
        query = f"create table {table}({struct}) ; "
        result = executors.mysql_executor(cursor,query)
        return
    except DatabaseError as e:
        raise errors.TableError(f'could not create table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def _desc_table(cursor:MySQLCursorAbstract, table)->list[tuple]:
    try:
        query = f"desc {table};"
        return executors.mysql_executor(cursor,query)
    except DatabaseError as e:
        raise errors.TableError(f'could not describe table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

    
def _show_create_table(cursor:MySQLCursorAbstract,table:str)->str: 

    try:
        #  all table names in our table
        query = f"Show create table {table} ;"
        result = executors.mysql_executor(cursor,query) # ['table','struct']
        return result[0][1] # struct
    except DatabaseError as e:
        raise errors.TableError(f'could not show create table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
      # to find fk_values if lost

def _is_column_exists(cursor:MySQLCursorAbstract,table:str,column:str)->bool:
    try:
        query = f"desc {table} ;"
        result = executors.mysql_executor(cursor,query) # [('column1','type1') ,('column2','type2')]
        columns_list = [columns_tuple[0] for columns_tuple in result ] # ['column1','column2]
        return column in columns_list
    except DatabaseError as e:
        raise errors.TableError(f'could not check column existence: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def _is_constraint_exists(root_cursor,table,constraint_name)->bool:
    '''It Requires Root Cursor Connected Without Using any database'''
    try:
        query = f"select * from information_schema.TABLE_CONSTRAINTS  where CONSTRAINT_NAME = %s and TABLE_NAME = %s;"
        params = (constraint_name,table)
        result = executors.mysql_executor(root_cursor,query,params)
        return len(result) > 0   # returns true if found else false
    except DatabaseError as e:
        raise errors.TableError(f'could not check constraint: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

# takes conn from caller (depends on executor (utils))
def _alter_table(cursor:MySQLCursorAbstract,table,remaining_query)->None:
    try:
        # sample struct 'alter table {table} {remaining_query}
        query = f"alter table {table} {remaining_query}"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not alter table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
def _truncate_table(cursor, table:str)->None:
    try:
        query = f"truncate table {table};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not truncate table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
# alter specific (Required add / drop in query)
# no any existence required except the table itself

def rename_table(cursor:MySQLCursorAbstract,old_name:str,new_name:str)->None:
    try:
        query = f"alter table {old_name} rename to {new_name} ;"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not rename table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
def change_auto_increment(cursor:MySQLCursorAbstract,table:str,auto_increment_value:int)->None:
    try:
        # sample 'auto_increment = value ' reset send to alter
        query = f"alter table {table} AUTO_INCREMENT = {auto_increment_value} ;"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not change auto_increment: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def _drop_table(cursor:MySQLCursorAbstract,table:str)->None:
    try:
        query = f"drop table {table};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not drop table: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
# column specific
# no column existence required
def add_column(cursor:MySQLCursorAbstract,table:str,new_column_config:str)->None:
    try:
        #  add new column (whole name + config)
        query = f"alter table {table} add column {new_column_config};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add column: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

# column existence also required
def modify_column(cursor:MySQLCursorAbstract,table ,old_column_name,new_config)->None:
    try:
        # change (column_config only ) 
        query = f"alter table {table} modify column {old_column_name} {new_config};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not modify column: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
def change_column(cursor:MySQLCursorAbstract,table,old_column_name,new_column_config)->None:
    try:
        #  change (name + config ) 
        query = f"alter table {table} change column {old_column_name} {new_column_config};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not change column: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
def drop_column(cursor:MySQLCursorAbstract,table:str,column:str)->None:
    try:
        # change (column_config only ) 
        query = f"alter table {table} drop column {column};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not drop column: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    

# constraints specific 
def _add_constraint(cursor:MySQLCursorAbstract,table,constraint_name,constraint_config)->None:
    try:
        #  sample alter table {table} add constraint {constraint_config}
        query = f"alter table {table} add constraint {constraint_name} {constraint_config};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add constraint: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
def add_primary_key(cursor:MySQLCursorAbstract,table,constraint_name , column)->None:
    try:
        #sample  'primary key (name)' 
        query = f"alter table {table} add constraint {constraint_name} primary key {column};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add primary key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
def add_unique_key(cursor,constraint_name,table,column)->None:
    try:
        # sample 'unique (column)'
        query = f"alter table {table} add constraint {constraint_name} unique key {column};"
        executors.mysql_executor(cursor,query) 
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add unique key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
def add_foreign_key(cursor:MySQLCursorAbstract,table,fk_config_list:list[tuple])->None:
    try:
        '''fk_name can be fk_{column_name} for easy access
        # fk_config_list  = [(constraint_name , key_column , reference_table , reference_column ) ]'''
        fk_statement_list = []
        for fk_config_tuple in fk_config_list: 
            #  (constraint_name , key_column , reference_table , reference_column ) 
            fk_config = f" add constraint {fk_config_tuple[0]} foreign key  ({fk_config_tuple[1]}) references {fk_config_tuple[2]}({fk_config_tuple[3]}) "
            fk_statement_list.append(fk_config)
        query = f"alter table {table} {','.join(fk_statement_list)};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add foreign key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
def add_index(cursor,index_name,table,column)->None:
    try:
        query = f"alter table {table} add index {index_name} ({column});"
        executors.mysql_executor(cursor,query)
        return 
    except DatabaseError as e:
        raise errors.TableError(f'could not add index: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
def drop_primary_key(cursor:MySQLCursorAbstract,table:str)->None:
    try:
        #sample  'primary key' 
        #sample  'primary key (name)' 
        query = f"alter table {table} drop primary key ;"
        executors.mysql_executor(cursor,query)
        return
    except DatabaseError as e:
        raise errors.TableError(f'could not drop primary key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
def drop_unique_key(cursor:MySQLCursorAbstract,table,constraint_name)->None:
    try:
        # sample 'unique (column)' 
        query = f"alter table {table} drop  index  {constraint_name};"
        executors.mysql_executor(cursor,query)
        return 
    except DatabaseError as e:
        raise errors.TableError(f'could not drop unique key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def drop_foreign_key(cursor:MySQLCursorAbstract,table,fk_name)->None:
    try:
        #  foreign key (column) references (references)
        # fk_name can be fk_{column_name} for easy access
        query = f"alter table {table} drop foreign key {fk_name};"
        executors.mysql_executor(cursor,query)
        return
    except DatabaseError as e:
        raise errors.TableError(f'could not drop foreign key: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def drop_index(cursor:MySQLCursorAbstract,table,index_name)->None:
    try:
        #  'index {column}
        query = f"alter table {table} drop index  {index_name};"
        executors.mysql_executor(cursor,query)
        return 
    except DatabaseError as e:
        raise errors.TableError(f'could not drop index: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

# defaults 
def add_default(cursor:MySQLCursorAbstract,table ,column,column_data_type,default_value)->None:
    try:
        query = f"alter table {table} modify column {column} {column_data_type} default %s;"
        params = (default_value,)
        executors.mysql_executor(cursor,query,params)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not add default: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
def drop_default(cursor:MySQLCursorAbstract,table ,column)->None:
    try:
        query = f"alter table {table} alter column {column} drop default;"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e:
        raise errors.TableError(f'could not drop default: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e:
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e:
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')
    
    
# if __name__ == '__main__':
        # from mysql.connector import connect
        # conn = connect(host='localhost', user='root', word='Secure@1201',database='TEST')
#         print("--- Running full table management test suite ---")
#         # 1. Create table
#         create_table(cursor, 'test_table', 'id int primary key, name varchar(50)')
#         # 2. Show all tables
#         show_all_tables(cursor)
#         # 3. Check table exists
#         is_table_exists(cursor, 'test_table')
#         # 4. Describe table
#         _desc_table(cursor, 'test_table')
#         # 5. Show create table
#         _show_create_table(cursor, 'test_table')
#         # 6. Add column
#         add_column(cursor, 'test_table', 'extra_col int')
#         # 7. Modify column
#         modify_column(cursor, 'test_table', 'extra_col', 'int default 42')
#         # 8. Change column (rename)
#         change_column(cursor, 'test_table', 'extra_col', 'renamed_col int')
#         # 9. Add unique key
#         add_unique_key(cursor, 'uk_name', 'test_table', '(name)')
#         # 10. Add index
#         add_index(cursor, 'idx_name', 'test_table', 'name')
#         # 11. Add default value
#         add_default(cursor, 'test_table', 'name', 'varchar(50)', 'default_name')
#         # 12. Drop default value
#         drop_default(cursor, 'test_table', 'name')
#         # 13. Add constraint (check)
#         _add_constraint(cursor, 'test_table', 'chk_id_positive', 'check (id > 0)')
#         # 14. Drop index
#         drop_index(cursor, 'test_table', 'idx_name')
#         # 15. Drop unique key
#         drop_unique_key(cursor, 'test_table', 'uk_name')
#         # 16. Drop column
#         drop_column(cursor, 'test_table', 'renamed_col')
#         # 17. Truncate table
#         _truncate_table(cursor, 'test_table')
#         # 18. Drop table
#         # _drop_table(cursor, 'test_table')
#         print("--- Table management test suite complete ---")
        # print(_is_constraint_exists(cursor,'test2','test2_ibfk_1'))
        # show_all_tables(cursor)
        # conn.close()