# from service_managers import mysql_services
# from core_app import users
# import errors
# conn = mysql_services.create_conn(password='SecurePass@1201',db='medicient')
# cursor = conn.cursor()
# try:
#     admin_id = 3
#     # creating non admin user
#     print('user trying to register specialization')
#     demo_passphrase = "tsri@hello.passhrase"
#     # user will be patient first
#     user_id = users.register(cursor,demo_passphrase)
#     if users.login(cursor):
#         print("user logged in")
#         if users.add_specialization(cursor,user_id=user_id) is None:
#             print(f'Failed to add specialization')
#         if users.add_disease(cursor,user_id=user_id) is None:
#             print(f'failed to add disease')
#     print(f'using admin to add specialization')
#     if users.add_specialization(cursor,user_id=admin_id) is None:
#             print(f'Failed to add specialization')
#     if users.add_disease(cursor,user_id=user_id) is None:
#             print(f'failed to add disease')    

#     conn.commit()
#     conn.close()
# except errors.DBError as e :
#     print(e)
#     conn.close()
# except errors.AuthError as e :
#     print(e)
#     conn.close()


# main.py - NO SETUP, NO CONFIG LOADING YET
# Just hardcode for NOW



from service_managers import mysql_services
from core_app import users, doctors, patients
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
            print("5. Exit")
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
                print("✅ Registration complete!")
                
            elif choice == '2':
                # LOGIN
                user_id = users.login(cursor)
                if user_id:
                    print(f"✅ Logged in! User ID: {user_id}")
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
                    print(f"✅ Specialization Added ! Spec ID: {spec_id}")
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
                    print(f"✅ disease Added ! Spec ID: {disease_id}")
                else:
                    print(f' ❌ Failed to add disease')  
            elif choice == '5':
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