'''EXECUTE COMMANDS AND QUERIES - Complete Executor Layer'''

def system_executor(command, need_output=True, sudo_access=False, sudo_password=None):
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
    import subprocess
    
    if sudo_access and not sudo_password:
        print("❌ sudo_password required for sudo commands")
        return None
    
    if sudo_access:
        cmd_with_sudo = ['sudo', '-S'] + command
        return subprocess.run(
            cmd_with_sudo,
            input=f"{sudo_password}\n",
            capture_output=need_output,
            text=need_output
        )
    else:
        return subprocess.run(
            command,
            capture_output=need_output,
            text=need_output
        )


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


def mysql_executor(conn, query, params=()):
    """
    Execute MySQL queries
    
    Args:
        conn: MySQL connection object
        query: SQL query string
        params: Tuple of parameters for parameterized queries
    
    Returns:
        list[tuple]: For SELECT queries
        None: For other queries (INSERT/UPDATE/DELETE)
    
    Examples:
        # SELECT
        rows = mysql_executor(conn, "SELECT * FROM users WHERE id = %s", (5,))
        
        # INSERT
        mysql_executor(conn, "INSERT INTO users (name) VALUES (%s)", ('John',))
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    # Check if it's a query that returns data
    first_word = query.strip().split()[0].lower() 
    if first_word in ['select', 'show', 'describe', 'desc', 'explain']:
        result = cursor.fetchall()
        cursor.close()
        return result
    else:
        # For INSERT/UPDATE/DELETE
        conn.commit()
        cursor.close()
        return None


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    print("="*50)
    print("EXECUTOR LAYER TEST SUITE")
    print("="*50)
    
    # Test 1: System executor
    print("\n[TEST 1] System Executor - Simple command")
    result = system_executor(['echo', 'hello'])
    if result:
        print(f"✓ Return code: {result.returncode}")
        print(f"  Output: {result.stdout.strip()}")
    
    # Test 2: Python executor - Script mode
    print("\n[TEST 2] Python Executor - Script mode")
    result = python_executor(['-c', 'print(30 > 20)'])
    if result:
        print(f"✓ Return code: {result.returncode}")
        print(f"  Output: {result.stdout.strip()}")
    
    # Test 3: Python executor - Module mode
    print("\n[TEST 3] Python Executor - Module mode")
    result = python_executor(['pip', 'list'], run_module=True)
    if result:
        print(f"✓ Return code: {result.returncode}")
        print(f"  Output: {result.stdout[:100]}...")  # First 100 chars
    
    # Test 4: Both flags (should fail)
    print("\n[TEST 4] Python Executor - Both flags (should fail)")
    result = python_executor(['test'], run_module=True, interactive_mode=True)
    if not result:
        print("✓ Correctly rejected both flags")
    
    # Test 5: System executor without sudo password (should fail)
    print("\n[TEST 5] System Executor - Missing sudo password")
    result = system_executor(['systemctl', 'status', 'mysql'], sudo_access=True)
    if not result:
        print("✓ Correctly rejected missing password")
    
    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50)
    pass
