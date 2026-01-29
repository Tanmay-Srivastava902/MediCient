from service_managers import mysql_services
from core_app import users, doctors, patients , appointments , medical_history
import errors

# Hardcoded for testing (FIX LATER)
PASSPHRASE = "tsri@hello.passhrase"
DB_PASSWORD = "SecurePass@1201"
DB_NAME = "medicient"

def main():
    try:
        conn = mysql_services.create_conn(password=DB_PASSWORD, db=DB_NAME)
        cursor = conn.cursor()
        
        while True:
            print("\n=== MEDICIENT ===")
            print("1. Register")
            print("2. Login")
            print("3. Add Specialization")
            print("4. Add Disease")
            print("5. Book Appointment")
            print("6. View Appointment")
            print("7. Cancel Appointment")
            print("8. Update Appointment Status")
            print("9. Add Medical History")
            print("10. View Medical History")
            print("11. Update Medical History Status")
            print("12. Exit")
            choice = input("Choose: ").strip()
            
            if choice == '1':
                # REGISTER + AUTO PROFILE COMPLETE
                user_id = users.register(cursor, PASSPHRASE)
                role = users.get_user_role(cursor, user_id)
                
                if role == 'doctor':
                    doctors.complete_doctor_profile(cursor, user_id)
                elif role == 'patient':
                    patients.complete_patient_profile(cursor, user_id)
                
                conn.commit()
                print("✔️ Registration complete!")
                
            elif choice == '2':
                # LOGIN
                user_id = users.login(cursor)
                if user_id:
                    print(f"✔️ Logged in! User ID: {user_id}")
                    # Can add more menu here later
                else:
                    print("❌ Login failed")
            elif choice == '3':
                print(f'adding specialization')
                try:
                    user_id = int(input('enter admin or doctor user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                spec_id =  users.add_specialization(cursor,user_id=user_id)
                if spec_id :
                    conn.commit()
                    print(f"✔️ Specialization Added ! Spec ID: {spec_id}")
                else:
                    print(f' ❌ Failed to add specialization')  
            elif choice == '4':
                print(f'adding diseases')
                try:
                    user_id = int(input('enter admin or doctor user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                disease_id =  users.add_disease(cursor,user_id=user_id)
                if disease_id :
                    conn.commit()
                    print(f"✔️ disease Added ! Spec ID: {disease_id}")
                else:
                    print(f' ❌ Failed to add disease')  
            elif choice == '5':
                print(f'booking appointment')
                try:
                    user_id = int(input('Enter patient user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                appointment_id =  appointments.book_appointment(cursor,user_id=user_id)
                if appointment_id :
                    conn.commit()
                    print(f"✔️ appointment Booked ! Appointment ID: {appointment_id}")
                else:
                    print(f' ❌ Failed to Book Appointment')  
            elif choice == '6':
                print(f'Viewing appointment')
                try:
                    user_id = int(input('Enter user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                record =  appointments.view_appointment(cursor,user_id=user_id)
                if record :
                    conn.commit()
                    print(f"✔️ appointment Viewed")
                else:
                    print(f' ❌ Failed to View Appointment')  
            elif choice == '7':
                print(f'Cancelling appointment')
                try:
                    user_id = int(input('Enter user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                record =  appointments.cancel_appointment(cursor,user_id=user_id)
                if record is None:
                    conn.commit()
                else:
                    print(f' ❌ Failed to Cancel Appointment')  
            elif choice == '8':
                print(f'Updating appointment Status')
                try:
                    user_id = int(input('Enter user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                record =  appointments.update_appointment_status(cursor,user_id=user_id)
                if record is None:
                    conn.commit()
                else:
                    print(f' ❌ Failed to Update Appointment')  
            elif choice == '9':
                print(f'adding medical history')
                try:
                    user_id = int(input('Enter  user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                appointment_id =  medical_history.add_medical_history(cursor,user_id=user_id)
                if appointment_id :
                    conn.commit()
                else:
                    print(f' ❌ Failed to Add Medical History') 
            elif choice == '11':
                print(f'updating medical history status')
                try:
                    user_id = int(input('Enter user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                appointment_id =  medical_history.update_medical_history_status(cursor,user_id=user_id)
                if appointment_id is None :
                    conn.commit()
                else:
                    print(f' ❌ Failed to UPdate medical history status')  
            elif choice == '10':
                print(f'Viewing medical history')
                try:
                    user_id = int(input('Enter user id : '))
                except ValueError:
                    print(f'id must be in numbers ')
                    continue
                record =  medical_history.view_medical_history(cursor,user_id=user_id)
                if record :
                    conn.commit()
                    print(f"✔️ medical history Viewed")
                else:
                    print(f' ❌ Failed to View medical history')  
            elif choice == '12':
                print("Goodbye!")
                conn.close()
                break

                
    except errors.DBError as e:
        print(f"❌ {e}")
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()

if __name__ == "__main__":
    main()