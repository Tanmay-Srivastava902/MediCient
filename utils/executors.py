'''EXECUTE COMMANDS AND QUERIES - Complete Executor Layer'''
# NOTE remove this sudo_access flag  directly use sudo_password instead
import errors
import subprocess
def system_executor(
    command,
    sudo_access=False, 
    sudo_password:str=''
    )->subprocess.CompletedProcess:
    """
    Execute system commands
    
    Args:
        command: List of command parts ['ls', '-la']
        need_output: Capture stdout/stderr
        sudo_access: Run with sudo
        sudo_password: Required if sudo_access=True
    
    Returns:
        CompletedProcess: On success
        None: If sudo password missing
    
    Examples:
        system_executor(['ls', '-la'])
        system_executor(['systemctl', 'start', 'mysql'], 
                       sudo_access=True, sudo_password='pass')
    """
    try:
        if sudo_access:
            cmd = ['sudo', '-S'] + command
            # Include newline so sudo knows password is complete
            input_data = (sudo_password + '\n').encode()
        else:
            cmd = command
            input_data = None
        
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result
    
    except subprocess.TimeoutExpired as e:
        raise errors.ExecutionError(f"Command timeout: {str(e)}")
    except Exception as e:
        raise errors.ExecutionError(f"Execution failed: {str(e)}")

def python_executor(command, run_module=False, interactive_mode=False, need_output=True):
    """
    Execute Python commands/scripts/modules
    
    Args:
        command: List of command parts
        run_module: Use -m flag (python -m pip install)
        interactive_mode: Use -i flag (python -i script.py)
        need_output: Capture output (set False for interactive)
    
    Returns:
        CompletedProcess: On success
        None: If both run_module and interactive_mode are True
    
    Examples:
        # Script mode
        python_executor(['-c', 'print(30 > 20)'])
        
        # Module mode
        python_executor(['pip', 'install', 'package'], run_module=True)
        
        # Interactive mode
        python_executor(['script.py'], interactive_mode=True, need_output=False)
    """
    import subprocess
    
    # Can't be both module and interactive
    if run_module and interactive_mode:
        print("❌ Cannot use both run_module and interactive_mode")
        return None
    
    # Build command
    if run_module:
        python_command = ['python3', '-m'] + command
    elif interactive_mode:
        python_command = ['python3', '-i'] + command
    else:
        python_command = ['python3'] + command
    
    return subprocess.run(
        python_command,
        capture_output=need_output,
        text=need_output
    )

def mysql_executor(cursor, query, params=())->list[tuple]:
    """
    Execute MySQL queries
    
    Args:
        cursor: MySQLCursorAbstract
        query: SQL query string
        params: Tuple of parameters for parameterized queries
    
    Returns:
        list[tuple]: For SELECT queries
        []: '' For other queries (INSERT/UPDATE/DELETE)
    
    Examples:
        # SELECT
        rows = execute_query(conn, "SELECT * FROM users WHERE id = %s", (5,))
        
        # INSERT
        execute_query(conn, "INSERT INTO users (name) VALUES (%s)", ('John',))
    """
    cursor.execute(query, params)
    # Check if it's a query that returns data
    first_word = query.strip().split()[0].lower() 
    if first_word in ['select', 'show', 'describe', 'desc', 'explain']:
        result = cursor.fetchall()
        return result
    else:
        # For INSERT/UPDATE/DELETE
        return [tuple()] # return blank list[tuple]  
