'''CONTAINS MYSQL SERVER RELATED FUNCTIONS'''
# mysql server
from mysql.connector import connect , ProgrammingError,InterfaceError,IntegrityError
import utils
from results import Result
# may require package_manager
def _install_mysql_server():
    pass
# may require service_manager
def _check_mysql_server():
    pass
def _start_mysql_server():
    pass
def _stop_mysql_server():
    pass

# requires system executor (subprocess) and session
# mysql root 
def _get_root_plugin(root_conn):
    # '''gets the auth method of root (for newly installed mysql server)'''
    try:
        query = F"SELECT plugin FROM mysql.user where user = %s;"
        params = ('root',)
        result = utils.mysql_executor(root_conn,query,params)
        if result is None:
            return Result(
            success=False,
            error_code=100,
            error_msg=f"could not execute : Select queries insert or update query detected"
        )
        # found plugin
        return Result(
            success=True,
            data=result[0] # result = ('auth_plugin',) -> auth_plugin
        )
    # not found
    except Exception as e:
        return Result(
            success=False,
            error_code=300,
            error_msg=f"Unknown Error {str(e).strip()}"
        )
        
    
def _change_mysql_native_password(root_conn,new_password:str,host:str='localhost'):
    '''changes mysql root user password'''
    try:
        query = F"ALTER USER 'root'@{host} IDENTIFIED WITH mysql_native_password BY %s;"
        params = (new_password,)
        utils.mysql_executor(root_conn,query,params)
        # password changed
        return Result(
            success=True,
            data=f"Mysql Password Changed"
        )
    except Exception as e:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"could not execute {str(e).strip()}"
        )
    


def create_conn(
        user:str='root',
        password:str='',
        host:str='localhost',
        use_db:bool=False,
        db:str=''
    ):
    '''
    Creates a connection with the mysql server from the given user root connection by default with the blank password default else the password provided
    
    :param user: username of connection default [root]
    :type user: str
    :param pwd: password for user default [blank]
    :type pwd: str
    :param host: mysql host default [localhost]
    :type host: str
    :param use_db: true for using  db else false default[false]
    :type use_db: bool
    :param db: db_name for use_db = True
    :type db: str
    :returns MysqlConnectionObject: the object used further 
    :returns None: when db is not provided for use_db = True
    '''
    if use_db and not db:
        return None # please provide db for use_db=true
    
    # with db 
    if use_db:
        return connect(host=host,user=user,password=password,database=db)
    
    # default 
    return connect(host=host,user=user,password=password)



def close_conn(conn,commit:bool=True):
    '''
    Closes the mysql connection
    
    :param conn: MysqlConnectionObject to close 
    :param commit: wether to commit before close or not 
    '''
    if not commit :
        return conn.close()
    conn.commit()
    return conn.close()
def flush_privileges(root_conn):
    '''
    Docstring for flush_privileges
    
    :param conn: connection for which to flush privileges
    '''
    try:

        query = f"FLUSH PRIVILEGES;"
        # execution
        result =  utils.mysql_executor(conn=root_conn,query=query)
        if result is not  None:
           return Result(
                success=False,
                error_code=100,
                error_msg=f"Wrong Query Insert/Update Detected During User Flushing Privileges"
            )
        # if result is none successful Execution
        return Result(
            success=True,
            data=f"Privileges Reloaded"
        )
    except Exception as e:
         return Result(
                success=False,
                error_code=200,
                error_msg=f"Unknown Error : {str(e).strip()}"
            )

    

# mysql user 
# require executors (after login in mysql shell queries)
def create_mysql_user(
        root_conn,
        user:str,
        host:str='localhost',
        with_password:bool=False,
        password:str=''
    )-> Result:
    '''
    Docstring for create_mysql_user
    
    :param root_conn: the connection made using root account 
    :param user: username for  the user to create 
    :type user: str
    :param with_password: wether to set password for the user or not 
    :type with_password: bool
    :param password: password to set for the given user during creation[if with_password = True]
    '''
    try:
        # params check
        if with_password and not password:
            return Result(
                success=False,
                error_code=200,
                error_msg=f"Password Not Provided"
            )
        
        # preparing query 
        if with_password:
            query = f"CREATE USER IF NOT EXISTS '{user}'@'{host}' IDENTIFIED BY %s ;"
            params = (password,)
        else:
            query = f"CREATE USER '{user}'@'{host}';"
            params = tuple()
        # execution
        result =  utils.mysql_executor(conn=root_conn,query=query,params=params)
        if result is not  None:
           return Result(
                success=False,
                error_code=100,
                error_msg=f"Wrong Query Insert/Update Detected During User Creation"
            )
        # if result is none successful Execution
        return Result(
            success=True,
            data=f"{user} Create Successfully"
        )
    except Exception as e:
         return Result(
                success=False,
                error_code=200,
                error_msg=f"Unknown Error : {str(e).strip()}"
            )


def grant_privileges(
        root_conn,
        user:str,
        object_name:str,
        host:str='localhost',
        all_privileges:bool=False,
        privileges_list:list=[]
    )-> Result:
    '''
    Docstring for grant_privileges
    
    :param root_conn: MysqlCOnnectionObject from root account
    :param user: Description
    :type user: str
    :param object_name: name of the object on which the privileges are to be given eg-[**database.table**] 
    :type object_name: str
    :param host: hostname from which the user is connected default [**localhost**]
    :type host: str
    :param all_privileges: wether to provide all privileges to the given user or not default [**False**] 
    :type all_privileges: bool
    :param privileges_list: list of privileges to provide to the given user eg- ['privilege1','privilege2']
    :type privileges_list: list
    '''
    try:
        # params check
        if not all_privileges and not privileges_list:
            return Result(
                success=False,
                error_code=200,
                error_msg=f"Please Provide privilege list for all_privileges = False"
            )
        
        # generating query
        privileges = 'ALL PRIVILEGES' if all_privileges else ','.join(privileges_list) 
        query = f"GRANT {privileges} ON {object_name} TO '{user}'@'{host}';"
        
        # execution
        result =  utils.mysql_executor(conn=root_conn,query=query)
        if result is not  None:
           return Result(
                success=False,
                error_code=100,
                error_msg=f"Wrong Query Insert/Update Detected During User Creation"
            )
        
        # if result is none successful Execution
        return Result(
            success=True,
            data=f"Granted {privileges} to {user}"
        )
    except Exception as e:
         return Result(
                success=False,
                error_code=200,
                error_msg=f"Unknown Error : {str(e).strip()}"
            )

    
def delete_mysql_user(
        root_conn,
        user:str,
        host:str='localhost'
    )->Result:
    '''
    Docstring for delete_mysql_user
    
    :param root_conn: the connection made using root account 
    :param user: username for mysql user to delete
    :type user: str
    :param host: hostname default ['localhost']
    '''
    try:

        query = f"DROP USER IF EXISTS '{user}'@'{host}';"
        params = tuple()
        
        # execution
        result =  utils.mysql_executor(conn=root_conn,query=query,params=params)
        if result is not  None:
           return Result(
                success=False,
                error_code=100,
                error_msg=f"Wrong Query Insert/Update Detected During User Deletion"
            )
        # if result is none successful Execution
        return Result(
            success=True,
            data=f"{user} Deleted Successfully"
        )
    except Exception as e:
         return Result(
                success=False,
                error_code=200,
                error_msg=f"Unknown Error : {str(e).strip()}"
            )
#==============================
# Fresh Serve Setup 
#==============================
def configure_fresh_mysql_server(sudo_password):
    '''changes the auth plugin of root to password bases if user wants sets the password else leave default blank password'''
    