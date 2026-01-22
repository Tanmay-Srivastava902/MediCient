# '''MANAGES SYSTEM SERVICES'''
import utils
import errors
def __service_status(service:str) -> int:
    '''
    Check  service Status
    returns returncode: int if found status [1,2,3,4...]
    '''

    cmd = ['systemctl', 'status', service]
    result = utils.system_executor(command=cmd, sudo_access=False)
    return result.returncode

def _start__service(service:str,sudo_password: str) -> None:
    '''Start service'''
    
    cmd = ['systemctl', 'start', service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not start : {result.stderr}")

def _stop__service(service:str,sudo_password: str) -> None:
    '''Stop  service'''
    cmd = ['systemctl', 'stop', service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not stop : {result.stderr}")

def _restart__service(service:str,sudo_password: str) -> None:
    '''Restart service'''
    
    cmd = ['systemctl', 'restart',service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not restart : {result.stderr}")




