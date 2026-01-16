"""Manages system package installation via APT (Debian/Ubuntu)"""

import utils
from results import Result


# ============================================================================
# PACKAGE DETECTION
# ============================================================================

def _package_version(package: str) -> Result:
    """
    Gets version of an installed package.
    
    Args:
        package: Package command name (e.g., 'python3', 'mysql')
    
    Returns:
        Result: Success with version string, or failure
    
    Note: Internal function - use is_package_installed() for simple checks
    """
    try:
        cmd = [package, '--version']
        result = utils.system_executor(cmd)
        
        # Handle executor failure
        if result is None:
            return Result(
                success=False,
                error_code=100,
                error_msg="Command execution failed"
            )
        
        # Check command success
        if result.returncode == 0:
            return Result(
                success=True,
                data=result.stdout.strip()  # Remove trailing newlines
            )
        else:
            return Result(
                success=False,
                error_code=100,
                error_msg=result.stderr.strip()
            )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e)}"
        )


def is_package_installed(package: str) -> bool:
    """
    Checks if a package is installed.
    
    Args:
        package: Package command name
    
    Returns:
        bool: True if installed, False otherwise
    
    Example:
        if is_package_installed('mysql'):
            print("MySQL is installed")
    """
    try:
        cmd = [package, '--version']
        result = utils.system_executor(cmd)
        return result is not None and result.returncode == 0
    except Exception:
        return False


# ============================================================================
# APT PACKAGE MANAGEMENT
# ============================================================================

def update_system_packages(sudo_password: str) -> Result:
    """
    Updates APT package lists (apt update).
    
    Args:
        sudo_password: User's sudo password
    
    Returns:
        Result: Success if update completed, failure otherwise
    
    Error Codes:
        100: Update command failed
    
    Example:
        result = update_system_packages(password)
        if result.ok:
            print("Package lists updated")
    """
    cmd = ['apt', 'update']
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    
    if result is None:
        return Result(
            success=False,
            error_code=100,
            error_msg="Update command failed to execute"
        )
    
    if result.returncode == 0:
        return Result(
            success=True,
            data="System package lists updated"
        )
    else:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"Update failed: {result.stderr.strip()}"
        )


def install_system_package(sudo_password: str, package: str, 
                          auto_yes: bool = True) -> Result:
    """
    Installs a system package via APT.
    
    Args:
        sudo_password: User's sudo password
        package: Package name to install
        auto_yes: Automatically answer 'yes' to prompts
    
    Returns:
        Result: Success if installed, failure otherwise
    
    Error Codes:
        100: Installation failed
    
    Example:
        result = install_system_package(password, 'mysql-server')
        if result.ok:
            print(f"{package} installed successfully")
    """
    cmd = ['apt', 'install']
    if auto_yes:
        cmd.append('-y')
    cmd.append(package)
    
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    
    if result is None:
        return Result(
            success=False,
            error_code=100,
            error_msg="Install command failed to execute"
        )
    
    if result.returncode == 0:
        return Result(
            success=True,
            data=f"Package '{package}' installed successfully"
        )
    else:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"Failed to install '{package}': {result.stderr.strip()}"
        )


def uninstall_system_package(sudo_password: str, package: str,
                             auto_yes: bool = True) -> Result:
    """
    Uninstalls a system package via APT.
    
    Args:
        sudo_password: User's sudo password
        package: Package name to uninstall
        auto_yes: Automatically answer 'yes' to prompts
    
    Returns:
        Result: Success if uninstalled, failure otherwise
    
    Error Codes:
        100: Uninstallation failed
    
    Example:
        result = uninstall_system_package(password, 'mysql-server')
        if result.ok:
            print(f"{package} uninstalled")
    """
    cmd = ['apt', 'remove']
    if auto_yes:
        cmd.append('-y')
    cmd.append(package)
    
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    
    if result is None:
        return Result(
            success=False,
            error_code=100,
            error_msg="Uninstall command failed to execute"
        )
    
    if result.returncode == 0:
        return Result(
            success=True,
            data=f"Package '{package}' uninstalled successfully"
        )
    else:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"Failed to uninstall '{package}': {result.stderr.strip()}"
        )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def upgrade_system_packages(sudo_password: str) -> Result:
    """
    Upgrades all installed packages (apt upgrade).
    
    Args:
        sudo_password: User's sudo password
    
    Returns:
        Result: Success if upgraded, failure otherwise
    """
    cmd = ['apt', 'upgrade', '-y']
    result = utils.system_executor(
        command=cmd,
        sudo_access=True,
        sudo_password=sudo_password
    )
    
    if result is None:
        return Result(
            success=False,
            error_code=100,
            error_msg="Upgrade command failed to execute"
        )
    
    if result.returncode == 0:
        return Result(
            success=True,
            data="System packages upgraded"
        )
    else:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"Upgrade failed: {result.stderr.strip()}"
        )


def get_package_info(package: str) -> Result:
    """
    Gets detailed information about a package.
    
    Args:
        package: Package name
    
    Returns:
        Result: Success with package info, or failure
    """
    cmd = ['apt', 'show', package]
    result = utils.system_executor(cmd)
    
    if result is None:
        return Result(
            success=False,
            error_code=100,
            error_msg="Info command failed to execute"
        )
    
    if result.returncode == 0:
        return Result(
            success=True,
            data=result.stdout.strip()
        )
    else:
        return Result(
            success=False,
            error_code=100,
            error_msg=f"Package '{package}' not found"
        )


# ============================================================================
# CONVENIENCE WRAPPER
# ============================================================================

def ensure_package_installed(sudo_password: str, package: str) -> Result:
    """
    Ensures a package is installed (installs if not already installed).
    
    Args:
        sudo_password: User's sudo password
        package: Package name
    
    Returns:
        Result: Success with installation status
    
    Example:
        result = ensure_package_installed(password, 'mysql-server')
        # Installs only if not already installed
    """
    # Check if already installed
    if is_package_installed(package):
        return Result(
            success=True,
            data=f"Package '{package}' already installed"
        )
    
    # Install package
    return install_system_package(sudo_password, package)