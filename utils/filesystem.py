"""UNIVERSAL FILE HANDLER WITH BASIC CRUD FOLDER OPERATIONS """
import os 
import json
import pickle
import errors
from typing import Any
#========================
# UNIVERSAL FILE OPERATIONS
#========================
def is_file_exists(filepath)->bool:
    return os.path.isfile(filepath)

def delete_file(filepath)->None:
    if not is_file_exists(filepath):
        raise errors.FileNotFoundError(f'File does not exists {filepath}')
    os.remove(filepath)
    return None
#========================
# TEXT FILE OPERATIONS
#========================
def write_txt_file(filepath,data,overwrite=False)->None:
    if is_file_exists(filepath) and not overwrite:
               raise errors.InvalidArgumentError(f'File Already Exists use overwrite= True')
    with open(filepath,'w') as f :
        f.write(data)
    return None
def append_txt_file(filepath,new_data)->None:
    
    if not  is_file_exists(filepath):
       raise errors.FileNotFoundError(f'File not found {filepath}')
    with open(filepath,'a') as f :
        f.write(new_data)
    return None
def read_txt_file(filepath)->str:
    if not is_file_exists(filepath):
        raise errors.InvalidArgumentError(f'File Already Exists use overwrite= True')
    with open(filepath) as f :
        data = f.read()
    return data
# NOTE update is prohibited for json and binary due to object content conflicts possibilities
#========================
# BINARY FILE OPERATIONS
#========================
# raw binary 
def write_raw_binary_file(filepath,data:Any,overwrite=False)-> None:
    '''Create a binary file'''
    if is_file_exists(filepath) and not overwrite:
        raise errors.InvalidArgumentError(f'File Already Exists use overwrite= True')
    with open(filepath,'wb') as f :
       f.write(data) # if raw files do not serialize eg- keys 
    return None

def read_raw_binary_file(filepath:str)->bytes:
    if not  is_file_exists(filepath):
        raise errors.FileNotFoundError(f"file not found {filepath}")
    with open(filepath,'rb') as f :
        data =  f.read() # if raw files do not deserialize  eg- keys 
    return data

# pickled binary
def write_pickled_binary_file(filepath,data:Any,overwrite=False)-> None:
    '''Create a binary file'''
    if is_file_exists(filepath) and not overwrite:
        raise errors.InvalidArgumentError(f'File Already Exists use overwrite= True')
    with open(filepath,'wb') as f :
        pickle.dump(data,f) # serialize if python object
    return None

def read_pickled_binary_file(filepath:str)->Any:
    if not  is_file_exists(filepath):
        raise errors.FileNotFoundError(f"file not found {filepath}")
    with open(filepath,'rb') as f :
        data  = pickle.load(f) # serialize if python objects
    return data
#=======================
# JSON FILE OPERATIONS
#========================
def write_json_file(filepath,json_dict:dict,overwrite=False)-> None:
    '''Create a Json file'''
    if is_file_exists(filepath) and not overwrite:
        raise errors.InvalidArgumentError(f'File Already Exists use overwrite= True')
    with open(filepath,'w') as f :
        json.dump(json_dict,f)
    return None

def read_json_file(filepath)->dict[str,Any]:
    # if file not exists
    if not is_file_exists(filepath):
        raise errors.FileNotFoundError(f'File does not exists {filepath}')
    with open(filepath) as f :
        data = json.load(f)
    return data

# =============================
# FOLDER OPERATIONS
# =============================

def is_dir_exists(dirpath)->bool:
    return os.path.isdir(dirpath)

def create_dir(parent_dirpath:str,dirname:str,mode:int=0o700)->None: # all can read but only owner can write
    '''Create A dir 
    
    :params parent_dirpath: path of parent dir 
    :params mode: chmod for setting permissions for folder default 700 user only
    :raises FolderNotFoundError: if parent not exits 
    '''
    # checking parent dir existence
    if  not is_dir_exists(parent_dirpath):
        raise errors.FolderNotFoundError(f'Parent folder does not exists {parent_dirpath}')
    dirpath = os.path.join(parent_dirpath,dirname)
    return os.makedirs(dirpath,mode,exist_ok=True)

def delete_dir(dirpath,forced=False,disable_prompt=False)->None:
    '''
    Docstring for delete_dir
    
    :param dirpath: name of folder
    :param forced: accidental protection for non empty dirs 
    :param disable_prompt: wether going to delete a non empty dir intentionally or not
    :raises FolderNotFoundError: if parent not exits 
    :raises InvalidArgumentError: if folder not empty and forced = False
    '''
    import shutil
    if not is_dir_exists(dirpath):
        raise errors.FolderNotFoundError(f'Folder does not exits : {dirpath}')
    # if folder is not empty 
    if len(os.listdir(dirpath)) > 0  and not forced:
        raise errors.InvalidArgumentError(f"Folder {dirpath} Is Not Empty Please Retry With  Forced = True")
    # if prompt is not disabled
    if not disable_prompt:
        input(f"⚠️ Warning ! You Are Going TO Delete Directory {dirpath}\nPress Enter To Continue or press Ctrl + C to Abort And Exit")
    # remove dir 
    return shutil.rmtree(dirpath)
       

