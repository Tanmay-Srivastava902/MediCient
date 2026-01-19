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
    


def create_conn(user:str,pwd:str,host:str='localhost',use_db:bool=False,db:str=''):
    pass
def close_conn(conn,commit):
    pass

# mysql user 
# require executors (after login in mysql shell queries)
def create_mysql_user(root_conn,user,with_password,password):
    pass
def grant_privileges(root_conn,user,host,db,all,privileges_list,table:bool,table_name):
    pass
def delete_mysql_user(root_conn,user):
    pass
def configure_fresh_mysql_server(sudo_password):
    '''changes the auth plugin of root to password bases if user wants sets the password else leave default blank password'''
