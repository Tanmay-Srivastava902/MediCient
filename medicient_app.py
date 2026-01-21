#!/usr/bin/env python3
"""
MEDICIENT - Healthcare Management System
Simple CLI Interface for Practicals Demo

This is the USER-FACING part that uses your backend!
"""

import sys
import os

# Your backend (the "useless" code you think you wasted time on)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from results import Result
from utils import get_password_input, confirm
import services.mysql_service as mysql


# ============================================================================
# SIMPLE MENU SYSTEM
# ============================================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_menu(options):
    """Print menu options"""
    for key, value in options.items():
        print(f"  [{key}] {value}")
    print()


# ============================================================================
# PATIENT MANAGEMENT
# ============================================================================

def register_patient(conn):
    """Register a new patient"""
    clear_screen()
    print_header("📋 REGISTER NEW PATIENT")
    
    print("Enter patient details:\n")
    
    # Get user details
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = get_password_input("Password: ", security_checks=True)
    
    if not password:
        print("\n❌ Password requirements not met!")
        input("Press Enter to continue...")
        return
    
    age = input("Age: ").strip()
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    address = input("Address: ").strip()
    height = input("Height (cm): ").strip()
    weight = input("Weight (kg): ").strip()
    
    # Create user first
    query = """
        INSERT INTO user (user_name, email, password, role, age, dob, current_address, status)
        VALUES (%s, %s, %s, 'patient', %s, %s, %s, 'active')
    """
    params = (name, email, password, age, dob, address)
    
    try:
        result = mysql.mysql_executor(conn, query, params)
        
        # Get the user_id
        user_id_query = "SELECT LAST_INSERT_ID()"
        user_id_result = mysql.mysql_executor(conn, user_id_query)
        user_id = user_id_result[0][0]
        
        # Create patient record
        patient_query = """
            INSERT INTO patient (user_id, height, weight, patient_desc)
            VALUES (%s, %s, %s, 'New patient')
        """
        patient_params = (user_id, height, weight)
        mysql.mysql_executor(conn, patient_query, patient_params)
        
        print(f"\n✅ Patient registered successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Name: {name}")
        
    except Exception as e:
        print(f"\n❌ Registration failed: {str(e)}")
    
    input("\nPress Enter to continue...")


def view_patients(conn):
    """View all registered patients"""
    clear_screen()
    print_header("👥 ALL PATIENTS")
    
    query = """
        SELECT u.user_id, u.user_name, u.email, u.age, p.height, p.weight, u.status
        FROM user u
        JOIN patient p ON u.user_id = p.user_id
        WHERE u.role = 'patient'
    """
    
    try:
        patients = mysql.mysql_executor(conn, query)
        
        if not patients:
            print("No patients registered yet.\n")
        else:
            print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Age':<5} {'Height':<8} {'Weight':<8} {'Status':<10}")
            print("-" * 90)
            
            for patient in patients:
                print(f"{patient[0]:<5} {patient[1]:<20} {patient[2]:<25} {patient[3]:<5} {patient[4]:<8} {patient[5]:<8} {patient[6]:<10}")
            
            print(f"\nTotal patients: {len(patients)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")


# ============================================================================
# DOCTOR MANAGEMENT
# ============================================================================

def register_doctor(conn):
    """Register a new doctor"""
    clear_screen()
    print_header("🏥 REGISTER NEW DOCTOR")
    
    print("Enter doctor details:\n")
    
    # Get user details
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = get_password_input("Password: ", security_checks=True)
    
    if not password:
        print("\n❌ Password requirements not met!")
        input("Press Enter to continue...")
        return
    
    age = input("Age: ").strip()
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    address = input("Address: ").strip()
    license = input("License Number: ").strip()
    specialization = input("Specialization ID: ").strip()
    institute = input("Institute: ").strip()
    
    # Create user first
    query = """
        INSERT INTO user (user_name, email, password, role, age, dob, current_address, status)
        VALUES (%s, %s, %s, 'doctor', %s, %s, %s, 'active')
    """
    params = (name, email, password, age, dob, address)
    
    try:
        mysql.mysql_executor(conn, query, params)
        
        # Get the user_id
        user_id_query = "SELECT LAST_INSERT_ID()"
        user_id_result = mysql.mysql_executor(conn, user_id_query)
        user_id = user_id_result[0][0]
        
        # Create doctor record
        doctor_query = """
            INSERT INTO doctor (user_id, license_number, spec_id, spec_institute, doctor_desc)
            VALUES (%s, %s, %s, %s, 'New doctor')
        """
        doctor_params = (user_id, license, specialization, institute)
        mysql.mysql_executor(conn, doctor_query, doctor_params)
        
        print(f"\n✅ Doctor registered successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Name: {name}")
        
    except Exception as e:
        print(f"\n❌ Registration failed: {str(e)}")
    
    input("\nPress Enter to continue...")


def view_doctors(conn):
    """View all registered doctors"""
    clear_screen()
    print_header("👨‍⚕️ ALL DOCTORS")
    
    query = """
        SELECT u.user_id, u.user_name, u.email, d.license_number, s.spec_name, u.status
        FROM user u
        JOIN doctor d ON u.user_id = d.user_id
        LEFT JOIN specialization s ON d.spec_id = s.spec_id
        WHERE u.role = 'doctor'
    """
    
    try:
        doctors = mysql.mysql_executor(conn, query)
        
        if not doctors:
            print("No doctors registered yet.\n")
        else:
            print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'License':<15} {'Specialization':<20} {'Status':<10}")
            print("-" * 100)
            
            for doctor in doctors:
                spec = doctor[4] if doctor[4] else "N/A"
                print(f"{doctor[0]:<5} {doctor[1]:<20} {doctor[2]:<25} {doctor[3]:<15} {spec:<20} {doctor[5]:<10}")
            
            print(f"\nTotal doctors: {len(doctors)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")


# ============================================================================
# APPOINTMENT MANAGEMENT
# ============================================================================

def create_appointment(conn):
    """Create a new appointment"""
    clear_screen()
    print_header("📅 CREATE APPOINTMENT")
    
    print("Enter appointment details:\n")
    
    doctor_id = input("Doctor ID: ").strip()
    patient_id = input("Patient ID: ").strip()
    symptoms = input("Symptoms: ").strip()
    schedule_date = input("Schedule Date & Time (YYYY-MM-DD HH:MM:SS): ").strip()
    
    query = """
        INSERT INTO appointment (doctor_id, patient_id, scheduled_at, symptoms, status)
        VALUES (%s, %s, %s, %s, 'scheduled')
    """
    params = (doctor_id, patient_id, schedule_date, symptoms)
    
    try:
        mysql.mysql_executor(conn, query, params)
        print("\n✅ Appointment scheduled successfully!")
        
    except Exception as e:
        print(f"\n❌ Failed to schedule: {str(e)}")
    
    input("\nPress Enter to continue...")


def view_appointments(conn):
    """View all appointments"""
    clear_screen()
    print_header("📅 ALL APPOINTMENTS")
    
    query = """
        SELECT 
            a.appointment_id,
            d.user_name as doctor,
            p.user_name as patient,
            a.scheduled_at,
            a.symptoms,
            a.status
        FROM appointment a
        JOIN doctor doc ON a.doctor_id = doc.doctor_id
        JOIN user d ON doc.user_id = d.user_id
        JOIN patient pat ON a.patient_id = pat.patient_id
        JOIN user p ON pat.user_id = p.user_id
        ORDER BY a.scheduled_at DESC
    """
    
    try:
        appointments = mysql.mysql_executor(conn, query)
        
        if not appointments:
            print("No appointments scheduled yet.\n")
        else:
            print(f"{'ID':<5} {'Doctor':<20} {'Patient':<20} {'Scheduled':<20} {'Status':<12}")
            print("-" * 85)
            
            for apt in appointments:
                print(f"{apt[0]:<5} {apt[1]:<20} {apt[2]:<20} {str(apt[3]):<20} {apt[5]:<12}")
            
            print(f"\nTotal appointments: {len(appointments)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu(conn):
    """Main application menu"""
    while True:
        clear_screen()
        print_header("🏥 MEDICIENT - Healthcare Management System")
        
        print_menu({
            '1': 'Register Patient',
            '2': 'View All Patients',
            '3': 'Register Doctor',
            '4': 'View All Doctors',
            '5': 'Create Appointment',
            '6': 'View All Appointments',
            'q': 'Quit'
        })
        
        choice = input("Select option: ").strip().lower()
        
        if choice == '1':
            register_patient(conn)
        elif choice == '2':
            view_patients(conn)
        elif choice == '3':
            register_doctor(conn)
        elif choice == '4':
            view_doctors(conn)
        elif choice == '5':
            create_appointment(conn)
        elif choice == '6':
            view_appointments(conn)
        elif choice == 'q':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option!")
            input("Press Enter to continue...")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """Main application entry point"""
    clear_screen()
    print("\n" + "="*60)
    print("  🏥 MEDICIENT - Healthcare Management System")
    print("="*60)
    
    # Connect to database
    print("\n📡 Connecting to database...")
    print("Enter MySQL credentials:\n")
    
    host = input("Host [localhost]: ").strip() or 'localhost'
    user = input("User [root]: ").strip() or 'root'
    password = get_password_input("Password: ", security_checks=False)
    database = input("Database [medicient]: ").strip() or 'medicient'
    
    try:
        conn = mysql.create_conn(
            user=user,
            password=password,
            host=host,
            use_db=True,
            db=database
        )
        
        print("\n✅ Connected successfully!")
        input("Press Enter to continue...")
        
        # Run main menu
        main_menu(conn)
        
        # Close connection
        mysql.close_conn(conn)
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("\nMake sure:")
        print("  1. MySQL server is running")
        print("  2. Database 'medicient' exists")
        print("  3. Credentials are correct")
        sys.exit(1)


if __name__ == "__main__":
    main()
