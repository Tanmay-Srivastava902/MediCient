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
from utils import filesystem
import errors
import os
from typing import Any
# only depend on 
def create_config(dirpath:str,filename:str)->None:
    '''Creates the marker file regardless existence of file'''
    try:
        # checking parent folder
        if not filesystem.is_dir_exists(dirpath):
           raise errors.FolderNotFoundError(f'Parent folder not found {dirpath}')
        # creating json
        filepath = os.path.join(dirpath,filename)
        filesystem.write_json_file(
            filepath=filepath,
            json_dict=DEFAULT_CONFIGS_DICT,
            overwrite=True
        )
        return None
    except Exception as e:
        raise errors.GeneralFileError(f'Could not create Json {str(e).strip()}')
    
def get_all_config(filepath:str)->dict[str,Any]:
    try:
        # checking parent folder
        if not filesystem.is_file_exists(filepath):
           raise errors.FolderNotFoundError(f'File not found {filepath}')
        all_configs = filesystem.read_json_file(filepath)
        return all_configs
    except Exception as e:
        raise errors.GeneralFileError(f'Could not load metadata {str(e).strip()}')

def get_specific_config(filepath:str,config_name:str)->dict[str,Any]:
    '''loading of config is supported only upto one level in dict eg- {'level_1':{'level_2':'value'}} -> config = level_1 is valid '''
    try:
        # checking parent folder
        if not filesystem.is_file_exists(filepath):
           raise errors.FolderNotFoundError(f'File not found {filepath}')
        all_configs = filesystem.read_json_file(filepath)
        if not config_name in all_configs.keys():
            raise errors.InvalidArgumentError(f'config name does not match to any config') 
        return all_configs[config_name] # specific
    except Exception as e:
        raise errors.GeneralFileError(f'Could not config {str(e).strip()}')
