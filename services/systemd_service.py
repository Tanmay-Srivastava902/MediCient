'''MANAGES SYSTEM SERVICES'''
# independent  (no sudo password needed)
import utils
from results import Result
def get_service_status(service):
    '''
    Retrieves the status of a systemd running service
    Args:
        service : name of service to handle
    Returns:
        Result : self.data = returncode [0,1,3,4]
    '''
    try:
        cmd = ['systemctl','status',service]
        result = utils.system_executor(
            command=cmd,
            sudo_access=False,
            need_output=True
        )
        if result is  None:
            return Result(
                success=False,
                error_code=100,
                error_msg=f"could not execute please provide sudo password"
            )
        return Result(
            success=True,
            data=result.returncode
        )
    except Exception as e :
        return Result(
            success=False,
            error_code=200,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )

# requires password (uses cmd executor)
def start_service(service,sudo_password):
    '''
    Starts The  systemd  service
    Args:
        service : name of service to handle
    Returns:
        Result : service started if result.returncode is 0 else 301 could not start 302 Not installed 
    '''
    try:
        cmd = ['systemctl','start',service]
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password,
            need_output=True
        )
        if result is  None:
            return Result(
                success=False,
                error_code=100,
                error_msg=f"could not execute please provide sudo password"
            )
        
        if result.returncode == 0:
            return Result(
                success=True,
                data=f"{service} started"
            )
        elif result.returncode == 1 :
            return Result(
            success=False,
            error_code=302,
            error_msg=f"{service} Could Not Be Started {result.stderr}"
        )
        else:
            return Result(
            success=False,
            error_code=303,
            error_msg=f"{service} Is Not Installed"
        )

    except Exception as e :
        return Result(
            success=False,
            error_code=200,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )


def stop_service(service,sudo_password):
    '''
    Stop The  systemd  service
    Args:
        service : name of service to handle
    Returns:
        Result : service Stopped if result.returncode is 0 else 301 could not Stop 302 Not installed 
    '''
    try:
        cmd = ['systemctl','stop',service]
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password,
            need_output=True
        )
        if result is  None:
            return Result(
                success=False,
                error_code=100,
                error_msg=f"could not execute please provide sudo password"
            )
        
        if result.returncode == 0:
            return Result(
                success=True,
                data=f"{service} Stopped"
            )
        elif result.returncode == 1 :
            return Result(
            success=False,
            error_code=301,
            error_msg=f"{service} Could Not Be Stopped {result.stderr}"
        )
        else:
            return Result(
            success=False,
            error_code=303,
            error_msg=f"{service} Is Not Installed"
        )

    except Exception as e :
        return Result(
            success=False,
            error_code=200,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )


def restart_service(service,sudo_password):
    '''
    Restarts The  systemd  service
    Args:
        service : name of service to handle
    Returns:
        Result : service restarted if result.returncode is 0 else 301 could not restart 302 Not installed 
    '''
    try:
        cmd = ['systemctl','start',service]
        result = utils.system_executor(
            command=cmd,
            sudo_access=True,
            sudo_password=sudo_password,
            need_output=True
        )
        if result is  None:
            return Result(
                success=False,
                error_code=100,
                error_msg=f"could not execute please provide sudo password"
            )
        
        if result.returncode == 0:
            return Result(
                success=True,
                data=f"{service} restarted"
            )
        elif result.returncode == 1 :
            return Result(
            success=False,
            error_code=302,
            error_msg=f"{service} Could Not Be restarted {result.stderr}"
        )
        else:
            return Result(
            success=False,
            error_code=303,
            error_msg=f"{service} Is Not Installed"
        )

    except Exception as e :
        return Result(
            success=False,
            error_code=200,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )




