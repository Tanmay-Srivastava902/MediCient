'''Manages encryption hashing for security'''

from cryptography.fernet import Fernet , InvalidToken
# depends on  nothing (encryption key) 
# let the exceptions flow to the caller till higher level
def generate_fernet_key():
    
    return Fernet.generate_key()

def __create_fernet_instance(key:bytes):
    from cryptography.fernet import Fernet 
    return Fernet(key)
        
def get_base64_urlsafe_data(data:str):
    '''for fernet encoding only'''
    import base64 
    return base64.urlsafe_b64encode(data.encode()).decode()

def decode_base64_urlsafe_data(data:str):
    '''for fernet encoding only'''
    import base64 
    return base64.urlsafe_b64decode(data).decode()

def hash_data(data:str):
    import hashlib 
    return hashlib.sha256(data.encode()).hexdigest()

# depends on (fernet_instance)
def encrypt(key:bytes,data:str):
    fernet = __create_fernet_instance(key)
    return fernet.encrypt(data.encode())

def decrypt(key:bytes,data:bytes):
    try:
        fernet  = __create_fernet_instance(key)
        return fernet.decrypt(data).decode()
    except (InvalidToken,ValueError):
        print("❌ Invalid Key Provided")
        return None

if __name__ == "__main__":
    
    print("\n" + "="*50)
    print("PROMPTS TEST SUIT")
    print("="*50)

    
    # Test 1: get base64 data 
    print("\n[TEST 1] BASE64 ENCODING ")
    base_encoded_result = get_base64_urlsafe_data('SECURE DATA : SECRET !!!❤️') 
    if base_encoded_result:
        print(f"✓ Check Passed Data: {base_encoded_result}")
    
    # Test 2: decode base64 data 
    print("\n[TEST 2] BASE64 DECODING ")
    result = decode_base64_urlsafe_data(base_encoded_result) 
    if result:
        print(f"✓ Check Passed Data: {result}")
    
    # Test 3: hash data 
    print("\n[TEST 3] HASHING DATA")
    result = hash_data('SECURE DATA : SECRET !!!❤️') 
    if result:
        import hashlib 
        original_hash = hashlib.sha256('SECURE DATA : SECRET !!!❤️'.encode()).hexdigest()
        if original_hash == result:
            print(f"✓ Check Passed Data: {result}")
        else :
            print(f"❌ Check Failed: {result}")
    

    # Test 4: generate fernet key 
    print("\n[TEST 4] GENERATING ENCRYPTION KEY")
    fernet_key = generate_fernet_key()
    if Fernet(fernet_key):
        print(f"✓ Check Passed Key: {fernet_key}")
    
    # Test 5: encrypt data (with a key fixed)
    print("\n[TEST 5] ENCRYPTING  DATA")
    encoded_result = encrypt(fernet_key,'SECURE DATA : SECRET !!!❤️') 
    if encoded_result:
        print(f"✓ Check Passed Data: {encoded_result}")
       
    # Test 6: decrypting  data (with wrong key )
    print("\n[TEST 6] DECRYPTING  DATA - wrong key ")
    decoded_result = decrypt('wrong_secure_key'.encode(),encoded_result) 
    if not decoded_result:
        print(f"✓ Check Passed Data: {decoded_result}")
    
    # Test 7: decrypting  data (with correct  key )
    print("\n[TEST 7] DECRYPTING  DATA  - correct key ")
    decoded_result = decrypt(fernet_key,encoded_result) 
    if decoded_result:
        print(f"✓ Check Passed Data: {decoded_result}")


    
       
    

    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50)



