"""
OPERATES ON VENV SERVICES RELATED TO PYTHON VIRTUAL ENVIRONMENT
"""
from utils import executors
import errors
import os 
import time 
import sys
#========================================================================
# PIP SERVICE
#========================================================================
def is_pip_exists() -> bool :
   '''Checks the pip presence'''
   try:
      cmd = ["python", "-m", "pip", "--version"]
      result = executors.system_executor(
         command=cmd,
         sudo_access=False
      )
      if result.returncode != 0:
         raise errors.ExecutionError(f"could not execute : {result.stderr}")
      return True
   except FileNotFoundError :
      return False
   
def install_pip(sudo_password)->None:
   '''
   Installs the pip python package manager

   :param sudo_password: password for sudo user
   :returns None: if installed
   :raises InstallError: if could not install
   '''
   cmd = ['apt','install','-y','python3-pip']
   result = executors.system_executor(
      command=cmd,
      sudo_access=True,
      sudo_password=sudo_password
      
   )
   if result.returncode == 0 :
      return None
   else:
      raise errors.InstallError(f"could not install : {result.stderr}")
   
#================================
# Package Transmission Controller
#================================
def export_python_packages()-> str:
   '''
   Exports the currently installed python packages to given location

   :returns exported_packages_string: the output of pip freeze
   :raises PipError: if could not export
   
   '''
   cmd  = ['pip','freeze']
   result = executors.system_executor(
      command=cmd,
      sudo_access=False
   )
   if result.returncode != 0 :
      raise errors.PipError(f"could not export : {result.stderr}")
   return result.stdout # packages string
      
def import_python_packages(filepath)->None:
   '''
   Imports(installs) the python packages from  given file

   :param filepath: location of import file with full name and extension
   :returns None : if imported
   :raises PipError: if could not export
   
   '''
   cmd  = ['pip','install','-r',filepath]
   result = executors.system_executor(
      command=cmd,
      sudo_access=False
   )
   if result.returncode != 0 :
      raise errors.PipError(f"Could Not import packages : {result.stderr}")
   return None
#=============================
# python package management
#==============================
def install_python_package(package:str)-> None:
   '''
   Installs python package 
   :param package: name of package to install
   :returns none: if installed 
   :raises PipError: if could not export
   '''
   cmd  = ['pip','install',package]
   result = executors.system_executor(
      command=cmd,
      sudo_access=False
   )
   if result.returncode != 0 :
      raise errors.PipError(f"Could Not install package : {result.stderr}")
   return None

def uninstall_python_package(package:str)->None:
   '''Uninstalls python package 
    :param: package name 
    :returns None: if installed
   '''
   cmd  = ['pip','uninstall',package]
   result = executors.system_executor(
      command=cmd,
      sudo_access=False
   )
   if result.returncode != 0 :
      raise errors.PipError(f"Could Not install package : {result.stderr}")
   return None
   
#=======================
# convenience wrapper
#=======================
def ensure_python_package(package,sudo_password):
   '''Ensures the package is installed and ready to use
  
   :params package: name of python package to install
   :returns None if package is present or installed   
   '''
   if not is_pip_exists():
      install_pip(sudo_password)
   # pip installed installing package 
   install_python_package(package)
   return None
   
#===============================================================================
# VENV SERVICE
#===============================================================================
def is_using_venv()-> bool:
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )

def install_venv(sudo_password:str)->None:
   '''
   Installs the venv python virtual environment manager

   :param sudo_password: password for sudo user
   :returns None: if installed
   :raises InstallError: if could not install
   '''
   cmd = ['apt','install','-y','python3-venv']
   result = executors.system_executor(
      command=cmd,
      sudo_access=True,
      sudo_password=sudo_password
   )
   if result.returncode != 0 :
      raise errors.InstallError(f'could not install venv package : {result.stderr}')
   return None

def create_venv(dirpath:str,venv_name:str)-> str:
   '''
   Create the virtual environment
    
    :param dirpath: the path of folder in which the venv folder is created 
    :param venv_name: the name of the venv we want to create
    :returns str: [**venv_path**] if created
    Examples: 
        :create_venv('/home/hello','my_venv')
        :result  -> /home/hello/my_venv <- the venv is created here 
   '''
   venv_path = os.path.join(dirpath,venv_name)
   cmd = ['python3','-m','venv' , venv_path]
   result = executors.system_executor(
      command=cmd,
      sudo_access=False
   )
   # venv created 
   if result.returncode != 0 :
      raise errors.VenvError(f"could not create venv: {result.stderr}")
   return venv_path

def start_venv(venv_path:str,script_path:str,restart_delay:int)->None:
   '''
   Starts The App Inside A Python Virtual Environment
 
   :params venv_path: the path of venv folder (absolute path)
   :params script_path: the path of the file python file we want to run after restart[**/myproject/medicient.py**]
   :params restart_delay: the time after which the scheduled process wakes up
   :returns: None 
   :raises code0: program exits creating a restart schedule for given time limit 
   '''
   # getting python paths 
   python_path = os.path.join(venv_path,'bin/python')
   # scheduling restart
   for i in range(restart_delay+1):
      print(f"restarting in {restart_delay-i} seconds")
      time.sleep(1)
   # executing after schedule
   os.execv(python_path, [python_path, script_path])
   return None
