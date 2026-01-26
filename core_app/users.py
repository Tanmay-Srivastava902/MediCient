# create user 
from mysql.connector.abstracts import MySQLCursorAbstract
from data_operators import records
from utils import prompt , security
import errors
import datetime
import options
# TODO :- add password encryption to register function and use decryption for login 
def is_user_exists(cursor:MySQLCursorAbstract,email:str='',user_id:int=-1)->bool:
    try:
        if user_id == -1 and not email :
            raise errors.InvalidArgumentError(f'please specify verification method userid or user email')
        elif user_id != -1:
            records.select_record(
                    cursor=cursor,
                    table='user',
                    columns_list=['user_id'],
                    where_clause=[{'user_id':user_id}]
                )
        else:
            records.select_record(
                    cursor=cursor,
                    table='user',
                    columns_list=['email'],
                    where_clause=[{'email':email}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check user existence: {str(e).strip()}')
def verify_admin_identity(original_passphrase:str):
    '''takes original passphrase and compared with the user input to verify the identity of user as admin'''
    try:
        print("verifying you admin identity")
        # taking passphrase 
        ipt_passphrase = prompt.get_password_input(msg="Enter Secret Passphrase: ")
        return ipt_passphrase == original_passphrase
    except Exception as e :
        raise errors.DBError(f'Could not verify your identity: {str(e).strip()}')
    
def know_your_user_id(cursor:MySQLCursorAbstract,email:str='')->int|None:
    '''gets **int user id** for given email if any or **none** if not found or invalid user or max attempts tried'''
    if not email:
        for i in range(3): 
            email = input(f'Enter User Email Address to know your uid [attempt {i}/3]:  ')
            if not prompt.validate_email(email):
                print(f"❗Invalid Email : {email}")
                continue
            break
        else:
            print(f'too many failed attempts please try again later')
            return None
    try:
        user_record = records.select_record(
                    cursor=cursor,
                    table='user',
                    columns_list=['user_id'],
                    where_clause=[{'email':email}]
                )
        if cursor.rowcount == 0 :
            print(f"❗ No user found with email address  : {email}")
            return None
        return int(user_record[0][0])
    except Exception as e :
        print(f'Internal Error Could not provide uid please try again later {str(e).strip()}')
        return None
                
def register(cursor:MySQLCursorAbstract,passphrase:str)->int:
    # creating Cursor
    try:
        for i in range(5):
                print(f"Attempt : {i}/5")
                print('registering user...')
                # getting params
                user_name = input('enter username : ')
                email = input('enter Email [b/w 8-15 chr and have [@ and .] without space]: ')
                if not prompt.validate_email(email):
                    print(f"❗Invalid Email : {email}")
                    continue
                # checking user existence
                if is_user_exists(cursor,email):
                    raise errors.AlreadyExistsError(f'user already registered')

                password = prompt.get_password_input(security_checks=True)
                if password is None:
                    print(f"❗Requirements Not Satisfied")
                    continue
                # password encryption
                hashed_password = security.hash_data(password)
                try:
                    choice = int(input("enter user role [1:admin,2:doctor,3:patient] : "))
                    role = options.UserRole(choice).name
                    # if role is admin
                    if role == 'admin' and not verify_admin_identity(passphrase):
                        print("❌ identity verification failed for role admin")
                        continue
                except (ValueError,KeyError):
                    print("❗Invalid role")
                    continue 
                try: 
                    age = int(input("enter age : "))
                except ValueError:
                    print(f"❗Invalid Age")
                    continue
                try:
                    dob = datetime.datetime.strptime(input('Enter your dob [dd-mm-yy]: '),"%d-%m-%Y")
                except ValueError:
                    print(f"❗Invalid DateOfBirth This Cannot Exists")
                    continue
                current_address = input('Enter Current Address : ')
                # inserting data
                records.insert_record(
                    cursor=cursor,
                    table='user',
                    column_order=('user_name','email','password','role','age','dob','current_address'),
                    values_list=[(user_name,email,hashed_password,role,age,dob,current_address)]
                )
                # when user is registered
                user_id  = know_your_user_id(cursor,email=email)
                print(f"USer Registered UID (please save this id you will be asked while login ): {user_id}")
                if user_id :
                    return user_id
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')

    except Exception as e:
        raise errors.DBError(f'Could Not register : {str(e).strip()}')

def login(cursor:MySQLCursorAbstract):
    try:
        # user login 
        for i in range(5):
            print('attempt',i,'/5')
            user_id = input('Enter User Id [if unknown leave blank to know your uid] : ').strip()
            if user_id and not user_id.isdigit():
                print('❗Invalid User id Enter a Number ')
                continue

            if not user_id:
                # trying to get user id 
                user_id = know_your_user_id(cursor)
                if user_id is None:
                    print("Login Failed")
                    return False
                else:
                    print(f'your user id is : {user_id}')
                    continue

            user_id = int(user_id)
            password = prompt.get_password_input(security_checks=False)
            if password is None:
                continue

            hashed_password  = security.hash_data(password)
            records.select_record(
                cursor=cursor,
                table='user',
                columns_list=['user_name'],
                where_clause=[{"user_id":user_id},{"password":hashed_password}]
            )
            if cursor.rowcount == 0:
                print(f'Invalid Password Please Retry ')
                continue
            return True
        else:
            print(f'too many invalid attempts please retry after sometime')
            return False
    except errors.UserNotFoundError as e :
        print(e)
        return False
    except Exception as e :
        raise errors.DBError(f'Internal Error Could Not Login : {str(e).strip()} ')
