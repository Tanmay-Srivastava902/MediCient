'''Manages Password'''
import utils
from results import Result
import os

struct  = {}
# only depend on 
def init_password_storage(filepath):
    try:
        # checking parent folder
        parent_folder = os.path.dirname(filepath) 
        if not utils.is_dir_exists(parent_folder):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory Does Not Exists {parent_folder}"
            )
        # creating Password Storage 
        result = utils.write_binary_file(
            filepath=filepath,
            data=struct,
            overwrite=True,
            raw_data=False
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
            data=f"Password Storage Is  Created at {filepath}"
        )
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
    
def get_password(filepath,user):
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Password File Not Found"
            )
        
        # reading the file
        password_dict = utils.read_binary_file(filepath,raw_data=False)

        # cannot read
        if not password_dict:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Password File {password_dict.error_msg}"
            )
       
        # Extracting Password
        if password_dict.data is not None and user in password_dict.data:
            password = password_dict.data[user]
            # sending results
            return Result(
                success=True,
                data=password
            )
        else:
            return Result(
                success=False,
                error_code=500,
                error_msg=f"User '{user}' not found"
            )
    
    except Exception as e :
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )
            
def update_password(filepath,user,password):
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Password File Not Found"
            )
        
        result = utils.read_binary_file(filepath,raw_data=False)

         # cannot read
        if not result.ok :
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Password File {result.error_msg}"
            )
        
        # getting the password 
        password_dict = result.data

        if password_dict is not None :
            password_dict[user] = password
        else:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"No Password Data Found File May Be Corrupted {result.error_msg}"
            )
        
        # updating Password 
        result = utils.write_binary_file(
            filepath=filepath,
            data=password_dict,
            overwrite=True,
            raw_data=False
        )
        if not result:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Update Password Storage : {result.error_msg}"
            )
        
        # send result 
        return Result(
            success=True,
            data=f"Password Storage Updated"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
