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
    
def is_patient_appointment(cursor, patient_id: int, appointment_id: int) -> bool:
    """Check if appointment belongs to patient"""
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='appointment',
                    columns_list=['appointment_id'],
                    where_clause=[{'appointment_id':appointment_id},{'patient_id':patient_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check appointment: {str(e).strip()}')
def is_doctor_appointment(cursor, doctor_id: int, appointment_id: int) -> bool:
    """Check if appointment belongs to doctor"""
    try:
       
        records.select_record(
                    cursor=cursor,
                    table='appointment',
                    columns_list=['appointment_id'],
                    where_clause=[{'appointment_id':appointment_id},{'doctor_id':doctor_id}]
                )
        
        return cursor.rowcount > 0
    except errors.RecordError as e : 
        raise errors.DBError(f'cannot check appointment: {str(e).strip()}')
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
    
def search_doctor(cursor:MySQLCursorAbstract,by_spec_name='',by_spec_desc='')->None:
  
    for i in range(5):
        try:
            # creating where clause 
            if by_spec_desc:
                where_clause = [{"specialization.spec_desc":f"%{by_spec_desc}%"}]
            elif by_spec_name:
                where_clause = [{"specialization.spec_name":f"%{by_spec_name}%"}]
            else:
                print("how do you choose want to search ")
                print('1:by description of specialist')
                print('2:by name of specialization')
                choice = input('Enter your choice : ')
                if choice == '1' :
                    by_spec_desc = input('Enter the description of specialist: ')
                    where_clause = [{"specialization.spec_desc":f"%{by_spec_desc}%"}]
                elif choice == '2':
                    by_spec_name = input('Enter the name of specialization: ')
                    where_clause = [{"specialization.spec_name":f"%{by_spec_name}%"}]
                else:
                    print('Invalid choice')
                    continue
            
            # preparing query 
            join_clause = [
                'user ON doctor.user_id = user.user_id',
                'specialization ON doctor.spec_id = specialization.spec_id'
            ]
            columns_list = ['doctor.doctor_id','user.user_name','specialization.spec_name']
            # searching
            search_record = records.select_record(
                cursor=cursor,
                table='doctor',
                columns_list=columns_list,
                join_clause=join_clause,
                where_clause=where_clause,
                order_by_column='doctor.doctor_id',
                with_like=True
            )
            # printing searched record 
            if cursor.rowcount == 0:
                print('sorry no record found')
                break                
            else:
                for record in search_record:
                    print(record)
            return None
        except ValueError:
            print('Invalid choice')
            continue
        except Exception as e :
            raise errors.DBError(f'Could not search doctor: {str(e).strip()}')
    else:
        raise errors.MaxAttemptError(f'too many attempts please try again later')

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
    
def know_appointment_id(cursor:MySQLCursorAbstract,doctor_id:int,patient_id:int)->int:   
    try:
        appointment_record = records.select_record(
                    cursor=cursor,
                    table='appointment',
                    columns_list=['appointment_id'],
                    where_clause=[{"patient_id":patient_id},{"doctor_id":doctor_id}]
                )
        if cursor.rowcount == 0 :
            raise errors.RecordNotFoundError(f"❗ No patient found with the given patient_id and doctor_id combination: {patient_id} and {doctor_id}")
        return int(appointment_record[0][0])
    except Exception as e :
        raise errors.DBError(f'Internal Error Could not provide patient_id please try again later {str(e).strip()}')
   
def book_appointment(cursor:MySQLCursorAbstract,user_id:int):
    try:
        for i in range(5):
            print(f'Attempt {i}/3')
            if get_user_role(cursor,user_id) != 'patient':
                raise errors.InvalidArgumentError(f'Only Patient Can Book Appointment')
            
            # getting doctor id 
            doctor_id = input(f'Enter Doctor Id [leave to search one with specialization] : ').strip()
            if not doctor_id :
                search_doctor(cursor)
                continue
             # trying conversion
            try:
                doctor_id = int(doctor_id)
            except ValueError:
                print(f'❗doctor id must be a integer ')
                continue
            # checking doctor existence
            if not is_doctor_exists(cursor,doctor_id):
                print(f'❗doctor is not registered please retry ')
                continue
            # getting patient id 
            patient_id = know_patient_id(cursor,user_id)
            # getting schedule date
            try:
                    scheduled_at = datetime.strptime(input('Enter date and time  to schedule [dd-mm-yy hours:minutes]: '),"%d-%m-%Y %H:%M")
                    current_time  = datetime.now()
                    if not scheduled_at > current_time :
                        print(f'❗Please Select Future Date and time ')
                        continue
                    
            except ValueError:
                    print(f"❗Invalid scheduled date and time This Cannot Exists")
                    continue
            symptoms = input(f'what symptom(s) observed ?: ').strip()
            if not symptoms :
                print(f'❗please provide symptoms')
            medical_history_id = input(f'Enter medical history id [leave if have no medical history here]: ') or 0

           
            # preparing data 
            column_order = ('doctor_id','patient_id','scheduled_at','symptoms','medical_history_id')
            values_list = [(doctor_id,patient_id,scheduled_at,symptoms,medical_history_id)]
            # inserting data
            records.insert_record(
                cursor=cursor,
                table='appointment',
                column_order=column_order,
                values_list=values_list
            )
            # when user is registered
            appointment_id  = know_appointment_id(cursor,doctor_id,patient_id)
            print(f"✔️ Appointment scheduled appointment id is  (please save this id you will be asked later  ): {appointment_id}")
            return appointment_id
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Cannot Book Appointment: {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not Book Appointment : {str(e).strip()}')

def view_appointment(cursor:MySQLCursorAbstract,user_id:int)->list[tuple]:
    try:
        for i in range(5):
            print(f'Attempt {i}/3')
            try:
                role = get_user_role(cursor,user_id)
                if role not in  ['doctor','patient']:
                    raise errors.InvalidArgumentError(f'Only Patient and Doctors Can Check Appointment')
            except errors.UserNotFoundError as e :
                print(f'could not view appointment {e}')
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

            appointment_record = records.select_record(
                    cursor=cursor,
                    table='appointment',
                    columns_list=['*'],
                    where_clause=where_clause 
                ) # [('appointment_id','doctor_id','patient_id','scheduled_at','symptoms','medical_history_id')]
            
            if cursor.rowcount == 0:
                print('❗ No appointments found')
                continue
            
            msg = "View all appointments? (y/n) [n shows only future]: "
            if prompt.confirm(msg):
                print(f"\n📋 ALL APPOINTMENTS ({len(appointment_record)}):")
                for apt in appointment_record:
                    print(f"  ID: {apt[0]} | Doctor: {apt[1]} | Patient: {apt[2]} | Date: {apt[3]} | Symptoms: {apt[4]} | Status: {apt[6]}")
            else:
                print(f'\n📋 FUTURE APPOINTMENTS:')
                future_count = 0
                for apt in appointment_record:
                    scheduled_at = apt[3]
                    
                    # Handle datetime object
                    if isinstance(scheduled_at, str):
                        scheduled_at = datetime.strptime(scheduled_at, "%d-%m-%Y %H:%M")
                    
                    current_time = datetime.now()
                    if scheduled_at > current_time:
                        print(f"  ID: {apt[0]} | Doctor: {apt[1]} | Patient: {apt[2]} | Date: {apt[3]} | Symptoms: {apt[4]} | Status: {apt[6]}")
                        future_count += 1
                
                if future_count == 0:
                    print(' No future appointments')
            
            return appointment_record
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Cannot View Appointment: {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could Not View Appointment : {str(e).strip()}')

def cancel_appointment(cursor: MySQLCursorAbstract, user_id: int) -> None:
    """
    Cancel an appointment
    Doctor: can cancel any appointment
    Patient: can cancel only their own appointments
    """
    try:
        for i in range(5):
            try:
                role = get_user_role(cursor,user_id)
                if role not in  ['doctor','patient']:
                    raise errors.InvalidArgumentError(f'Only Patient and Doctors Can Cancel Appointment')
            except errors.UserNotFoundError as e :
                print(f'could not Cancel appointment {e}')
                continue

            appointment_id = int(input(f'Enter appointment id  to cancel appointment: '))
            if not is_appointment_exists(cursor,appointment_id):
                    print(f'❗appointment does not exists')
                    continue
            
            if role == 'patient':
                patient_id = int(input(f'Enter patient id : '))
                if not is_patient_exists(cursor,patient_id):
                        print(f'❗patient does not exists')
                        continue
                
                if not is_patient_appointment(cursor,patient_id,appointment_id):
                    print(f'Cannot Cancel appointment This Record Does Not Belongs to Patient  ID  : {patient_id} ')
                    continue
            
                
            else:
                doctor_id = int(input(f'Enter Doctor id : '))
                if not is_doctor_exists(cursor,doctor_id):
                        print(f'❗doctor does not exists')
                        continue
                
                if not is_doctor_appointment(cursor,doctor_id,appointment_id):
                    print(f'Cannot Cancel appointment This Record Does Not Belongs to Doctor ID : {doctor_id} ')
                    continue
            
            
            # canceling appointment
            records.update_record(
                cursor=cursor,
                table='appointment',
                set_clause={"status":'canceled'},
                where_clause=[{"appointment_id":appointment_id}]
            )
            print(f' ✔️ Appointment Canceled')
            return None
        else:
            raise errors.MaxAttemptError(f'too many Invalid attempts please try again later')
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'⚠️ Cannot Cancel Appointment: {str(e).split()}')
    except Exception as e:
        raise errors.DBError(f'Could not cancel appointment: {str(e).strip()}')

def update_appointment_status(cursor: MySQLCursorAbstract, user_id: int) -> None:
    """
    ONLY doctors can update appointment status
    Doctor provides: appointment_id, new_status
    Status can be: scheduled, ongoing, ended, canceled
    """
    try:
        for i in range(5):
            try:
                # 1. Verify user is doctor
                role = get_user_role(cursor, user_id)
                if role != 'doctor':
                    raise errors.InvalidArgumentError(f'Only Doctors Can Update Appointment Status')
            except errors.UserNotFoundError as e:
                print(f'❗ {e}')
                continue
            
            # 2. Get doctor_id
            doctor_id = int(input(f'Enter doctor id: '))
            if not is_doctor_exists(cursor, doctor_id):
                print(f'❗Doctor does not exist')
                continue
            
            # 3. Get appointment_id
            appointment_id = int(input(f'Enter appointment id to update: '))
            if not is_appointment_exists(cursor, appointment_id):
                print(f'❗Appointment does not exist')
                continue
            
            # 4. Verify it's doctor's appointment
            if not is_doctor_appointment(cursor, doctor_id, appointment_id):
                print(f'❗ This appointment does not belong to doctor ID: {doctor_id}')
                continue
            
            # 5. Get current status
            current_apt = records.select_record(
                cursor=cursor,
                table='appointment',
                columns_list=['status'],
                where_clause=[{'appointment_id': appointment_id}]
            )
            current_status = current_apt[0][0]
            print(f'Current status: {current_status}')
            
            # 6. Get new status input
            print('Available statuses: scheduled, ongoing, ended, canceled')
            new_status = input(f'Enter new status: ').strip().lower()
            
            if new_status not in ['scheduled', 'ongoing', 'ended', 'canceled']:
                print(f'❗Invalid status')
                continue
            
            # 7. Update database
            records.update_record(
                cursor=cursor,
                table='appointment',
                set_clause={'status': new_status},
                where_clause=[{'appointment_id': appointment_id}]
            )
            
            print(f' ✔️ Appointment status updated: {current_status} → {new_status}')
            return None
            
        else:
            raise errors.MaxAttemptError(f'Too many attempts, try again later')
            
    except errors.RecordNotFoundError as e:
        raise errors.DBError(f'Cannot update appointment: {str(e)}')
    except Exception as e:
        raise errors.DBError(f'Could not update appointment status: {str(e).strip()}')


        


