"""
OPERATES ON VENV SERVICES RELATED TO PYTHON VIRTUAL ENVIRONMENT
"""
from utils import executor
from results import Result
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
def install_venv_dependencies(venv_path,filepath):
   '''
   Install All Dependencies To The Given Python Venv Via The Given Requirement file 
   :params venv_path: path to the venv folder with its name 
   :type venv_path: str
   :params filepath: path to the requirements file where the requirements are kept
   '''
   pass

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
   # import subprocess
   
   # getting paths 
   python_path = os.path.join(venv_path,'bin/python')

   # scheduling python 
   try:
      # & in last is to keep the process alive after start of the script
      import time 
      for i in range(restart_delay+1):
         print(f"restarting in {restart_delay-i} seconds")
         time.sleep(1)

      os.execv(python_path, [python_path, script_path])
   except Exception as e:
      return Result(
         success=False,
         error_code=102,
         error_msg=f"Could Not Start Venv : {str(e).strip()}"
      )


# if __name__ == '__main__':
#    try: 
#       print('an i in venv expected false? ',is_using_venv())
#       start_venv(
#          venv_path='/home/curiousme/myproject/medicient/medicient',
#          script_path='/home/curiousme/myproject/medicient/test_venv_entry.py',
#          restart_delay=3
#       )
#       print('am i in venv expected false? ' , is_using_venv())

#       print('exited')
#    except Exception as e:
#       print(e)


