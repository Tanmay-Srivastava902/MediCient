
# depends on file manager only just create file read file update file
import utils
import os 
from results import Result
def init_install_marker(filepath:str,metadata:dict):
    '''Creates the marker file regardless existence of file'''
    try:
        # checking parent folder
        parent_folder = os.path.dirname(filepath) 
        if not utils.is_dir_exists(parent_folder):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory Does Not Exists {parent_folder}"
            )
        
        # creating install marker 
        result = utils.write_binary_file(
            filepath=filepath,
            data=metadata,
            overwrite=True,
            raw_data=False
        )
        if result.ok :
            return Result(
                success=True,
                data=f"Install Marker Created at {filepath}"
            )
        else:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Write File : {result.error_msg}"
            )
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e)}"
        )

def load_install_marker_data(filepath):
    ''''''
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Install Marker Not Found Corrupted installation"
            )
        
        # reading the file
        result = utils.read_binary_file(
            filepath,
            raw_data=False
        )
        # file not found
        if not result :
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Install Marker : {result.error_msg}"
            )
        # return marker data 
        return Result(
           success=True,
           data=result.data
        )
    except Exception as e :
         return Result(
                success= False,
                error_code=410,
                error_msg=f"Unexpected Error {str(e)}"
            )

