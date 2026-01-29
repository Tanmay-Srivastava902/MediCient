from mysql.connector.abstracts import MySQLCursorAbstract
from data_operators import records
from utils import prompt
import errors
from datetime import datetime
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
def is_doctor_exists(cursor:MySQLCursorAbstract,doctor_id:int)->bool:
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='doctor',
                    columns_list=['doctor_id'],
                    where_clause=[{'doctor_id':doctor_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check doctor existence: {str(e).strip()}')
def is_patient_exists(cursor:MySQLCursorAbstract,patient_id:int)->bool:
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='patient',
                    columns_list=['patient_id'],
                    where_clause=[{'patient_id':patient_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check patient existence: {str(e).strip()}')
    
# def is_patient_appointment(cursor, patient_id: int, appointment_id: int) -> bool:
#     """Check if appointment belongs to patient"""
#     try:
       
#         records.select_record(
#                     cursor=cursor,
#                     table='appointment',
#                     columns_list=['appointment_id'],
#                     where_clause=[{'appointment_id':appointment_id},{'patient_id':patient_id}]
#                 )
        
#         return cursor.rowcount > 0
#     except errors.RecordError as e : 
#         raise errors.DBError(f'cannot check appointment: {str(e).strip()}')
def is_doctor_medical_history(cursor, doctor_id: int, medical_history_id: int) -> bool:
    """Check if medical_history belongs to doctor"""
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='medical_history',
                    columns_list=['record_id'],
                    where_clause=[{'record_id':medical_history_id},{'doctor_id':doctor_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check medical history: {str(e).strip()}')
 
def is_disease_exists(cursor:MySQLCursorAbstract,disease_id:int)->bool:
    try:
        records.select_record(
                    cursor=cursor,
                    table='disease',
                    columns_list=['disease_id'],
                    where_clause=[{"disease_id":disease_id}]
                )
        return  cursor.rowcount > 0 
    except Exception as e :
        raise errors.DBError(f'Could not provide disease_id please try again later {str(e).strip()}')   
def is_appointment_exists(cursor, appointment_id: int) -> bool:
    """Check if appointment exists"""
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='appointment',
                    columns_list=['appointment_id'],
                    where_clause=[{'appointment_id':appointment_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check appointment: {str(e).strip()}')

def is_medical_history_exists(cursor, medical_history_id: int) -> bool:
    """Check if medical_history exists"""
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='medical_history',
                    columns_list=['record_id'],
                    where_clause=[{'record_id':medical_history_id}]
                )
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check medical history: {str(e).strip()}')


def add_medical_history(cursor: MySQLCursorAbstract, user_id: int) -> int:
    """Doctor records medical history after appointment"""
    for i in range(5):
        try:
            # Verify doctor
            if get_user_role(cursor, user_id) != 'doctor':
                raise errors.InvalidArgumentError('Only doctors can add medical history')
            
            doctor_id = int(input('Enter doctor id: '))
            if not is_doctor_exists(cursor,doctor_id):
                    print(f'❗doctor is not registered please retry ')
                    continue
            patient_id = int(input('Enter patient id: '))
            if not is_patient_exists(cursor,patient_id):
                    print(f'❗patient is not registered please retry ')
                    continue
            disease_id = int(input('Enter disease id: '))
            if not is_disease_exists(cursor,disease_id):
                    print(f'❗disease is not exists in our database please retry ')
                    continue
            appointment_id = int(input('Enter appointment id: '))
            if not is_appointment_exists(cursor,disease_id):
                    print(f'! appointment is not exists in our database please retry ')
                    continue
            symptoms = input('Symptoms observed: ')
            treatment = input('Treatment given: ')
            medicines = input('Medicines prescribed: ')
            prevention = input('Prevention advice: ')
            
            # Insert
            records.insert_record(
                cursor=cursor,
                table='medical_history',
                column_order=('doctor_id', 'patient_id', 'disease_id', 'appointment_id', 
                            'symptoms', 'treatment', 'medicines', 'prevention', 'status'),
                values_list=[(doctor_id, patient_id, disease_id, appointment_id, 
                            symptoms, treatment, medicines, prevention, 'active')]
            )
            
            # Get record_id
            record = records.select_record(
                cursor=cursor,
                table='medical_history',
                columns_list=['record_id'],
                where_clause=[{'appointment_id': appointment_id}]
            )
            
            record_id = int(record[0][0])
            print(f'✔️ Medical history added! Record ID: {record_id}')
            return record_id
        except ValueError:
            print("id's must be integer ")
            continue
        except Exception as e:
            raise errors.DBError(f'Could not add medical history: {str(e).strip()}')
    else:
       raise errors.MaxAttemptError(f'too many attempts please try again later')
    
def view_medical_history(cursor:MySQLCursorAbstract,user_id:int)->list[tuple]:
    try:
        for i in range(5):
            print(f'Attempt {i}/3')
            try:
                role = get_user_role(cursor,user_id)
                if role not in  ['doctor','patient']:
                    raise errors.InvalidArgumentError(f'Only Patient and Doctors Can Check medical_history')
            except errors.UserNotFoundError as e :
                print(f'could not view medical_history {e}')
                continue
            
            # getting doctor or patient id 
            if role == 'doctor':
                doctor_id = int(input(f'Enter doctor id : '))
                if not is_doctor_exists(cursor,doctor_id):
                    print(f'❗doctor does not exists')
                    continue
                where_clause=[{'doctor_id':doctor_id}]
               
            else : 
                patient_id = int(input(f'Enter patient id : '))
                if not is_patient_exists(cursor,patient_id):
                    print(f'❗patient does not exists')
                    continue
                where_clause=[{'patient_id':patient_id}]

            medical_history_record = records.select_record(
                    cursor=cursor,
                    table='medical_history',
                    columns_list=['*'],
                    where_clause=where_clause 
                ) # [('doctor_id', 'patient_id', 'disease_id', 'appointment_id', 'symptoms', 'treatment', 'medicines', 'prevention', 'status')]
            
            if cursor.rowcount == 0:
                print('❗ No medical_history found')
                continue
        
            print(f"\n📋 ALL medical_history ({len(medical_history_record)}):")
            for medical_history in medical_history_record:
                print(f"  ID: {medical_history[0]} | Doctor: {medical_history[1]} | Patient: {medical_history[2]} | Disease: {medical_history[3]} | Symptoms: {medical_history[4]} | Treatment: {medical_history[5]} | Medicines: {medical_history[6]} | Prevention: {medical_history[7]} | Diagnosed At: {medical_history[8]} | Status: {medical_history[9]} | Note: {medical_history[10]}")
            
            return medical_history_record
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Cannot View medical_history: {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not View medical_history : {str(e).strip()}')

def update_medical_history_status(cursor: MySQLCursorAbstract, user_id: int) -> None:
    """
    ONLY doctors can update medical_history status
    Doctor provides: medical_history_id, new_status
    Status can be: active, recovered
    """
    try:
        for i in range(5):
            try:
                # 1. Verify user is doctor
                role = get_user_role(cursor, user_id)
                if role != 'doctor':
                    raise errors.InvalidArgumentError(f'Only Doctors Can Update medical_history Status')
            except errors.UserNotFoundError as e:
                print(f'❗ {e}')
                continue
            
            # 2. Get doctor_id
            doctor_id = int(input(f'Enter doctor id: '))
            if not is_doctor_exists(cursor, doctor_id):
                print(f'❗Doctor does not exist')
                continue
            
            # 3. Get medical_history_id
            medical_history_id = int(input(f'Enter medical_history record id to update: '))
            if not is_medical_history_exists(cursor, medical_history_id):
                print(f'❗medical_history does not exist')
                continue
            
            # 4. Verify it's doctor's medical_history
            if not is_doctor_medical_history(cursor, doctor_id, medical_history_id):
                print(f'❗ This medical_history does not belong to doctor ID: {doctor_id}')
                continue
            
            # 5. Get current status
            current_apt = records.select_record(
                cursor=cursor,
                table='medical_history',
                columns_list=['status'],
                where_clause=[{'record_id': medical_history_id}]
            )
            current_status = current_apt[0][0]
            print(f'Current status: {current_status}')
            
            # 6. Get new status input
            print('Available statuses: active recovered')
            new_status = input(f'Enter new status: ').strip().lower()
            
            if new_status not in ['active', 'recovered']:
                print(f'❗Invalid status')
                continue
            
            # 7. Update database
            records.update_record(
                cursor=cursor,
                table='medical_history',
                set_clause={'status': new_status},
                where_clause=[{'medical_history_id': medical_history_id}]
            )
            
            print(f' ✔️ medical_history status updated: {current_status} → {new_status}')
            return None
            
        else:
            raise errors.MaxAttemptError(f'Too many attempts, try again later')
            
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'Cannot update medical_history: {str(e)}')
    except Exception as e:
        raise errors.DBError(f'Could not update medical_history status: {str(e).strip()}')


        