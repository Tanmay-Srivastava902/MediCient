'''CONTAINS RESULTS CLASS FOR STORING RESULTS OF A FUNCTION'''
from typing import Any


class Result:
    '''Store results of a function'''
    UNKNOWN_ERROR=1
    EXECUTION_ERROR: int = 100
    PIP_ERROR: int = 101
    VENV_ERROR: int = 102
    SERVICE_ERROR: int = 300
    SERVICE_RUNNING: int = 301
    SERVICE_STOPPED: int = 302
    SERVICE_NOT_INSTALLED: int = 303
    MYSQL_ERROR: int = 200
    USER_AUTH_ERROR :int = 201
    FOLDER_ALREADY_EXISTS_ERROR: int = 400
    FOLDER_NOT_FOUND_ERROR: int = 401
    FILE_ALREADY_EXISTS_ERROR: int = 402
    FILE_NOT_FOUND_ERROR: int = 404
    FOLDER_NOT_EMPTY: int = 409
    GENERAL_FILE_ERROR: int = 410
    KEY_NOT_FOUND_ERROR: int = 500


    def __init__(self, success:bool ,data : Any = '', error_msg: str = '', error_code: int = 1):
        '''Create a Result object'''
        self.ok = success          # wether succeed or not
        self.data = data           # data when successful (empty string = failed)
        self.error_msg = error_msg       # error description when failed
        self.error_code = error_code     # error code number

    def __bool__(self):
        '''if result: checks if success'''
        return self.ok
    
    def __str__(self):
        '''print(result) shows success or error'''
        if self.ok:  # if success is not empty
            return f"Success : {self.data}"
        else:  # if success is empty = error
            return f"Error [{self.error_code}] : {self.error_msg}"
    def get_data(self):
        '''Get the success data'''
        return self.data    
    def get_error(self):
        '''Get error code and message together'''
        return self.error_code, self.error_msg
