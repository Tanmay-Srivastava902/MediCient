# '''MANAGES SYSTEM SERVICES'''
import utils
import errors
#==============================================================================
# SYSTEMD (SYSTEMCTL) SERVICE
#==============================================================================
def service_status(service:str) -> int:
    '''
    Check  service Status
    returns returncode: int if found status [1,2,3,4...]
    '''

    cmd = ['systemctl', 'status', service]
    result = utils.system_executor(command=cmd, sudo_access=False)
    return result.returncode

def start__service(service:str,sudo_password: str) -> None:
    '''Start service'''
    
    cmd = ['systemctl', 'start', service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not start : {result.stderr}")

def stop__service(service:str,sudo_password: str) -> None:
    '''Stop  service'''
    cmd = ['systemctl', 'stop', service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not stop : {result.stderr}")

def restart__service(service:str,sudo_password: str) -> None:
    '''Restart service'''
    
    cmd = ['systemctl', 'restart',service]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.ServiceError(f"could not restart : {result.stderr}")
#===============================================================================
# APT SERVICES
#===============================================================================
#=================================
# package detection
# =================================
def _package_version(package: str) -> str:
    """
    Gets version of an installed package

    :params package: Package command name (e.g., 'python3', 'mysql')
    :returns package_version_info: str if found 
    :raises AptError: if could not check version 
    """
    cmd = [package, '--version']
    result = utils.system_executor(cmd)

    # Check command success
    if result.returncode != 0:
        raise errors.AptError(f"could not check version: {result.stderr}")
    return result.stdout # package version
    
def is_package_installed(package: str) -> bool:
    """
    Checks if a package is installed.
    :params package: Package command name (e.g., 'python3', 'mysql')
    :returns True: bool if found 
    
    """
    cmd = [package, '--version']
    result = utils.system_executor(cmd)
    return result.returncode == 0  # returns true or false 

# =================================
# APT PACKAGE MANAGEMENT
# =================================

def update_system_packages(sudo_password: str) -> None:
    """
    Updates APT package lists (apt update).
    
    :params sudo_password: User's sudo password
    :returns None: bool if updated 
    :raises AptError: if could not update packages 
"""
    cmd = ['apt', 'update','-y']
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.AptError(f"could not update packages: {result.stderr}")
    return None
        

def upgrade_system_packages(sudo_password: str) -> None:
    """
    Updates APT package lists (apt upgrade).
    
    :params sudo_password: User's sudo password
    :returns None: bool if upgrade 
    :raises AptError: if could not upgrade packages 
"""
    cmd = ['apt', 'upgrade','-y']
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.AptError(f"could not upgrade packages: {result.stderr}")
    return None
        

def install_system_package(sudo_password: str, package:str) -> None:
    """
    Installs a system package via APT.

    :params sudo_password: User's sudo password
    :params package: Package command name (e.g., 'python3', 'mysql')
    :returns None: bool if cannot install 
    :raises AptError: if could not install
    """
    cmd = ['apt', 'install','-y',package]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.AptError(f"could not install packages: {result.stderr}")
    return None
    

def uninstall_system_package(sudo_password: str, package:str) -> None:
    """
    Uninstalls a system package via APT.
    
    :params sudo_password: User's sudo password
    :params package: Package command name (e.g., 'python3', 'mysql')
    :returns None: bool if cannot uninstall 
    :raises AptError: if could not uninstall
    
    """
    cmd = ['apt', 'remove','-y',package]
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    if result.returncode != 0:
        raise errors.AptError(f"could not uninstall packages: {result.stderr}")
    return None

# =================================
# CONVENIENCE WRAPPER
# =================================

def ensure_package_installed(sudo_password: str, package: str) -> None:
    """
    Ensures a package is installed (installs if not already installed).
    :params package: Package command name (e.g., 'python3', 'mysql')
    :returns True: bool if found 
    """
    # Check if already installed
    if is_package_installed(package):
       return None
    # Install package
    install_system_package(sudo_password, package)
    return None



