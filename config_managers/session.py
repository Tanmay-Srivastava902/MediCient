'''Manages Session'''
struct = {
    "USER":{
    "USER":"",
    "HOST":"localhost",
    "session":"",
    "DB":"",
    "LOGGED_IN_AT":"",
    "STATUS":""
    }
}
# only depend on 
# def init_session_storage(filepath , ):
#     '''empty dict'''
#     pass
# def get_session(filepath , user ,session):
#     '''gets a session dict for users'''
#     pass
# def update_session(filepath , user_session):
#     pass

'''Manages session'''
import utils
from results import Result
import os

struct  = {}
# only depend on 
def init_session_storage(filepath):
    try:
        # checking parent folder
        parent_folder = os.path.dirname(filepath) 
        if not utils.is_dir_exists(parent_folder):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory Does Not Exists {parent_folder}"
            )
        # creating session Storage 
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
            data=f"Session Storage Is  Created at {filepath}"
        )
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
    
def get_session(filepath,user):
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="session File Not Found"
            )
        
        # reading the file
        result = utils.read_binary_file(filepath,raw_data=False)

        # cannot read
        if not result:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read session File {result.error_msg}"
            )

        session_dict =result.data
        # Extracting session
        if session_dict is not None and user in session_dict.keys():
            session_dict = session_dict[user]
            # sending results
            return Result(
                success=True,
                data=session_dict
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
            
def update_session(filepath,user,session:dict):
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="session File Not Found"
            )
        
        result = utils.read_binary_file(filepath,raw_data=False)

         # cannot read
        if not result.ok :
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read session File {result.error_msg}"
            )
        
        # getting the session 
        session_dict = result.data

        if session_dict is not None :
            session_dict[user] = session
        else:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"No session Data Found File May Be Corrupted {result.error_msg}"
            )
        
        # updating session 
        result = utils.write_binary_file(
            filepath=filepath,
            data=session_dict,
            overwrite=True,
            raw_data=False
        )
        if not result:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Update session Storage : {result.error_msg}"
            )
        
        # send result 
        return Result(
            success=True,
            data=f"session Storage Updated"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
