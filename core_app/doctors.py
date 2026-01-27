from mysql.connector.abstracts import MySQLCursorAbstract
from data_operators import records
from utils import prompt
import errors
def get_user_role(cursor:MySQLCursorAbstract,user_id:int)->str:
    '''gives the role of the doctor'''
    try:
        user_record = records.select_record(
            cursor=cursor,
            table='user',
            columns_list=['role'],
            where_clause=[{'user_id':user_id}]
        )  
        if cursor.rowcount == 0:
            raise errors.UserNotFoundError(f'User Is Not Registered')
        return user_record[0][0]
    except Exception as e :
        raise errors.DBError(f'Could not get user role: {str(e).strip()}')
def validate_doctor_license(license_number:str)->bool:
    blocked = list('!@#$%^&*()-_=+[]{};:\'\",.<>/?|\\`~ ' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower())

    # manual check 
    if not  license_number.startswith('DOC'):
        return False
    
    # print(blocked,allowed)
    return prompt.validate_input(
        ipt=license_number,
        min_length=8,
        max_length=15,
        blocked_chars=blocked
    )
def show_available_specifications(cursor:MySQLCursorAbstract)->None:
    for i in range(3):
        print(f'Attempt {i}/3')
        spec_name = input(f'Enter specialization name to search (leave blank to see full list):  ').strip()     
        columns_list = ['spec_id','spec_name','status']
        where_clause = [{"spec_name":f"%{spec_name}%"},{"spec_name":spec_name}] if spec_name else []
        try:
            spec_records = records.select_record(
                cursor=cursor,
                table='specialization',
                columns_list=columns_list,
                where_clause=where_clause,
                with_or=True
            )
            available_specs = [record for record in spec_records if record[-1] == "verified" ]
            if len(available_specs) == 0:
                print(f'No specifications are available to choose please retry')
                continue            
            # printing records 
            for specs in available_specs:
                print(specs)
            else:
                return None
        except Exception as e :
            raise errors.DBError(f'Could not list specifications : {str(e).strip()}')
    else:
        raise errors.MaxAttemptError(f'too many attempts tried please try again later')
    
def is_specification_valid(cursor:MySQLCursorAbstract,spec_id:int)->bool:
    try:
        records.select_record(
                        cursor=cursor,
                        table='specialization',
                        columns_list=['spec_name'],
                        where_clause=[{"spec_id":spec_id},{"status":"verified"}]
                    )
        if cursor.rowcount == 0 :
            return False
        return True
    except Exception as e :
        raise errors.DBError(f'could not check specification')
def know_doctor_id(cursor:MySQLCursorAbstract,license_number:str='')->int:   
    try:
        doctor_record = records.select_record(
                    cursor=cursor,
                    table='doctor',
                    columns_list=['doctor_id'],
                    where_clause=[{"license_number":license_number}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No doctor found with the given license_number : {license_number}")
        return int(doctor_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Internal Error Could not provide doctor_id please try again later {str(e).strip()}')
   
def complete_doctor_profile(cursor:MySQLCursorAbstract,user_id:int)->int:
    try:
        # verifying user role before proceeding 
        if get_user_role(cursor,user_id) != 'doctor':
            raise errors.InvalidArgumentError(f'❗ user is not registered as doctor ')
        
        print('Complete Doctor Profile')
        for i in range(5):
                print(f"Attempt : {i}/5")
                # getting params
                license_number = input('Enter Your License Number : ').strip()
                if not validate_doctor_license(license_number):
                    continue
                spec_id = input('Enter Specialization id [leave blank to find] : ').strip()
                # finding spec_id 
                if not spec_id:
                    show_available_specifications(cursor)
                    continue
                spec_id = int(spec_id)
                # validating spec_id 
                if not is_specification_valid(cursor,spec_id):
                    print(f'❗Invalid Specification Id No specification found with spec_id :{spec_id}')
                    continue
                # extra fields info
                skills = input(f'what is your expert skills (please enter comma (,) separated values)? : ').strip()
                doctor_desc = input(f'Enter your description (for public showcase) ? : ').strip()
                spec_institute = input(f'Enter name(s) of your institute (comma(,) separated): ').strip()
                work_location = input(f'Enter Your work address (eg-location of clinic ): ').strip()
                
                # preparing data 
                column_order = ('user_id','license_number','spec_id','skills','doctor_desc','spec_institute','work_location')
                values_list = [(user_id,license_number,spec_id,skills,doctor_desc,spec_institute,work_location)]
                # inserting data
                records.insert_record(
                    cursor=cursor,
                    table='doctor',
                    column_order=column_order,
                    values_list=values_list
                )
                # when user is registered
                doctor_id  = know_doctor_id(cursor,license_number=license_number)
                print(f"Profile Completed Doctor Id is  (please save this id you will be asked later ): {doctor_id}")
                return doctor_id
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Profile Incomplete : {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not Complete Profile : {str(e).strip()}')
