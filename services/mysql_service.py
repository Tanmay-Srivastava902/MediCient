'''CONTAINS ALL MYSQL SERVER RELATED FUNCTIONS'''

from mysql.connector import connect, ProgrammingError, InterfaceError
import utils
import errors

# ============================================================================
# SERVER MANAGEMENT
# ============================================================================

def _install_mysql_server(sudo_password: str) -> None:
    '''Install MySQL Server'''
    try:
        cmd = ['apt', 'install', '-y', 'mysql-server']
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password
        )
        if result.returncode != 0:
            raise errors.InstallError(f"could not install : {result.stderr}")
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def _mysql_server_status() -> int:
    '''
    Check MySQL Server Status
    
    Returns:
        returncode: 0 if running, else if not running
    '''
    try:
        cmd = ['systemctl', 'status', 'mysql']
        result = utils.system_executor(command=cmd, sudo_access=False)
        return result.returncode
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def _start_mysql_server(sudo_password: str) -> None:
    '''Start MySQL Server'''
    try:
        cmd = ['systemctl', 'start', 'mysql']
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password
        )
        if result.returncode != 0:
            raise errors.ServiceError(f"could not start : {result.stderr}")
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def _stop_mysql_server(sudo_password: str) -> None:
    '''Stop MySQL Server'''
    try:
        cmd = ['systemctl', 'stop', 'mysql']
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password
        )
        if result.returncode != 0:
            raise errors.ServiceError(f"could not stop : {result.stderr}")
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def _restart_mysql_server(sudo_password: str) -> None:
    '''Restart MySQL Server'''
    try:
        cmd = ['systemctl', 'restart', 'mysql']
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password
        )
        if result.returncode != 0:
            raise errors.ServiceError(f"could not restart : {result.stderr}")
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


# ============================================================================
# CONNECTION MANAGEMENT
# ============================================================================

def create_conn(
    user: str = 'root',
    password: str = '',
    host: str = 'localhost',
    db: str = ''
):
    '''
    Create MySQL connection
    
    Args:
        user: MySQL username (default: root)
        password: MySQL password (default: empty)
        host: MySQL host (default: localhost)
        db: Database name (default: empty - no specific db)
    
    Returns:
        MySQL connection object
    
    Raises:
        AuthError: If authentication fails
        MysqlConnectionError: If connection fails
    '''
    try:
        if db:
            return connect(host=host, user=user, password=password, database=db)
        else:
            return connect(host=host, user=user, password=password)
    except (InterfaceError, ProgrammingError):
        raise errors.AuthError(f"Wrong password for user '{user}'")
    except Exception as e:
        raise errors.MysqlConnectionError(f"could not connect : {str(e).strip()}")


def close_conn(conn, commit: bool = True) -> None:
    '''
    Close MySQL connection
    
    Args:
        conn: MySQL connection object
        commit: Whether to commit before closing (default: True)
    '''
    if commit:
        conn.commit()
    conn.close()


# ============================================================================
# USER OPERATIONS
# ============================================================================

def create_mysql_user(
    root_conn,
    user: str,
    host: str = 'localhost',
    password: str = ''
) -> None:
    '''
    Create MySQL user
    
    Args:
        root_conn: MySQL connection with root privileges
        user: Username to create
        host: Host permission (default: localhost)
        password: User password (default: empty - no password)
    
    Raises:
        ExecutionError: If user creation fails
    '''
    try:
        if password:
            query = f"CREATE USER IF NOT EXISTS '{user}'@'{host}' IDENTIFIED BY %s ;"
            params = (password,)
        else:
            query = f"CREATE USER '{user}'@'{host}';"
            params = tuple()
        
        utils.mysql_executor(conn=root_conn, query=query, params=params)
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def grant_privileges(
    root_conn,
    user: str,
    object_name: str,
    host: str = 'localhost',
    all_privileges: bool = False,
    privileges_list: list = []
) -> None:
    '''
    Grant privileges to MySQL user
    
    Args:
        root_conn: MySQL connection with root privileges
        user: Username to grant privileges to
        object_name: Target (e.g., 'database.*' or 'database.table')
        host: Host permission (default: localhost)
        all_privileges: Grant ALL PRIVILEGES (default: False)
        privileges_list: List of specific privileges if all_privileges=False
    
    Raises:
        InvalidArgumentError: If privileges not specified properly
        ExecutionError: If privilege grant fails
    '''
    if not all_privileges and not privileges_list:
        raise errors.InvalidArgumentError("Provide privilege list when all_privileges=False")
    
    try:
        privileges = 'ALL PRIVILEGES' if all_privileges else ','.join(privileges_list)
        query = f"GRANT {privileges} ON {object_name} TO '{user}'@'{host}';"
        utils.mysql_executor(conn=root_conn, query=query)
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def delete_mysql_user(
    root_conn,
    user: str,
    host: str = 'localhost'
) -> None:
    '''
    Delete MySQL user
    
    Args:
        root_conn: MySQL connection with root privileges
        user: Username to delete
        host: Host permission (default: localhost)
    
    Raises:
        ExecutionError: If user deletion fails
    '''
    try:
        query = f"DROP USER IF EXISTS '{user}'@'{host}';"
        utils.mysql_executor(conn=root_conn, query=query)
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


# ============================================================================
# PASSWORD OPERATIONS
# ============================================================================

def verify_mysql_password(
    user: str,
    password: str,
    host: str = "localhost",
) -> bool:
    '''
    Verify MySQL user credentials
    
    Args:
        user: MySQL username
        password: Password to verify
        host: MySQL host (default: localhost)
    
    Returns:
        True if credentials valid, False otherwise
    
    Raises:
        AuthError: If unexpected error during authentication check
    '''
    try:
        connect(user=user, password=password, host=host)
        return True
    except (InterfaceError, ProgrammingError):
        return False
    except Exception as e:
        raise errors.AuthError(f"Could not authenticate : {str(e).strip()}")


def _change_mysql_root_password(
    root_conn,
    new_password: str,
    host: str = 'localhost'
) -> None:
    '''
    Change MySQL root user password
    
    Args:
        root_conn: MySQL connection with root privileges
        new_password: New password to set
        host: MySQL host (default: localhost)
    
    Raises:
        ExecutionError: If password change fails
    '''
    try:
        query = f"ALTER USER 'root'@'{host}' IDENTIFIED WITH mysql_native_password BY %s;"
        params = (new_password,)
        utils.mysql_executor(root_conn, query, params)
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


# ============================================================================
# PRIVILEGE MANAGEMENT (Administrative)
# ============================================================================

def _get_root_plugin(root_conn) -> str:
    '''
    Get authentication method of root user
    
    Args:
        root_conn: MySQL connection with root privileges
    
    Returns:
        Authentication plugin name (e.g., 'mysql_native_password')
    
    Raises:
        ExecutionError: If query execution fails
    '''
    try:
        query = "SELECT plugin FROM mysql.user WHERE user = %s;"
        params = ('root',)
        result = utils.mysql_executor(root_conn, query, params)
        return result[0][0]  # result = [('auth_plugin',)] -> auth_plugin
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")


def flush_privileges(root_conn) -> None:
    '''
    Reload MySQL privileges (apply changes immediately)
    
    Args:
        root_conn: MySQL connection with root privileges
    
    Raises:
        ExecutionError: If execution fails
    '''
    try:
        query = "FLUSH PRIVILEGES;"
        utils.mysql_executor(conn=root_conn, query=query)
    except Exception as e:
        raise errors.ExecutionError(f"could not execute : {str(e).strip()}")