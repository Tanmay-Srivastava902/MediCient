"""UNIVERSAL FILE HANDLER WITH BASIC CRUD FOLDER OPERATIONS """
import os 
import json
import pickle
from results import Result
# universal file handler
def is_file_exists(filepath)->bool:
    return os.path.isfile(filepath)

def delete_file(filepath)->Result:
    if os.path.isfile(filepath):
        os.remove(filepath)
        return Result(
                    success=True,
                        data=f"{filepath} deleted successfully"
                     )
    else : 
       return Result(
                success=False,
                error_msg=f"{filepath} file does not exists",
                error_code=404
            )
    
# specific to file types
# txt
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
                    data=f"{filepath} created successfully"
                    )
        
def append_txt_file(filepath,new_data):
    if os.path.exists(filepath):
        with open(filepath,'a') as f :
            f.write(new_data)
        return Result(
                        success=True,
                        data=f"{filepath} updated successfully"
                        )
    else:
        return Result(
            success=False,
            error_msg=f"{filepath} file does not exists",
            error_code=404
            )
def read_txt_file(filepath)->Result:
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
# NOTE update is prohibited for json and binary due to object content possibilities
# binary
def write_binary_file(filepath,data,overwrite=False):
    '''Create a binary file'''
    if os.path.isfile(filepath) and not overwrite:
        return Result(
            success=False,
            error_msg=f"file already exists cannot overwrite try again with  overwrite = True",
            error_code=402
            )
    
    with open(filepath,'wb') as f :
        pickle.dump(data,f)
    return Result(
                    success=True,
                    data=f"{filepath} created successfully"
                    )


def read_binary_file(filepath):
    if os.path.exists(filepath):
        with open(filepath,'rb') as f :
            data = pickle.load(f)
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

# json
def write_json_file(filepath,json_dict:dict,overwrite=False):

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
                    data=f"{filepath} created successfully"
                    )


def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath,) as f :
            data = json.load(f)
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



# =============================
# BASIC FOLDER OPERATIONS
# =============================

import os
def is_dir_exists(dirpath):
    return os.path.isdir(dirpath)

def create_dir(parent_dirpath,dirname,mode:int=511):
    if os.path.isdir(parent_dirpath):
        dir_path = os.path.join(parent_dirpath,dirname)
        os.makedirs(dir_path,exist_ok=True)
        return Result(
                success=True,
                data=f"Folder {dir_path} Created Successfully"
        )

    else:
        return Result(
                success=False,
                error_msg=f"Folder {parent_dirpath} Does Not  Exists",
                error_code=401
        )

def delete_dir(dirpath,forced=False):
    import shutil
    if os.path.isdir(dirpath):
        if len(os.listdir(dirpath)) > 0  and not forced:
            
             return Result(
                            success=False,
                            error_msg=f"Folder {dirpath} Is Not Empty Please Retry With  Forced = True",
                            error_code=409
                          )
        input(f"⚠️ Warning ! You Are Going TO Delete Directory {dirpath}\nPress Enter To Continue or press Ctrl + C to Abort And Exit")
        shutil.rmtree(dirpath)
        return Result(
                success=True,
                data=f"Folder {dirpath} Deleted Successfully"
        )

    else:
        return Result(
                success=False,
                error_msg=f"Folder {dirpath} Does Not Exists",
                error_code=401
        )



# 
if __name__ == "__main__":
    print("="*50)
    print("FILE OPERATION LAYER TEST SUITE")
    print("="*50)
    

    # Test 1: is_file_exists (with present file)
    print("\n[TEST 1] FILE EXISTENCE ")
    result = is_file_exists('folder.py')
    if result:
        print(f" ✓ Tested Ok : {result}")
   
    # Test 2: is_file_exists (with absent  file)
    print("\n[TEST 2] FILE ABSENCE ")
    result = is_file_exists('absent.py')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # txt file
    # Test 3: create file
    print("\n[TEST 3] FILE CREATION ")
    result = write_txt_file('test.txt','TEXT FILE TEST IS CREATED')
    if result:
        print(f" ✓ Tested Ok : {result}")
   
    # Test 4: create file without overwrite
    print("\n[TEST 4] FILE OVERWRITE PROTECTION ")
    result = write_txt_file('test.txt','TEXT FILE TEST IS CREATED')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 5: create file with overwrite
    print("\n[TEST 5] FILE  OVERWRITE ")
    result = write_txt_file('test.txt','TEXT FILE TEST IS OVERWRITTEN',overwrite=True)
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 6: update file 
    print("\n[TEST 6] FILE UPDATE ")
    result = append_txt_file('test.txt','TEXT FILE TEST IS APPENDED')
    if result:
        print(f" ✓ Tested Ok : {result}")

    # Test 7: read text file 
    print("\n[TEST ]7 FILE READ ")
    result = read_txt_file('test.txt')
    if result:
        print(f" ✓ Tested Ok : {result}")
   
   # binary 
    # Test 8: create binary file
    print("\n[TEST 8] FILE CREATION ")
    result = write_binary_file('test.bin','BINARY  FILE  IS CREATED')
    if result:
        print(f" ✓ Tested Ok : {result}")
   
    # Test 9: create binary file without overwrite
    print("\n[TEST 9] FILE OVERWRITE PROTECTION ")
    result = write_binary_file('test.bin','BINARY TEST IS CREATED')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 10: create binary file with overwrite
    print("\n[TEST 10] FILE  OVERWRITE ")
    result = write_binary_file('test.bin','BINARY TEST IS OVERWRITTEN',overwrite=True)
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 11: read binary file 
    print("\n[TEST 11] FILE READ ")
    result = read_binary_file('test.bin')
    if result:
        print(f" ✓ Tested Ok : {result}")

   # json 
    # Test 12: create json file
    print("\n[TEST 12] FILE CREATION ")
    result = write_json_file('test.json',{"FILE":'JSON  FILE  IS CREATED'})
    if result:
        print(f" ✓ Tested Ok : {result}")
   
    # Test 13: create json file without overwrite
    print("\n[TEST 13] FILE OVERWRITE PROTECTION ")
    result = write_json_file('test.json',{"FILE":'JSON  FILE  IS CREATED'})
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 14: create json file with overwrite
    print("\n[TEST 14] FILE  OVERWRITE ")
    result = write_json_file('test.json',{"FILE":'json TEST IS OVERWRITTEN'},overwrite=True)
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 15: read json file 
    print("\n[TEST 15] FILE READ ")
    result = read_json_file('test.json')
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 16: delete json file 
    print("\n[TEST 16] FILE DELETED ")
    result = delete_file('test.json')
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 17: delete binary file 
    print("\n[TEST 17] FILE DELETED ")
    result = delete_file('test.bin')
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 18: delete txt file 
    print("\n[TEST 18] FILE DELETED ")
    result = delete_file('test.txt')
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 19: read json file (not existing)
    print("\n[TEST 19] FILE READ ")
    result = read_json_file('test.json')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    # Test 20: read binary file (not existing)
    print("\n[TEST 20] FILE READ ")
    result = read_binary_file('test.bin')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 21: read txt file (not existing)
    print("\n[TEST 21] FILE READ ")
    result = read_txt_file('test.txt')
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    

    # folder tests
    # Test 22: create folder parent dir  (not existing)
    print("\n[TEST 22] FOLDER CREATION EXISTENCE CHECK ")
    result = create_dir('unknown/path','dir_test',)
    if not result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 23: create folder parent dir (exists) current dir  with mode 
    print("\n[TEST 23] FOLDER CREATION MODE SPECIFIED ")
    result = create_dir(os.getcwd(),'dir_test',mode=700)
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 24: folder deletion (existing)
    print("\n[TEST 24] FOLDER DELETION")
    result = delete_dir(os.path.join(os.getcwd(),'dir_test'))
    if result:
        print(f" ✓ Tested Ok : {result}")
   
    # Test 25: folder deletion (not existing)
    print("\n[TEST 24] FOLDER DELETION")
    result = delete_dir(os.path.join(os.getcwd(),'dir_test'))
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    # Test 26: is folder exists 
    print("\n[TEST 21] FOLDER EXISTENCE CHECK ")
    result = is_dir_exists(os.path.join(os.getcwd(),'utils'))
    if result:
        print(f" ✓ Tested Ok : {result}")
    
    

    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50)
    




