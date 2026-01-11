'''MANAGES SYSTEM SERVICES'''
# independent  (no sudo password needed)
def get_service_status(service):
    pass

# requires password (uses cmd executor)
def start_service(service,sudo_password):
    pass
def stop_service(service,sudo_password):
    pass
def restart_service(service,sudo_password):
    pass

# dependent on system root (package_installer)
def install_service(service,sudo_password):
    pass
def uninstall_services(service,sudo_password):
    pass


