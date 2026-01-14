# depends on specifically (file operation for create file , read file )
import utils
from results import Result
def init_encryption_key(dirpath,filepath,key:bytes)-> Result:
    '''gets encrypted key from caller returns 410 general file error and 401 if key folder not found'''
    try:
        if utils.is_dir_exists(dirpath):

            # key testing 
            result = utils.create_fernet_instance(key)
            if result :
                # creating file 
                utils.write_binary_file(filepath,key,overwrite=True) # always overwrite 
                return Result(
                            success=True,
                            data=f"encryption key Created {filepath}"
                        )
            else:
                 return Result(
                        success=False,
                        error_code=410,
                        error_msg=f" ❌ Key Is Not Valid Fernet key use generate_fernet_key to get key"
                     )

        else :
            return Result(
                            success=False,
                            error_code=401,
                            error_msg=f"folder does not exists {dirpath}"
                        )
    except Exception as e :
        return Result(
                        success=False,
                        error_code=410,
                        error_msg=str(e)
                     )
    
def load_encryption_key(filepath) -> Result:
    '''give encryption key to caller'''
    try:
        result  = utils.read_binary_file(filepath)
        if result :
            return Result(
                            success=True,
                            data=result.data
                        )
        else:
            return result # file does not exists result returned
    except Exception as e :
        return Result(
                        success=False,
                        error_code=410,
                        error_msg=str(e)
                     )

if __name__ == "__main__":

    print("="*50)
    print("ENCRYPTION KEY TEST SUITE")
    print("="*50)
    
    # required key credentials
    filepath = 'configs/.app_key/encryption.key'
    dirpath = 'configs/.app_key'
    
    # Test 1:load key (key does not  exists)
    print("\n[TEST 1] LOAD KEY - (does not  exists) ")
    result = load_encryption_key(filepath)
    if not result:
        print(f" ✓ Tested Ok key: {result}")
    
    # creating key dir for testing remaining 
    res = utils.create_dir('configs/','.app_key',700)
    print(res)

    # Test 2:initialize encryption key 
    print("\n[TEST 2] INITIALIZING KEY - (not already exists) ")
    key1 = utils.generate_fernet_key()
    result1 = init_encryption_key(dirpath,filepath,key1)
    if result:
        print(f" ✓ Tested Ok : {result1}")

     # Test 3:load key (key does not  exists)
    print("\n[TEST 3] LOAD KEY - (already exists) ")
    result = load_encryption_key(filepath)
    if  result:
        print(f" ✓ Tested Ok key: {result}")
    
    
    # Test 4:initialize encryption key
    print("\n[TEST 4] INITIALIZING KEY - (already exists) ")
    key2 = utils.generate_fernet_key()
    result2 = init_encryption_key(dirpath,filepath,key2)
    if  result:
        print(f" ✓ Tested Ok : {result2}")
    
    # Test 4 
     # Test 4:load key (key does not  exists)
    print("\n[TEST 4] LOAD KEY - (after re-initialization) ")
    result = load_encryption_key(filepath)
    # result must be same created successfully but not key 
    if key1 != key2  and result1 == result2:
        print(f" ✓ Tested Ok : {result2}")
        print(f"old key : {key1}")
        print(f"new key : {key2}")
    
    utils.delete_dir(dirpath,forced=True) # removing dir for safety
    
    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50)
    pass



    


