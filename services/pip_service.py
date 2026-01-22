'''FOR PYTHON SPECIFIC TASKS'''
import utils
import errors
#==============================
# pip management
#==============================
def is_pip_exists() -> bool :
   '''Checks the pip presence'''
   try:
      cmd = ["python", "-m", "pip", "--version"]
      result = utils.system_executor(
         command=cmd,
         sudo_access=False
      )
      if result.returncode != 0:
         raise errors.ExecutionError(f"could not execute : {result.stderr}")
      return True
   except FileNotFoundError :
      return False
   
def install_pip(sudo_password)->None:
   '''Installs the pip python package manager
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   cmd = ['apt','install','-y','python3-pip']
   result = utils.system_executor(
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
   result = utils.system_executor(
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
   result = utils.system_executor(
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
   result = utils.system_executor(
      command=cmd,
      sudo_access=False
   )
   if result.returncode != 0 :
      raise errors.PipError(f"Could Not install package : {result.stderr}")
   return None

def uninstall_python_package(package:str)->None:
   '''Uninstalls python package 
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   cmd  = ['pip','uninstall',package]
   result = utils.system_executor(
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
   


         



