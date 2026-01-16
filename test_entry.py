# # =========================
# # executor.py testing
# # =========================

from utils import system_executor , python_executor , mysql_executor

print("="*50)
print("EXECUTOR LAYER TEST SUITE")
print("="*50)

# Test 1: System executor
print("\n[TEST 1] System Executor - Simple command")
result = system_executor(['echo', 'hello'])
if result:
    print(f"✔️ Return code: {result.returncode}")
    print(f"  Output: {result.stdout.strip()}")

# Test 2: Python executor - Script mode
print("\n[TEST 2] Python Executor - Script mode")
result = python_executor(['-c', 'print(30 > 20)'])
if result:
    print(f"✔️ Return code: {result.returncode}")
    print(f"  Output: {result.stdout.strip()}")

# Test 3: Python executor - Module mode
print("\n[TEST 3] Python Executor - Module mode")
result = python_executor(['pip', 'list'], run_module=True)
if result:
    print(f"✔️ Return code: {result.returncode}")
    print(f"  Output: {result.stdout[:100]}...")  # First 100 chars

# Test 4: Both flags (should fail)
print("\n[TEST 4] Python Executor - Both flags (should fail)")
result = python_executor(['test'], run_module=True, interactive_mode=True)
if not result:
    print("✔️ Correctly rejected both flags")

# Test 5: System executor without sudo password (should fail)
print("\n[TEST 5] System Executor - Missing sudo password")
result = system_executor(['systemctl', 'status', 'mysql'], sudo_access=True)
if not result:
    print("✔️ Correctly rejected missing password")

print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)



# # =========================
# # file.py testing
# # =========================

from utils import is_file_exists, delete_file, write_txt_file, append_txt_file, read_txt_file, write_binary_file, read_binary_file, write_json_file, read_json_file ,create_dir , is_dir_exists,delete_dir
import os

print("="*50)
print("FILE OPERATION LAYER TEST SUITE")
print("="*50)


# Test 1: is_file_exists (with present file)
print("\n[TEST 1] FILE EXISTENCE ")
result = is_file_exists('folder.py')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 2: is_file_exists (with absent  file)
print("\n[TEST 2] FILE ABSENCE ")
result = is_file_exists('absent.py')
if not result:
    print(f" ✔️ Tested Ok : {result}")

# txt file
# Test 3: create file
print("\n[TEST 3] FILE CREATION ")
result = write_txt_file('test.txt','TEXT FILE TEST IS CREATED')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 4: create file without overwrite
print("\n[TEST 4] FILE OVERWRITE PROTECTION ")
result = write_txt_file('test.txt','TEXT FILE TEST IS CREATED')
if not result:
    print(f" ✔️ Tested Ok : {result}")

# Test 5: create file with overwrite
print("\n[TEST 5] FILE  OVERWRITE ")
result = write_txt_file('test.txt','TEXT FILE TEST IS OVERWRITTEN',overwrite=True)
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 6: update file 
print("\n[TEST 6] FILE UPDATE ")
result = append_txt_file('test.txt','TEXT FILE TEST IS APPENDED')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 7: read text file 
print("\n[TEST ]7 FILE READ ")
result = read_txt_file('test.txt')
if result:
    print(f" ✔️ Tested Ok : {result}")

# binary 
# Test 8: create binary file
print("\n[TEST 8] FILE CREATION ")
result = write_binary_file('test.bin','BINARY  FILE  IS CREATED')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 9: create binary file without overwrite
print("\n[TEST 9] FILE OVERWRITE PROTECTION ")
result = write_binary_file('test.bin','BINARY TEST IS CREATED')
if not result:
    print(f" ✔️ Tested Ok : {result}")

# Test 10: create binary file with overwrite
print("\n[TEST 10] FILE  OVERWRITE ")
result = write_binary_file('test.bin','BINARY TEST IS OVERWRITTEN',overwrite=True)
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 11: read binary file 
print("\n[TEST 11] FILE READ ")
result = read_binary_file('test.bin')
if result:
    print(f" ✔️ Tested Ok : {result}")

# json 
# Test 12: create json file
print("\n[TEST 12] FILE CREATION ")
result = write_json_file('test.json',{"FILE":'JSON  FILE  IS CREATED'})
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 13: create json file without overwrite
print("\n[TEST 13] FILE OVERWRITE PROTECTION ")
result = write_json_file('test.json',{"FILE":'JSON  FILE  IS CREATED'})
if not result:
    print(f" ✔️ Tested Ok : {result}")

# Test 14: create json file with overwrite
print("\n[TEST 14] FILE  OVERWRITE ")
result = write_json_file('test.json',{"FILE":'json TEST IS OVERWRITTEN'},overwrite=True)
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 15: read json file 
print("\n[TEST 15] FILE READ ")
result = read_json_file('test.json')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 16: delete json file 
print("\n[TEST 16] FILE DELETED ")
result = delete_file('test.json')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 17: delete binary file 
print("\n[TEST 17] FILE DELETED ")
result = delete_file('test.bin')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 18: delete txt file 
print("\n[TEST 18] FILE DELETED ")
result = delete_file('test.txt')
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 19: read json file (not existing)
print("\n[TEST 19] FILE READ ")
result = read_json_file('test.json')
if not result:
    print(f" ✔️ Tested Ok : {result}")
# Test 20: read binary file (not existing)
print("\n[TEST 20] FILE READ ")
result = read_binary_file('test.bin')
if not result:
    print(f" ✔️ Tested Ok : {result}")

# Test 21: read txt file (not existing)
print("\n[TEST 21] FILE READ ")
result = read_txt_file('test.txt')
if not result:
    print(f" ✔️ Tested Ok : {result}")

# folder tests
# Test 22: create folder parent dir  (not existing)
print("\n[TEST 22] FOLDER CREATION EXISTENCE CHECK ")
result = create_dir('unknown_path/dir_test',449)
if not result:
    print(f" ✔️ Tested Ok : {result}")

# Test 23: create folder parent dir (exists) current dir  with mode 
print("\n[TEST 23] FOLDER CREATION MODE SPECIFIED ")
result = create_dir(os.getcwd(),555)
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 24: folder deletion (existing)
print("\n[TEST 24] FOLDER DELETION")
result = delete_dir(os.path.join(os.getcwd(),'dir_test'))
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 25: folder deletion (not existing)
print("\n[TEST 24] FOLDER DELETION")
result = delete_dir(os.path.join(os.getcwd(),'dir_test'))
if result:
    print(f" ✔️ Tested Ok : {result}")

# Test 26: is folder exists 
print("\n[TEST 21] FOLDER EXISTENCE CHECK ")
result = is_dir_exists(os.path.join(os.getcwd(),'utils'))
if result:
    print(f" ✔️ Tested Ok : {result}")



print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)
pass




# #=================================
# # ENCRYPTION KEY FILE encryption.py
# #=================================
import os 
import utils 
from config_managers import load_encryption_key,init_encryption_key

print("="*50)
print("ENCRYPTION KEY TEST SUITE")
print("="*50)

# required key credentials
filepath = os.path.expanduser('~/.config/.medicient/app_encryption_key.key')
app_dirpath = os.path.expanduser('~/.config/.medicient')
config_dir_path =  os.path.expanduser('~/.config')

# checking config and medicient folder 
if not utils.is_dir_exists(config_dir_path):
    print(utils.create_dir(config_dir_path,mode=0o700))

if not utils.is_dir_exists(app_dirpath):
    print(utils.create_dir(app_dirpath,mode=0o700))

# Test 1:load key (key does not  exists)
print("\n[TEST 1] LOAD KEY - (does not  exists) ")
result = load_encryption_key(filepath)
if not result:
    print(f" ✔️ Tested Ok key: {result}")


# Test 2:initialize encryption key 
print("\n[TEST 2] INITIALIZING KEY - (not already exists) ")
key1 = utils.generate_fernet_key()
result1 = init_encryption_key(app_dirpath,filepath,key1)
if result1:
    print(f" ✔️ Tested Ok : {result1}")
else:
    print(f"❌ key does not initialized {result1}")

    # Test 3:load key (key does not  exists)
print("\n[TEST 3] LOAD KEY - (already exists) ")
result = load_encryption_key(filepath)
if  result:
    print(f" ✔️ Tested Ok key: {result}")
else:
    print(f"❌ key does not Loaded {result1}")



# Test 4:initialize encryption key
print("\n[TEST 4] INITIALIZING KEY - (already exists) ")
key2 = utils.generate_fernet_key()
result2 = init_encryption_key(app_dirpath,filepath,key2)
if  result:
    print(f" ✔️ Tested Ok : {result2}")
else:
    print(f"❌ key does not re-initialized {result1}")

# Test 4 
    # Test 4:load key (key does not  exists)
print("\n[TEST 4] LOAD KEY - (after re-initialization) ")
result = load_encryption_key(filepath)
# result must be same created successfully but not key 
if key1 != key2  and result1 == result2:
    print(f" ✔️ Tested Ok : {result2}")
    print(f"old key : {key1}")
    print(f"new key : {key2}")

input("press enter to complete setup ")
utils.delete_dir(app_dirpath,forced=True,disable_prompt=True) # removing dir for safety

print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)


# #=================================
# # INSTALL MARKER FILE install_marker.py
# #=================================
import os 
import datetime
import utils 
from config_managers import init_install_marker , load_install_marker_data

print("="*50)
print("INSTALL MARKER TEST SUITE")
print("="*50)

# required key credentials
filepath = os.path.expanduser('~/.config/.medicient/install_marker.medisecure')
app_dirpath = os.path.expanduser('~/.config/.medicient')
config_dir_path =  os.path.expanduser('~/.config')

# checking config and medicient folder 
if not utils.is_dir_exists(config_dir_path):
    print(utils.create_dir(config_dir_path,mode=0o700))

if not utils.is_dir_exists(app_dirpath):
    print(utils.create_dir(app_dirpath,mode=0o700))

# Test 1:load Install Merer (INSTALL MARKER does not  exists)
print("\n[TEST 1] LOAD INSTALL MARKER - (does not  exists) ")
result = load_install_marker_data(filepath)
if not result:
    print(f" ✔️ Tested Ok INSTALL MARKER: {result}")


# Test 2:initialize encryption INSTALL MARKER 
print("\n[TEST 2] INITIALIZING INSTALL MARKER - (not already exists) ")
metadata1 = {
  "app_name": "medicient",
  "version": "1.0.0",
  "install_time":datetime.datetime.now().isoformat(),
  "install_user": "curiousme",
  "install_path": "/home/curiousme/myproject/medicient",
  "system": "Linux",
  "python_version": "3.12.1",
  "marker_version": "1",
  "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab"
}
result1 = init_install_marker(filepath,metadata1)
if result1:
    print(f" ✔️ Tested Ok : {result1}")
else:
    print(f"❌ INSTALL MARKER does not initialized {result1}")

# Test 3:load INSTALL MARKER (INSTALL MARKER does not  exists)
print("\n[TEST 3] LOAD INSTALL MARKER - (already exists) ")
result = load_install_marker_data(filepath)
if  result:
    print(f" ✔️ Tested Ok INSTALL MARKER: {result}")
else:
    print(f"❌ INSTALL MARKER does not Loaded {result1}")



# Test 4:Re-initialize INSTALL MARKER
print("\n[TEST 4] RE-INITIALIZING INSTALL MARKER - (already exists) ")
metadata2 = {
  "app_name": "medicient",
  "version": "1.0.1",
  "install_time":datetime.datetime.now().isoformat(),
  "install_user": "curiousme",
  "install_path": "/home/curiousme/myproject/medicient",
  "system": "Linux",
  "python_version": "3.12.1",
  "marker_version": "1",
  "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890abc"
}
result2 = init_install_marker(filepath,metadata2)
if  result:
    print(f" ✔️ Tested Ok : {result2}")
else:
    print(f"❌ INSTALL MARKER does not re-initialized {result1}")

# Test 4 
    # Test 4:load INSTALL MARKER (INSTALL MARKER exists)
print("\n[TEST 4] LOAD INSTALL MARKER - (after re-initialization) ")
result = load_install_marker_data(filepath)
# result must be same created successfully but not INSTALL MARKER 
if metadata1 != metadata2  and result1 != result2:
    print(f" ✔️ Tested Ok : {result2}")
    print(f"\nold INSTALL MARKER : {metadata1}")
    print(f"\nnew INSTALL MARKER : {metadata2}")

input("press enter to complete setup ")
utils.delete_dir(app_dirpath,forced=True,disable_prompt=True) # removing dir for safety

print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)


# #=================================
# # LOGGER FILE logger.py
# #=================================
from config_managers import init_logger_storage , get_logged_entries ,add_log_entry
import os
import utils



print("="*50)
print("LOGGER TEST SUITE")
print("="*50)

# required key credentials
LOG_PATH = os.path.join(os.getcwd(),'configs/app_logger.log')
app_dirpath = os.path.join(os.getcwd(),'configs')

if not utils.is_dir_exists(app_dirpath):
    print(utils.create_dir(app_dirpath,mode=0o700))

# Test 1: Initialize logger storage
print("\n[TEST 1] Initialize Logger Storage")
result = init_logger_storage(LOG_PATH)
if result and result.ok:
    print(f"✔️ Logger created: {result.data}")
else:
    print(f"❌ Failed to create logger: {result.error_msg}")

# Test 2: Add log entries
print("\n[TEST 2] Add Log Entries")
log_result1 =  add_log_entry(filepath=LOG_PATH,data="INFO: First log entry\n")
log_result2 =add_log_entry(filepath=LOG_PATH,data="ERROR: Something went wrong\n")
log_result3 = add_log_entry(filepath=LOG_PATH,data="DEBUG: Debugging info\n")

if log_result1 and log_result2 and log_result3:
    print("✔️ Log entries added.")
    print()
else:
    print(f"❌ Failed to Log : {log_result1.error_msg}")
    print(f"❌ Failed to Log : {log_result2.error_msg}")
    print(f"❌ Failed to Log : {log_result3.error_msg}")

# Test 3: Read all log entries
print("\n[TEST 3] Read All Log Entries")
result = get_logged_entries(LOG_PATH)
if result and result.ok and result.data is not None:
    print("✔️  Test Ok \nLog entries:")
    for line in result.data:
        print(line.strip())
else:
    print(f"❌ Failed to read log: {result.error_msg}")

# Test 4: Read last 2 log entries (if supported)
print("\n[TEST 4] Read Last 2 Log Entries")
result = get_logged_entries(LOG_PATH, number_of_lines=2)
if result and result.ok and result.data is not None:
    print("✔️ Tested Ok \nLast 2 log entries:")
    for line in result.data:
        print(line.strip())
else:
    print(f"❌ Failed to read log: {result.error_msg}")

input("press enter to complete setup ")
# Cleanup
utils.delete_file(LOG_PATH) 

print("\n" + "="*50)
print("LOGGER TESTS COMPLETE")
print("="*50)

# =========================
# schema.py testing
# =========================
from config_managers.schema import create_database_schema
import os
from results import Result
print("="*50)
print("SCHEMA CREATION TEST SUITE")
print("="*50)

SCHEMA_PATH = "test_schema.sql"

# Test 1: Create database schema file
print("\n[TEST 1] Create Database Schema File")
result = create_database_schema(SCHEMA_PATH)
if result and result.ok:
	print(f"✔️ Schema file created: {result.data}")
else:
	print(f"❌ Failed to create schema: {result.error_msg}")

input("press enter to complete setup ")
# Cleanup
if os.path.exists(SCHEMA_PATH):
	os.remove(SCHEMA_PATH)
print("\n" + "="*50)
print("SCHEMA TESTS COMPLETE")
print("="*50)

# =========================
# passwords.py testing
# =========================
import config_managers
# import utils
import os

test_file = "configs/test_password.medisecure"

print("="*50)
print("PASSWORD MANAGER TEST SUITE")
print("="*50)
# Test 2: Add a user 
print("\n[TEST 2] ADD USER PASSWORD")
result = config_managers.update_password(test_file,'tanmay','helloSecret@23')
if not result:
    print(f"✔️ Tested Ok : {result} ")
else:
    print(f" ❌ Failed : {result}")

# Test 1: Initialize password storage
print("\n[TEST 1] INIT PASSWORD STORAGE")
result = config_managers.init_password_storage(test_file)
if result:
    print(f" ✔️ Tested Ok : {result}")
else:
    print(f" ❌ Failed : {result}")

# Test 2: Add a user 
print("\n[TEST 2] ADD USER PASSWORD")
result = config_managers.update_password(test_file,'tanmay','helloSecret@23')
if result:
    print(f"✔️ Tested Ok : {result} ")
else:
    print(f" ❌ Failed : {result}")

# Test 3: Get password for existing user
print("\n[TEST 3] GET EXISTING USER PASSWORD")
result = config_managers.get_password(test_file, "tanmay")
if result:
    print(f" ✔️ Tested Ok : {result}")
else:
    print(f" ❌ Failed : {result}")

# Test 4: Get password for non-existing user
print("\n[TEST 4] GET NON-EXISTING USER PASSWORD")
result = config_managers.get_password(test_file, "unknown")
if not result:
    print(f" ✔️ Tested Ok : {result}")
else:
    print(f" ❌ Failed : {result}")
    
input("press enter to cleanup and finish setup")
# Cleanup
os.remove(test_file)
print("\n" + "="*50)
print("PASSWORD TESTS COMPLETE")
print("="*50)

# =========================
# configs/config.json and config_managers/settings.py testing
# =========================
# import json
import config_managers
json_path = 'configs/test_config.json'

print("="*50)
print("CONFIGS/SETTINGS TEST SUITE")
print("="*50)

# Test 1: Load error codes from config.json (not exist)
print("\n[TEST 1] LOAD ERROR CODES FROM JSON (not exists)")
result = config_managers.get_config(filepath=json_path,all=True)
if not result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
    

# Test 2:initializing json
print("\n[TEST 2] creating json")
# from config_managers import settings
result = config_managers.init_config_storage(filepath=json_path)
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
    
# Test 3: testing json update (if available)
print("\n[TEST 3]  Testing Update")
# from config_managers import settings
result = config_managers.update_config(filepath=json_path,config_name='TEST_CONFIG',config_dict={"testing_key":"testing_value"})
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")

# test 4: Load error codes from config.json (exist)
print("\n[TEST 4] LOAD ERROR CODES FROM JSON (exists)")
result = config_managers.get_config(filepath=json_path,all=True)
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
    
# test 5: Load current updated config from config.json (exist)
print("\n[TEST 5] LOAD current updated config FROM JSON (exists) without config_name ")
result = config_managers.get_config(filepath=json_path,all=False)
if not  result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
      
    
# test 6: Load current updated config from config.json (exist)
print("\n[TEST 5] LOAD current updated config FROM JSON (exists) with config name")
result = config_managers.get_config(filepath=json_path,all=False,config_name="TEST_CONFIG")
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
      
print("press enter to cleanup")
# Cleanup
if os.path.exists(json_path):
    os.remove(json_path)
    print(f"Cleanup: Removed {json_path}")


print("\n" + "="*50)
print("CONFIGS/SETTINGS TESTS COMPLETE")
print("="*50)

# =========================
# session.py testing
# =========================
test_session_file = "configs/test_session.medisecure"

import config_managers
print("="*50)
print("SESSION TEST SUITE")
print("="*50)

#  test1" Get session (not exists)
print("\n[TEST 1] GET SESSION (file not exists)")
result = config_managers.get_session(test_session_file, "user1")
if not result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")


# Test 2: Initialize session storage
print("\n[TEST 2] INIT SESSION STORAGE")
result = config_managers.init_session_storage(test_session_file)
if result.ok:
	print(f" ✔️ Session storage initialized: {result}")
	if os.path.exists(test_session_file):
		print(f" ✔️ Session file created: {test_session_file}")
	else:
		print(f" ❌ Session file not found: {test_session_file}")
else:
	print(f" ❌ Failed to init session storage: {result}")

# Test 3: updating session
print("\n[TEST 3] updating session")
result = config_managers.update_session(test_session_file,"user1",{"session":{"user":"tanmay","host":"localhost","password":"Test@123"}})
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
    
# Test 3: Get session for correct user
print("\n[TEST 4] GET SESSION FOR MISSING USER")
result = config_managers.get_session(test_session_file, "user1")
if result.ok:
    print(f'✔️ TESTED OK : {result}')
else:
    print(f"❌ TEST FAILED :{result}")
    
# Test 5 : getting session for missing user 
print("\n[TEST 5] GET SESSION FOR MISSING USER")
result = config_managers.get_session(test_session_file, "user10")
if not result.ok:
	print(f" ✔️ get_session handles missing user: {result}")
else:
	print(f" ❌ Unexpected success: {result}")
     
print("press enter to cleanup")
# Cleanup
if os.path.exists(test_session_file):
    os.remove(test_session_file)
    print(f"Cleanup: Removed {test_session_file}")

print("\n" + "="*50)
print("SESSION TESTS COMPLETE")
print("="*50)

