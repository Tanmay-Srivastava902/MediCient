'''HANDLES EXTERNAL OS SYSTEM RELATED TASK'''

# requires nothing (subprocess)
def execute_cmd(cmd,sudo_access,sudo_password):
    pass

# apt specific requires (execute_cmd)
def update_packages(sudo_password):
    pass
def upgrade_packages(sudo_password):
    pass
def auto_remove_packages(sudo_password):
    pass

# package specific requires (upgrade and update and execute cmd )
def package_installer(package,sudo_password):
    pass
def service_controller(operation,service):
    '''start stop restart status'''
    pass

# uses file operations (password specific)
def save_sudo_password(password):
    # knows user
    pass




