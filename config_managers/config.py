'''Manages json'configs.json'''

DEFAULT_CONFIGS_DICT = {
    "ERROR_CODES":{
        "EXECUTION_ERROR":100,
        "PIP_ERROR":101,
        "VENV_ERROR":102,
        "SERVICE_ERROR":300,
        "SERVICE_RUNNING":301,
        "SERVICE_STOPPED":302,
        "SERVICE_NOT_INSTALLED":303,
        "UNKNOWN_ERROR":200,
        "FOLDER_ALREADY_EXISTS_ERROR":400,
        "FOLDER_NOT_FOUND_ERROR":401,
        "FILE_ALREADY_EXISTS_ERROR":402,
        "FILE_NOT_FOUND_ERROR":404,
        "FOLDER_NOT_EMPTY":409,
        "GENERAL_FILE_ERROR":410,
        "KEY_NOT_FOUND_ERROR":500,

    },
    "APP_CONFIG":{
        "app_name":"MediCient",
        "app_tagline":"Medicine X Patient",
        "app_tagline2":"Relates Medicine with Patients  With Care",
        "app_desc":"Healthcare Management System for Patients & Doctors"
    },
    "AUTHOR_CONFIG":{
        "author_name":"Tanmay Srivastava",
        "author_email":"tscreateandcare+medicient@gmail.com",
        "author_contact":"+91000000000"
    },
    "DB_CONFIG":{
        "db_host":"localhost",
        "db_name":"medicient",
        "db_admin":"medicient_admin"
    },
    "PATH_CONFIG":{
        "app_dir_path":"~/.config/.medicient",
        "config_dir_path":"'~/.config",
        "install_marker_file_path":"~/.config/.medicient/install_marker.medisecure",
        "encryption_key_file_path":"~/.config/.medicient/app_encryption_key.key",
        "config_file_path":"configs/config.medisecure",
        "session_file_path":"configs/session.medisecure",
        "log_file_path":"configs/app_logger.log",
        "packages_file_path":"configs/packages.medisecure"
    }
}
import os 
import utils 
from results import Result

# only depend on 
def init_config_storage(filepath):
    try:
        # checking parent folder
        parent_folder = os.path.dirname(filepath) 
        if not utils.is_dir_exists(parent_folder):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory Does Not Exists {parent_folder}"
            )
        # creating schema  
        result = utils.write_json_file(
            filepath=filepath,
            json_dict=DEFAULT_CONFIGS_DICT,
            overwrite=True
        )
        
        if not result:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Write File : {result.error_msg}"
            )
        # send result 
        return Result(
            success=True,
            data=f"Json file  Is Created at {filepath}"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
    
def get_config(filepath , all:bool=False,config_name:str='')->Result:
    '''loading of config is supported only upto one level in dict eg- {'level_1':{'level_2':'value'}} -> config = level_1 is valid '''
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Config File Not Found"
            )
        
        # reading the file
        result = utils.read_json_file(filepath)

        # cannot read
        if not result:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Config File {result.error_msg}"
            )

        json_dict = result.data

        # whole dict is requested
        if all:
            return Result(
                success=True,
                data=json_dict,
            )

        # if not config name is given
        if not all and not config_name:
            return Result(
                success=False,
                error_code=410,
                error_msg=f'Cannot Found config_name for all=False '
            )
        
        # Extracting configs
        if json_dict is not None and config_name in json_dict.keys():
            config_dict = json_dict[config_name]
            # sending results
            return Result(
                success=True,
                data=config_dict
            )
        else:
            return Result(
                success=False,
                error_code=500,
                error_msg=f"config_name '{config_name}' Does Not Exists"
            )
    
    except Exception as e :
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )
            


def update_config(filepath,config_name:str,config_dict:dict):
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="config File Not Found"
            )
        
        result = utils.read_json_file(filepath)

         # cannot read
        if not result.ok :
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Json File {result.error_msg}"
            )
        
        # getting the config 
        json_dict = result.data

        if json_dict is not None:
            json_dict[config_name] = config_dict
        else:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"No config Data Found File May Be Corrupted {result.error_msg}"
            )
        
        # updating config 
        result = utils.write_json_file(
            filepath=filepath,
            json_dict=json_dict,
            overwrite=True
        )
        if not result:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Update config Storage : {result.error_msg}"
            )
        
        # send result 
        return Result(
            success=True,
            data=f"config Storage Updated"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )

