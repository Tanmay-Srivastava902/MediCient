from utils import filesystem
import errors
import os
from typing import Any
import datetime
#==============================
# install marker file
#==============================
def create_install_marker(dirpath:str,filename:str,metadata:dict)->None:
    '''Creates the marker file regardless existence of file'''
    try:
        # checking parent folder
        if not filesystem.is_dir_exists(dirpath):
           raise errors.FolderNotFoundError(f'Parent folder not found {dirpath}')
        # creating install marker 
        filepath = os.path.join(dirpath,filename)
        filesystem.write_raw_binary_file(
            filepath=filepath,
            data=metadata,
            overwrite=True
        )
        return None
    except Exception as e:
        raise errors.GeneralFileError(f'Could not create install marker {str(e).strip()}')
    
def load_install_marker_data(filepath:str)->dict[str,Any]:
    try:
        # checking parent folder
        if not filesystem.is_file_exists(filepath):
           raise errors.FolderNotFoundError(f'File not found {filepath}')
        metadata = filesystem.read_pickled_binary_file(filepath)
        return metadata
    except Exception as e:
        raise errors.GeneralFileError(f'Could not load metadata {str(e).strip()}')

#===============================
# log file 
#===============================
def create_logger(dirpath:str,filename:str):
    '''empty txt'''
    try:
        # checking parent folder
        if not filesystem.is_dir_exists(dirpath):
           raise errors.FolderNotFoundError(f'Parent folder not found {dirpath}')
        filepath = os.path.join(dirpath,filename)
        first_log_entry = f'[{datetime.datetime.now()}] Created Logger File\n'
        # creating logger 
        filesystem.write_txt_file(
            filepath=filepath,
            data=first_log_entry,
            overwrite=True
        )
        return None
    except Exception as e:
        raise errors.GeneralFileError(f'Could not create Logger {str(e).strip()}')

def get_logged_entries(
        filepath:str,
        number_of_entries:int=-1 ,
        reversed_reading:bool=True
        )->list[str]:

    '''all lines are loaded by default  Returns List of requested logged entries'''
    try:
        # checking parent folder
        if not filesystem.is_file_exists(filepath):
           raise errors.FolderNotFoundError(f'File not found {filepath}')
        logged_data = filesystem.read_txt_file(filepath)
        # getting all log entries [list]
        logged_entries = logged_data.splitlines()
        # getting no of entries requested entries 
        if number_of_entries != -1:
            requested_entries = logged_entries[:number_of_entries]
        else:
            requested_entries = logged_entries
        # reversing order of entries (latest first)
        if reversed_reading:
            requested_entries = logged_entries[::-1]
        return requested_entries
    except Exception as e:
        raise errors.GeneralFileError(f'Could not load metadata {str(e).strip()}')
            
def add_log_entry(filepath,new_entry:str)->None:
    '''appends to log '''
    try:
        # checking parent folder
        if not filesystem.is_file_exists(filepath):
           raise errors.FolderNotFoundError(f'File not found {filepath}')
        # auto adding new line on all logs if not already present 
        if not new_entry.endswith('\n'):
            new_entry += '\n'
        # auto adding time stamp 
        if not new_entry.startswith(str(datetime.datetime.now())):
            new_entry = f"[{str(datetime.datetime.now())}] {new_entry}"
        filesystem.append_txt_file(
            filepath=filepath,
            new_data=new_entry
        )
    except Exception as e:
        raise errors.GeneralFileError(f'Could not add entry {str(e).strip()}')
   

