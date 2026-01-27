from mysql.connector.abstracts import MySQLCursorAbstract
from data_operators import records
from utils import prompt
import errors
def get_user_role(cursor:MySQLCursorAbstract,user_id:int)->str:
    '''gives the role of the patient'''
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
def know_patient_id(cursor:MySQLCursorAbstract,user_id:int)->int:   
    try:
        patient_record = records.select_record(
                    cursor=cursor,
                    table='patient',
                    columns_list=['patient_id'],
                    where_clause=[{"user_id":user_id}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No patient found with the given user_id : {user_id}")
        return int(patient_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Internal Error Could not provide patient_id please try again later {str(e).strip()}')
   
def complete_patient_profile(cursor:MySQLCursorAbstract,user_id:int)->int:
    try:
        # verifying user role before proceeding 
        if get_user_role(cursor,user_id) != 'patient':
            raise errors.InvalidArgumentError(f'❗ user is not registered as patient ')
        
        print('Complete patient Profile')
        for i in range(5):
                print(f"Attempt : {i}/5")
                try:
                    weight  =  int(input('Enter your Weight (in kg) : ').strip())
                    if not prompt.validate_integer(weight,10,200):
                        print(f'❗Invalid weight : weight must be b/w 10kg to 200kg')
                        continue
                    
                    height  =  int(input('Enter your height (in cm) : ').strip())
                    if not prompt.validate_integer(height,50,250):
                        print(f'❗Invalid height : height must be b/w 50cm to 250cm')
                        continue
                
                    
                    # extra fields info
                    lifestyle = input(f'how is the actual lifestyle of patient ? : ').strip() 
                    if not lifestyle:
                        print(f'Please Provide lifestyle info for better judgement of patient health') 
                        continue
                    current_location = input(f'Enter Your Current address (for emergency usage): ').strip() or "Not Provided"
                    note = input(f'Enter any extra info about patient as notes (optional) : ').strip() or "Not Provided"
                    # preparing data 
                    column_order = ('user_id','height','weight','lifestyle','current_location','note')
                    values_list = [(user_id,height,weight,lifestyle,current_location,note)]
                    # inserting data
                    records.insert_record(
                        cursor=cursor,
                        table='patient',
                        column_order=column_order,
                        values_list=values_list
                    )
                    # when user is registered
                    patient_id  = know_patient_id(cursor,user_id=user_id)
                    print(f"Profile Completed patient Id is  (please save this id you will be asked later ): {patient_id}")
                    return patient_id
                except ValueError:
                    print(f'❗Invalid Input Only numeric values are allowed')
                    continue
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Profile Incomplete : {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not Complete Profile : {str(e).strip()}')
