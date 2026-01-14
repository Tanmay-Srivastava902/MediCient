'''Manages logging'''
# only depend on 
import datetime
import utils
import os 
from results import Result

def init_logger_storage(filepath):
    '''empty txt'''
    try:
        # checking parent folder
        parent_folder = os.path.dirname(filepath) 
        if not utils.is_dir_exists(parent_folder):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory Does Not Exists {parent_folder}"
            )
        
        # creating logger 
        result = utils.write_txt_file(
            filepath=filepath,
            data=f'[{datetime.datetime.now()}] Created Logger File\n',
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
            data=f"Logger Storage Is  Created at {filepath}"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
def get_logged_entries(filepath , number_of_lines:int=-1 , reversed_reading:bool=True):

    '''all lines are loaded by default  Returns List of log lines'''
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Log File Not Found"
            )
        
        # reading the file
        log_result = utils.read_txt_file(filepath)

        # cannot read
        if not log_result:
            return Result(
                success= False,
                error_code=410,
                error_msg=f"Cannot Read Log File {log_result.error_msg}"
            )
       
        # converting whole log to lines list
        log_data_list = str(log_result.data).splitlines() # get data list
        
        # getting lines
        if number_of_lines != -1:
            log_data_list = log_data_list[:number_of_lines] # get desired lines


        # reversing the list 
        if reversed_reading:
            log_data_list = log_data_list[::-1] # reversed list

        # sending results
        return Result(
            success=True,
            data=log_data_list
        )
    
    except Exception as e :
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected Error {str(e).strip()}"
        )
            
def add_log_entry(filepath,data:str):
    '''appends to log '''
    try:
        # file does not exists 
        if not utils.is_file_exists(filepath):
            return Result(
                success=False,
                error_code=404,
                error_msg="Log File Not Found"
            )
        
        # auto adding new line on all logs if not already present 
        if not data.endswith('\n'):
            data += '\n'
        
        # auto adding time stamp 
        if not data.startswith(str(datetime.datetime.now())):
            data = f"[{str(datetime.datetime.now())}] {data}"
            
        # updating logger 
        result = utils.append_txt_file(
            filepath=filepath,
            new_data=data
        )
        if not result:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Cannot Append File : {result.error_msg}"
            )
        
        # send result 
        return Result(
            success=True,
            data=f"Entry Is Logged at {filepath}"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e).strip()}"
        )
