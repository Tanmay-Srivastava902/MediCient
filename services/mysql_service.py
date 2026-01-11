'''CONTAINS MYSQL SERVER RELATED FUNCTIONS'''
# mysql server
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
def _get_root_plugin():
    # '''gets the auth method of root (for newly installed mysql server)'''
    pass
def _change_mysql_password(root_conn,host,password):
    pass

def configure_fresh_mysql_server(sudo_password):
    '''changes the auth plugin of root to password bases if user wants sets the password else leave default blank password'''
    pass

def save_mysql_password(root_conn,host,password):
    pass
def create_conn(host,user,pwd,use_db,db):
    pass
def execute_query(conn,query,params,sudo_access):
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
