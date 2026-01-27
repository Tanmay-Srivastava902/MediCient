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
def get_user_role(cursor:MySQLCursorAbstract,user_id:int)->bool:
    '''verifies wether the user role is as intended or not'''
    try:
        user_record = records.select_record(
            cursor=cursor,
            table='user',
            columns_list=['role'],
            where_clause=[{'user_id':user_id}]
        )  
        return user_record[0][0]
    except Exception as e :
        raise errors.DBError(f'Could not get user role: {str(e).strip()}')
    
def verify_user_role(cursor:MySQLCursorAbstract,role:str,user_id:int)->bool:
    '''verifies wether the user role is as intended or not'''
    try:
        user_record = records.select_record(
            cursor=cursor,
            table='user',
            columns_list=['role'],
            where_clause=[{'user_id':user_id}]
        )  
        return role == user_record[0][0]
    except Exception as e :
        raise errors.DBError(f'Could not verify user role: {str(e).strip()}')
def know_your_user_id(cursor:MySQLCursorAbstract,email:str='')->int:
    '''gets **int user id** for given email if any or **none** if not found or invalid user or max attempts tried'''
    if not email:
        for i in range(3): 
            email = input(f'Enter User Email Address to know your uid [attempt {i}/3]:  ')
            if not prompt.validate_email(email):
                print(f"❗Invalid Email : {email}")
                continue
            break
        else:
            raise errors.MaxAttemptError(f'too many failed attempts please try again later')
    try:
        user_record = records.select_record(
                    cursor=cursor,
                    table='user',
                    columns_list=['user_id'],
                    where_clause=[{'email':email}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No user found with email address  : {email}")
        return int(user_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Internal Error Could not provide uid please try again later {str(e).strip()}')
def know_spec_id(cursor:MySQLCursorAbstract,spec_name:str='')->int:
    if not spec_name:
        spec_name = input(f'Enter specialization name to know spec_id :  ')     
    try:
        user_record = records.select_record(
                    cursor=cursor,
                    table='specialization',
                    columns_list=['spec_id'],
                    where_clause=[{"spec_name":spec_name}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No specialization found with the given name : {spec_name}")
        return int(user_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Internal Error Could not provide spec_id please try again later {str(e).strip()}')

def know_disease_id(cursor:MySQLCursorAbstract,disease_name:str='')->int:
    if not disease_name:
        disease_name = input(f'Enter disease name to know disease_id :  ')     
    try:
        user_record = records.select_record(
                    cursor=cursor,
                    table='disease',
                    columns_list=['disease_id'],
                    where_clause=[{"disease_name":disease_name}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No specialization found with the given name : {disease_name}")
        return int(user_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Could not provide disease_id please try again later {str(e).strip()}')
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
                return user_id
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ user registered : {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not register : {str(e).strip()}')

def login(cursor:MySQLCursorAbstract)->int:
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
            return user_id
        else:
            raise errors.MaxAttemptError(f'too many invalid attempts please retry after sometime')
    except Exception as e :
        raise errors.DBError(f'Internal Error Could Not Login : {str(e).strip()} ')

def add_specialization(cursor:MySQLCursorAbstract,user_id:int)->int:
    
    print(f'⚙️ Verifying Your Identity Please Wait...')
    is_admin = verify_user_role(cursor,role='admin',user_id=user_id)
    is_doctor = verify_user_role(cursor,role='doctor',user_id=user_id)
    if not (is_admin or is_doctor):
        raise errors.AuthError(f'❌ Identity verification failed : only admins and doctors can add specialization')
    try:
        print('✔️ identity verified')
        print(f'Adding specialization')
        spec_name = input(f'Enter specialization name : ')
        spec_desc = input(f'provide a description (what this specialization is for ?) : ')
        treats_diseases  = input(f"what diseases it treats? (use comma to provide next name ) eg-diseaseA,diseaseB : ")
        # verifying status if admin directly adds it else default 'unverified'
        status = 'verified' if is_admin else 'unverified'
        column_order = ('spec_name','spec_desc','treats_diseases','status')
        values_list =  [(spec_name,spec_desc,treats_diseases,status)]
        # adding specialization (with status )
        records.insert_record(
            cursor=cursor,
            table='specialization',
            column_order=column_order,
            values_list=values_list
        )
        # getting spec id 
        spec_id = know_spec_id(cursor,spec_name)
        print(f"Specialization added spec_id (please save this id you will be asked while selection ): {spec_id}")
        return spec_id
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ specialization added : {str(e).split()}')
    except Exception as e :
        raise errors.DBError(f'Could not add specialization Internal Error : {str(e).strip()}')

#TODO use doctor only disease addition system (not now for later)
def add_disease(cursor:MySQLCursorAbstract,user_id:int)->int:
    try:
        print(f'⚙️  Verifying Your Identity Please Wait...')
        is_admin = verify_user_role(cursor,role='admin',user_id=user_id)
        is_doctor = verify_user_role(cursor,role='doctor',user_id=user_id)
        if not (is_admin or is_doctor):
            raise errors.AuthError(f'❌ Identity verification failed : only admins and doctors can add disease')
        print('✔️  identity verified')
        print(f'Adding Disease')
        print(f'use comma(,) to separate b/w two entries where the list is asked to provide (eg- for symptoms : input -> symptom1,symptom2 etc)')
        disease_name = input(f'Enter disease name : ')
        symptoms = input(f'what symptom(s) this disease shows ?: ')
        disease_desc = input(f"provide a description for this disease? (extra medical info about it): ")
        medicines_preferred = input(f'provide a list of preferred medicine(s) (for initial general treatment): ')
        precautions_needed = input(f'provide the list of precaution(s) ? (for initial prevention) : ')
        column_order = ('disease_name','symptoms','disease_desc','medicines_preferred','precautions_needed')
        values_list =  [(disease_name,symptoms,disease_desc,medicines_preferred,precautions_needed)]
        # adding specialization (with status )
        records.insert_record(
            cursor=cursor,
            table='disease',
            column_order=column_order,
            values_list=values_list
        )
        # getting disease id 
        disease_id = know_disease_id(cursor,disease_name)
        print(f"disease added disease_id (please save this id you will be asked while selection ): {disease_id}")
        return disease_id
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ disease added : {str(e).split()}')
    except Exception as e :
        raise errors.DBError(f'Could not add disease Internal Error : {str(e).strip()}')

        
    

    