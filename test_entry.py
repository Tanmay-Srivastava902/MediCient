from utils import system_executor , python_executor , mysql_executor
from results import Result

# print(system_executor(['true']))
# res = system_executor(['true'],sudo_access=True)
# res = system_executor(['systemctl','status','mysql'],sudo_access=False,sudo_password="1201")
# res = system_executor(['systemctl','start','mysql'],sudo_access=False,sudo_password="1201")
# res = system_executor(['systemctl','start','mysql'],sudo_access=True,sudo_password="1201")
# res = system_executor(['systemctl','start','mysql'],sudo_access=True)
# res = python_executor(['30 > 20']) # script mode -c
# res = python_executor(['30 > 20'],run_module=True,interactive_mode=True) # both mode -m and -i
# res = python_executor(['pip','install','mysql-connector-python'],run_module=True,interactive_mode=True) # both mode -m and -i
# res = python_executor(['pip','install','mysql-connector-python'],run_module=True) # testing -m
# res = python_executor(['-m','utils'],interactive_mode=True,need_output=False) # testing -m
# if res:
#     print(res.returncode,res.stderr)
# else:
#     print('both args provide select one')
#     print(res.error_msg)
