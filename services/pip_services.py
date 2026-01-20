'''FOR PYTHON SPECIFIC TASKS'''
import utils
from results import Result
#==============================
# pip management
#==============================
def is_pip_exists() -> bool :
   '''Checks the pip presence'''
   try:
      import pip
      return True
   except (ModuleNotFoundError,ImportError):
      return False
   
def install_pip(sudo_password)->Result:
   '''Installs the pip python package manager
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   try:
      cmd = ['apt','install','python3-pip']
      result = utils.system_executor(
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


#========================
# Package Transmission Controller
#========================
def export_python_packages()-> Result:
   '''
   Exports the currently installed python packages to given location

   :returns Result: [**packages_string in result.data**] if self.ok  exported else not self.ok and error_code,error_msg
   '''
   try:
      cmd  = ['pip','freeze']
      result = utils.system_executor(
         command=cmd,
         need_output=True,
         sudo_access=False
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
            data=result.stdout  # result to ve saved 
         )
      else:
         return Result(
            success=False,
            error_code=100,
            error_msg=result.stderr # result is given back 
         )
   except Exception as e :
      return Result(
         success=False,
         error_code=101,
         error_msg=f"Unexpected Error:{str(e).strip()}"
      )
      
def import_python_packages(filepath):
   '''Imports(installs) the python packages from  given file
   Args:
      filepath: location of import file with full name and extension
   Returns:
      Result: self.ok if exported else not self.ok and error_code,error_msg
   '''
   try:
      cmd  = ['pip','install','-r',filepath]
      result = utils.system_executor(
         command=cmd,
         need_output=True,
         sudo_access=False
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
            data=f"Packages Imported From  {filepath}"
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
      

#========================
# python package management
#========================
# only require system execute cmd  (subprocess)
def install_python_package(package)-> Result:
   '''Installs python package 
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   try:
      cmd = ['pip','install',package]
      result = utils.system_executor(
         command=cmd,
         sudo_access=False
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
            data=f"{package} is installed"
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


def uninstall_python_package(package):
   '''Uninstalls python package 
   Args:
      None
   Returns:
      Result: self.ok if installed Else not self.ok 
   '''
   try:
      cmd = ['pip','uninstall','-y',package]
      result = utils.system_executor(
         command=cmd,
         sudo_access=False
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
            data=f"{package} is uninstalled"
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

#=======================
# convenience wrapper
#=======================
def ensure_python_package(package,sudo_password):
   '''Ensures the package is installed and ready to use
   Args:
      package: name of python package to install
   Returns:
      Result: self.ok if succeed else not self.ok if undesired error
   '''
   try:
      if not is_pip_exists():
         # installing pip
         result = install_pip(sudo_password)
         if not  result.ok :
            return result # could not perform operation
   
      # pip installed installing package 
      result = install_python_package(package)
      if not result.ok:
         return result # could not install
   
      # package is installed
      return Result(
         success=True,
         data=f"{package} is installed"
      )
   except Exception as e :
      return Result(
         success=False,
         error_code=100,
         error_msg=f"Unknown Error: {str(e).strip()}"
      )
   


         



