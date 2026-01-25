'''GENERAL PROMPTS OPERATIONS'''

def get_password_input(msg="Enter Password : ",security_checks:bool=False) -> str | None:
    '''
    :returns password: str if requirements satisfied 
    :returns None: if requirements not satisfied
    '''
    import getpass
    if not security_checks :
        password = getpass.getpass(msg).strip() 
        return password
    else:
        print('Password Should Have - \n[one uppercase][one lowercase][one digit]\n[one special symbol "!@#$%^&*()-_=+"][no spaces in between]')
        password = getpass.getpass(msg).strip() 
        confirm_password = getpass.getpass("Confirm Password : ").strip() 
        if password == confirm_password :
            check_length=       len(password) > 8  
            check_upper_case=   any(i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for i in password)
            check_lower_case=   any(i in 'abcdefghijklmnopqrstuvwxyz' for i in password)
            check_digit=        any(i.isdigit() for i in password)
            check_special_char= any(i in '!@#$%^&*()-_=+' for i in password)
            check_spaces=       ' ' not in password

            if ( check_digit and check_length 
                and check_lower_case and check_upper_case 
                and check_special_char and check_spaces):
                return password 
            else:
                print(f"❗Password Requirement Not Satisfied")
                return None
        else:
            print("❗Password And Confirm Password Not Matched")
            return None
    
def confirm(msg="Do You Want To Continue (y/n) : ")->bool|None:
    '''returns true if yes False for no else None for Invalid Response'''
    response = input(msg).strip().lower()
    if response in ['y','n']:
        return response == 'y'
    else:
        print(f"Invalid Response {response}")
        return None
def validate_input(ipt:str,min_length:int,max_length:int,blocked_chars:list[str]=[],required_chars:list[str]=[]):
    # length check
    if len(ipt) < min_length or len(ipt) > max_length:
        return False
    # required char check [as this requires less memory only few chars to iterate over]
    for required_char in required_chars:
        if required_char not in ipt:
            return False
    # blocked char check [requsires more memory whole ipt is to iterate over]
    for char in ipt:
        if char in blocked_chars:
            return False
    # all checks passed
    return True 
            
    
    


if __name__ == "__main__":
    
    print("\n" + "="*50)
    print("PROMPTS TEST SUIT")
    print("="*50)


    # Test 1: get password input security checks = false
    print("\n[TEST 1] PASSWORD INPUT - No security Checks")
    result = get_password_input('Enter Password : ') 
    if result:
        print(f"✓ Check Passed Password: {result}")
    
    # Test 2: get password input security checks = false
    print("\n[TEST 2] PASSWORD INPUT - no confirm password match")
    result = get_password_input('Enter Password : ',security_checks=True) 
    if not result:
        print(f"✓ Check Passed Password: {result}")
    
    # Test 3: get password input security checks = True 
    # (ensuring  password always  meets security check)
    print("\n[TEST 3] PASSWORD INPUT - with security checks (always passed)")
    result = get_password_input('Enter Password ',security_checks=True) 
    if result:
        print(f"✓ Check Passed Password: {result}")
    
    # Test 4: get password input security checks = True 
    # (ensuring  password does not meet security checks)
    print("\n[TEST 4] PASSWORD INPUT - with security checks (intentionally failed)")
    result = get_password_input('Enter Password ',security_checks=True) 
    if not result:
        print(f"✓ Check Passed Password: {result}")
    
    
    # Test 4: confirm ( with invalid input)
    print("\n[TEST 5] confirmation (with invalid input )")
    result = confirm() 
    if result ==  None:
        print(f"✓ Check Passed Confirmation: {result}")
    
    # Test 5: confirm (with correct response)
    print("\n[TEST 6] confirmation (with correct response)")
    result = confirm() 
    if result != None:
        print(f"✓ Check Passed Confirmation: {result}")


    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50)



