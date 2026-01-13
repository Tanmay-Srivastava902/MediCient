from utils import system_executor , python_executor , mysql_executor

print("="*50)
print("EXECUTOR LAYER TEST SUITE")
print("="*50)

# Test 1: System executor
print("\n[TEST 1] System Executor - Simple command")
result = system_executor(['echo', 'hello'])
if result:
    print(f"✓ Return code: {result.returncode}")
    print(f"  Output: {result.stdout.strip()}")

# Test 2: Python executor - Script mode
print("\n[TEST 2] Python Executor - Script mode")
result = python_executor(['-c', 'print(30 > 20)'])
if result:
    print(f"✓ Return code: {result.returncode}")
    print(f"  Output: {result.stdout.strip()}")

# Test 3: Python executor - Module mode
print("\n[TEST 3] Python Executor - Module mode")
result = python_executor(['pip', 'list'], run_module=True)
if result:
    print(f"✓ Return code: {result.returncode}")
    print(f"  Output: {result.stdout[:100]}...")  # First 100 chars

# Test 4: Both flags (should fail)
print("\n[TEST 4] Python Executor - Both flags (should fail)")
result = python_executor(['test'], run_module=True, interactive_mode=True)
if not result:
    print("✓ Correctly rejected both flags")

# Test 5: System executor without sudo password (should fail)
print("\n[TEST 5] System Executor - Missing sudo password")
result = system_executor(['systemctl', 'status', 'mysql'], sudo_access=True)
if not result:
    print("✓ Correctly rejected missing password")

print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)



# =========================
# file.py testing
# =========================

from utils import is_file_exists, delete_file, write_txt_file, append_txt_file, read_txt_file, write_binary_file, read_binary_file, write_json_file, read_json_file ,create_dir , is_dir_exists,delete_dir
import os

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
pass






