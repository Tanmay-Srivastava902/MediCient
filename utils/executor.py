'''EXECUTE COMMANDS AND QUERIES'''
def system_executor(command:list,need_output=True,sudo_access:bool=False,sudo_password=None):
    '''runs the given cmd in shell returns CompletedProcess Else None if sudo password is missing in sudo commands'''
    import subprocess 

    if sudo_access and not sudo_password:
        return None
    elif sudo_access and sudo_password :
        cmd_with_sudo  = ['sudo','-S'] + command
        output  = subprocess.run(
                                cmd_with_sudo,
                                input=sudo_password + '\n',
                                capture_output=need_output,
                                text=need_output
                                )
    else:
        output  =  subprocess.run(
                                command,
                                capture_output=need_output,
                                text=need_output
                                )
    
    return output
    
def mysql_executor(conn,query:str,params:tuple=()) -> list[tuple] | None:
    '''runs the given cmd in shell returns Result of cmd cursor.fetchall()'''
    from mysql.connector import connect
    cursor = conn.cursor() 
    cursor.execute(query,params)
    
    if query.split()[0].lower() in ['select','show','describe','desc','explain']:
        return cursor.fetchall()
    else :
        return None


def python_executor(command:list,run_module=False,interactive_mode=False,need_output=True):
    '''[**returns none if both args found true**][**use capture output false for interactive window**]uses run_module = True for module else DEFAULT command will be executed in script mode
    use interactive_mode for scripts as interactive shell'''
    import subprocess
    if run_module and interactive_mode:
        return None
    if run_module :
        python_command = ['python3','-m'] + command
    elif interactive_mode:
        python_command = ['python3','-i'] + command
    else:
        python_command = ['python3'] + command
    
    return subprocess.run(
                        python_command,
                        capture_output=need_output,
                        text=need_output
    )
    



if __name__ == "__main__":
    print(system_executor(['true']))