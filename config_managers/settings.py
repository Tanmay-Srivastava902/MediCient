'''Manages json'Settings.json'''

DEFAULT_SETTINGS_STRUCTURE = '''{
    "ERROR_CODES":{
        "EXECUTION_ERROR":100,
        "FOLDER_ALREADY_EXISTS_ERROR":400,
        "FOLDER_NOT_FOUND_ERROR":401,
        "FILE_ALREADY_EXISTS_ERROR":402,
        "FILE_NOT_FOUND_ERROR":404,
        "FOLDER_NOT_EMPTY":409,
        "GENERAL_FILE_ERROR":410

    }
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
        "db_admin":"medicient_admin",
    },
    "PATH_CONFIG":{
        "app_dir_path":"~/.config/.medicient",
        "config_dir_path":"'~/.config"
        "install_marker_file_path":"~/.config/.medicient/install_marker.medisecure",
        "encryption_key_file_path":"~/.config/.medicient/app_encryption_key.key",
        "password_file_path":"configs/password.medisecure",
        "session_file_path":"configs/session.medisecure",
        "log_file_path":"configs/app_logger.log",
        "packages_file_path":"configs/packages.medisecure",

    },
}

'''
import os 
import utils 
from results import Result

# only depend on 
def init_setting_storage(filepath):
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
        result = utils.write_txt_file(
            filepath=filepath,
            data=DEFAULT_SETTINGS_STRUCTURE,
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
    
def get_setting(filepath , all:bool=False,setting_name:str=''):
 pass


def update_setting(all,setting):
    pass
