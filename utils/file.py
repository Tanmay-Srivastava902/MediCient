"""UNIVERSAL FILE HANDLER WITH BASIC CRUD FOLDER OPERATIONS """
import os 
import json
import pickle
from results import Result
# universal file handler

#========================
# UNIVERSAL FILE OPERATIONS
#========================
def is_file_exists(filepath)->bool:
    return os.path.isfile(filepath)

def delete_file(filepath)->Result:
    if os.path.isfile(filepath):
        os.remove(filepath)
        return Result(
                    success=True,
                    data=f"Deleted File {filepath}"
                     )
    else : 
       return Result(
                success=False,
                error_msg=f"{filepath} file does not exists",
                error_code=404
            )
    
# specific to file types

#========================
# TEXT FILE OPERATIONS
#========================
def write_txt_file(filepath,data,overwrite=False)->Result:
    if os.path.isfile(filepath) and not overwrite:
        return Result(
            success=False,
            error_msg=f"file already exists cannot overwrite try again with  overwrite = True",
            error_code=402
            )
    
    with open(filepath,'w') as f :
        f.write(data)
    return Result(
                success=True,
                data=f"written text file {filepath}"
                )
        
def append_txt_file(filepath,new_data):
    
    if not  os.path.exists(filepath):
        return Result(
            success=False,
            error_msg=f"{filepath} file does not exists",
            error_code=404
            )

    with open(filepath,'a') as f :
        f.write(new_data)
    return Result(
                success=True,
                data=f"Appended File {filepath}"
                )
    
def read_txt_file(filepath)->Result:
    '''set readlines = True to get output as list '''
    if os.path.exists(filepath):
        with open(filepath) as f :
            data = f.read()
        return Result(
                    success=True,
                    data=data
                    )
    else:
        return Result(
            success=False,
            error_msg=f"{filepath} file does not exists",
            error_code=404
            )
# NOTE update is prohibited for json and binary due to object content conflicts possibilities
#========================
# BINARY FILE OPERATIONS
#========================
def write_binary_file(filepath,data,overwrite=False,raw_data=False):
    '''Create a binary file'''
    if os.path.isfile(filepath) and not overwrite:
        return Result(
            success=False,
            error_msg=f"file already exists cannot overwrite try again with  overwrite = True",
            error_code=402
            )
   
    with open(filepath,'wb') as f :

        if not raw_data:
            pickle.dump(data,f) # serialize if python objects
        else:
            f.write(data) # if raw files do not serialize eg- keys 

    return Result(
                    success=True,
                    data=f"Written binary file {filepath}"
                    )


def read_binary_file(filepath,raw_data:bool=False)-> Result:
    if not  os.path.exists(filepath):
          return Result(
            success=False,
            error_msg=f"{filepath} file does not exists",
            error_code=404
            )
    
    with open(filepath,'rb') as f :
            if not raw_data:
                data  = pickle.load(f) # serialize if python objects
            else:
               data =  f.read() # if raw files do not deserialize  eg- keys 
    
    return Result(
                    success=True,
                    data=data
                    )

#========================
# JSON FILE OPERATIONS
#========================
def write_json_file(filepath,json_dict:dict,overwrite=False)-> Result:

    '''Create a Json file'''
    if os.path.isfile(filepath) and not overwrite:
        return Result(
            success=False,
            error_msg=f"file already exists cannot overwrite try again with  overwrite = True",
            error_code=402
            )
    
    with open(filepath,'w') as f :
        json.dump(json_dict,f)
    return Result(
                success=True,
                data=f"written json file {filepath}"
                )


def read_json_file(filepath):
    # if file not exists
    if not os.path.exists(filepath):
        return Result(
            success=False,
            error_msg=f"{filepath} file does not exists",
            error_code=404
            )
    
    with open(filepath) as f :
        data = json.load(f)
        return Result(
                        success=True,
                        data=data
                      )




# =============================
# BASIC FOLDER OPERATIONS
# =============================

def is_dir_exists(dirpath):
    return os.path.isdir(dirpath)

def create_dir(dirpath:str,mode:int=0o700): # all can read but only owner can write
    '''Create A dir 
    Args:
        dirpath: full path of dir with name of dir [**eg- parent_dirpath/dirname]
        mode: chmod for setting permissions for folder default 700 user only
    Returns:
        Result: result object 
        401: parent folder not exists 

    '''
   
    # checking parent dir existence
    parent_dirpath = dirpath.rsplit('/',1)[0]
    if  not os.path.isdir(parent_dirpath):
        return Result(
                success=False,
                error_msg=f"Parent Folder {parent_dirpath} Does Not  Exists",
                error_code=401
        )
    
    # create dir 
    os.makedirs(dirpath,mode,exist_ok=True)
    return Result(
            success=True,
            data=f"Created dir {dirpath}"
    )

def delete_dir(dirpath,forced=False,disable_prompt=False):
    import shutil

    # parent dir existence check
    if not os.path.isdir(dirpath):
         return Result(
                success=False,
                error_msg=f"Folder {dirpath} Does Not Exists",
                error_code=401
        )
    # if folder is not empty 
    if len(os.listdir(dirpath)) > 0  and not forced:
        
            return Result(
                        success=False,
                        error_msg=f"Folder {dirpath} Is Not Empty Please Retry With  Forced = True",
                        error_code=409
                        )
    # if prompt is not disabled
    if not disable_prompt:
        input(f"⚠️ Warning ! You Are Going TO Delete Directory {dirpath}\nPress Enter To Continue or press Ctrl + C to Abort And Exit")
    
    # remove dir 
    shutil.rmtree(dirpath)
    return Result(
            success=True,
            data=f"Deleted Dir {dirpath}"
    )
       

