from utils import executor
from results import Result
def is_venv_exists() -> bool :
   '''Checks the venv presence'''
   try:
      import venv
      return True
   except (ModuleNotFoundError,ImportError):
      return False
   
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
         sudo_password=sudo_password,
         need_output=True
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
def create_venv(dirpath,venv_name):
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
    try:
      venv_path = os.path.join(dirpath,venv_name)
      cmd = ['python3','-m','venv' , venv_path]
      result = executor.system_executor(
         command=cmd,
         sudo_access=False
      )
      if result is None:
         return Result(
            success=False,
            error_code=100,
            error_msg=f"❌ sudo_password required for sudo commands"
         )
      
      # venv created 
      if result.returncode == 0 :
         return Result(
            success=True,
            data=venv_path # path where venv is created 
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
#==============================
# VIRTUAL ENV MANAGEMENT
#==============================
def start_venv(venv_path:str,script_path:str,restart_delay:int):
   '''
   Starts The App Inside A Python Virtual Environment
   Args:
      venv_path: the path of venv folder (absolute path)
      script_path: the path of the file python file we want to run after restart[**/myproject/medicient.py**]
      restart_delay: the time after which the scheduled process wakes up
   Returns:
      None 
   Exits:
      code0: program exits creating a restart schedule for given time limit 
   '''
   import sys
   import os 
   import subprocess
   
   # getting paths 
   python_path = os.path.join(venv_path,'bin/python')

   # scheduling python 
   try:
      # & in last is to keep the process alive after start of the script 
      cmd  = f"sleep {restart_delay} && {python_path} {script_path}"
      subprocess.call(cmd,shell=True,start_new_session=True)
      sys.exit(0)
   except Exception as e:
      return Result(
         success=False,
         error_code=102,
         error_msg=f"Could Not Start Venv : {str(e).strip()}"
      )


# if __name__ == '__main__':
#    try: 
#       start_venv(
#          venv_path='/home/curiousme/myproject/medicient/medicient',
#          script_path='/home/curiousme/myproject/medicient/test_entry.py',
#          restart_delay=3
#       )
#       print('exited')
#    except Exception as e:
#       print(e)


