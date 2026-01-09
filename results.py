'''CONTAINS RESULTS CLASS FOR STORING RESULTS OF A FUNCTION'''
class Result:
    '''Store results'''
    def __init__(self ,success:bool,data:None,error_msg = None,error_code = None):
        '''Automatically called when a object is created '''
        self.ok = success                  # wether action succeed or not 
        self.data = data                   # result of the action
        self.error_msg = error_msg         # error description
        self.error_code = error_code       # error code specific 

    def __bool__(self):
        '''Called when used as argument for if eg- if Result : '''
        return self.ok # true of false
    
    def __str__(self):
        '''Called when used as argument for print statement eg- print(Result)'''
        if self.ok :
            # if succeed 
            return f"Success : {self.data}" # returns data stored
        else :
            # if error occurred
            return f"Error [{self.error_code}] : {self.error_msg}" # returns error msg with error code 
