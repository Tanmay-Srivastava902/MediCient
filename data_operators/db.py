'''HOLDS DATABASE SPECIFIC LOGIC'''
from mysql.connector.errors import DatabaseError,ProgrammingError,InterfaceError,Error
from mysql.connector.abstracts import MySQLCursorAbstract
from utils import executors
import errors
# all requires connection made with specifying database already
# requires root_conn 
def create_db(cursor:MySQLCursorAbstract,db)->None:
    try:
        query = f"create database {db} ; "
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e :
        raise errors.DBError(f'could not Create Database :{str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e :
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e : 
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def show_db(cursor:MySQLCursorAbstract,like_value=None)->list[str]:
    try:
        if like_value:
            query = f"show databases  Like %s ;"
            params = (like_value,)
        else:
            query = f"show databases;"
            params = tuple()
        result = executors.mysql_executor(cursor,query,params)
        return [db[0] for db in result]
    except DatabaseError as e :
        raise errors.DBError(f'could not show database: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e :
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e : 
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

def is_db_exists(cursor:MySQLCursorAbstract,db:str)->bool:
    try:
        query = f"Show databases ;"
        result = executors.mysql_executor(cursor,query) # [(db_name1,),(db_name2,)]
        db_list = [db_tuple[0] for db_tuple in result]
        return db in db_list 
    except DatabaseError as e :
        raise errors.DBError(f'could not tell existence: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e :
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e : 
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

# not to be accessed by the way for super protection
def __drop_db(cursor:MySQLCursorAbstract,db:str)->None:
    try:
        query = f"drop database {db};"
        executors.mysql_executor(cursor,query)
        return None
    except DatabaseError as e :
        raise errors.DBError(f'could not drop database: {str(e).strip()}')
    except (InterfaceError,ProgrammingError) as e :
        raise errors.DBConnectionError(f'could not connect : {str(e).strip()}')
    except Error as e : 
        raise errors.ExecutionError(f'Could not execute query : {str(e).strip()}')

# if __name__ == '__main__':
    # from mysql.connector import connect
    # conn = connect(host = 'localhost',user='root',password='SecurePass@1201')
    # create_db(cursor:MySQLCursorAbstract,'hello')
    # print()
    # show_db(conn)
    # print()
    # show_db(cursor:MySQLCursorAbstract,like_value='T%')
    # print()
    # show_db(cursor:MySQLCursorAbstract,like_value='%_schema')
    # print()
    # is_db_exists(cursor:MySQLCursorAbstract,'medicient')
    # print()
    # is_db_exists(cursor:MySQLCursorAbstract,'TESTs')
    # print()
    # __drop_db(cursor:MySQLCursorAbstract,'hello')
    # print()
    # show_db(conn)

    # conn.close()
    # pass
