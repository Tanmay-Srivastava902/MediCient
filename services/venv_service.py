"""
OPERATES ON VENV SERVICES RELATED TO PYTHON VIRTUAL ENVIRONMENT
"""
from utils import executor
from results import Result
import errors
def is_using_venv()-> bool:
    import sys
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def install_venv(sudo_password):
   '''Installs the venv python virtual environment manager
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   try:
      cmd = ['apt','install','python3-venv']
      result = executor.system_executor(
         command=cmd,
         sudo_access=True,
         sudo_password=sudo_password
      )
      if result is None:
         return Result(
            success=False,
            error_code=100,
            error_msg=f"❌ sudo_password required for sudo commands"
         )
      if result.returncode == 0 :
         return Result(
            success=True,
            data=f"Pip is installed"
         )
      else:
         return Result(
            success=False,
            error_code=100,
            error_msg=result.stderr
         )
   except Exception as e :
      return Result(
         success=False,
         error_code=101,
         error_msg=f"Unexpected Error:{str(e).strip()}"
      )

# venv related
def create_venv(dirpath:str,venv_name:str)-> str:
   '''Create the virtual environment
    Args:
        dirpath: the path of folder in which the venv folder is created 
        venv_name: the name of the venv we want to create
    Returns:
        Result: [**venv_path**] if created (self.ok) else [**result.stderr**] or [**str(e)**] if exception occurred
    Example:
        create_venv('/home/hello','my_venv')
        result  -> /home/hello/my_venv <- the venv is created here 
   '''
   import os 
   venv_path = os.path.join(dirpath,venv_name)
   cmd = ['python3','-m','venv' , venv_path]
   result = executor.system_executor(
      command=cmd,
      sudo_access=False
   )
   # venv created 
   if result.returncode != 0 :
      raise errors.VenvError(f"could not create venv: {result.stderr}")
   return venv_path

def start_venv(venv_path:str,script_path:str,restart_delay:int):
   '''
   Starts The App Inside A Python Virtual Environment
 
   :params venv_path: the path of venv folder (absolute path)
   :params script_path: the path of the file python file we want to run after restart[**/myproject/medicient.py**]
   :params restart_delay: the time after which the scheduled process wakes up
   :returns: None 
   :raises code0: program exits creating a restart schedule for given time limit 
   '''
   import os 
   import time 
   # getting python paths 
   python_path = os.path.join(venv_path,'bin/python')
   # scheduling restart
   for i in range(restart_delay+1):
      print(f"restarting in {restart_delay-i} seconds")
      time.sleep(1)
   # executing after schedule
   os.execv(python_path, [python_path, script_path])
   return None
