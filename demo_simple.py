#!/usr/bin/env python3
"""
MEDICIENT - Healthcare Management System
ONE-FILE DEMO VERSION for Practicals

Simple, working, demo-ready code.
No complicated architecture - just functions that work!

Author: Tanmay Srivastava (Biology 12th)
Date: January 21, 2026
"""

import mysql.connector
import hashlib
import getpass
import os
from datetime import datetime

# ============================================================================
# DATABASE CONNECTION (Simple & Direct)
# ============================================================================

def get_connection():
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='SecurePass@1201',  # Will prompt if empty
            database='medicient'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None


# ============================================================================
# UTILITY FUNCTIONS (Simple versions)
# ============================================================================

def clear_screen():
    """Clear terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')


def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


def get_password():
    """Get password securely"""
    return getpass.getpass("Password: ")


def print_header(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title.center(66)}")
    print("="*70 + "\n")


def print_success(msg):
    """Print success message"""
    print(f"\n✅ {msg}\n")


def print_error(msg):
    """Print error message"""
    print(f"\n❌ {msg}\n")


# ============================================================================
# USER REGISTRATION
# ============================================================================

def register_patient(conn):
    """Register a new patient - SIMPLE VERSION"""
    clear_screen()
    print_header("REGISTER PATIENT")
    
    # Get basic info
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = get_password()
    password_hash = hash_password(password)
    
    age = int(input("Age: ").strip())
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    address = input("Address: ").strip()
    height = float(input("Height (cm): ").strip())
    weight = float(input("Weight (kg): ").strip())
    
    cursor = conn.cursor()
    
    try:
        # Insert user
        user_query = """
            INSERT INTO user (user_name, email, password, role, age, dob, current_address, status)
            VALUES (%s, %s, %s, 'patient', %s, %s, %s, 'active')
        """
        cursor.execute(user_query, (name, email, password_hash, age, dob, address))
        user_id = cursor.lastrowid
        
        # Insert patient
        patient_query = """
            INSERT INTO patient (user_id, height, weight, patient_desc)
            VALUES (%s, %s, %s, 'New patient')
        """
        cursor.execute(patient_query, (user_id, height, weight))
        
        conn.commit()
        print_success(f"Patient registered! ID: {user_id}, Name: {name}")
        
    except mysql.connector.Error as e:
        conn.rollback()
        print_error(f"Registration failed: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


def register_doctor(conn):
    """Register a new doctor - SIMPLE VERSION"""
    clear_screen()
    print_header("REGISTER DOCTOR")
    
    # Get basic info
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = get_password()
    password_hash = hash_password(password)
    
    age = int(input("Age: ").strip())
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    address = input("Address: ").strip()
    license = input("License Number: ").strip()
    specialization = input("Specialization (e.g., Cardiology, Neurology): ").strip()
    institute = input("Medical Institute: ").strip()
    
    cursor = conn.cursor()
    
    try:
        # Check if specialization exists, if not create it
        cursor.execute("SELECT spec_id FROM specialization WHERE spec_name = %s", (specialization,))
        result = cursor.fetchone()
        
        if result:
            spec_id = result[0]
        else:
            # Create new specialization
            spec_query = """
                INSERT INTO specialization (spec_name, spec_desc, treats_diseases)
                VALUES (%s, %s, %s)
            """
            cursor.execute(spec_query, (specialization, f"{specialization} specialist", "Various"))
            spec_id = cursor.lastrowid
        
        # Insert user
        user_query = """
            INSERT INTO user (user_name, email, password, role, age, dob, current_address, status)
            VALUES (%s, %s, %s, 'doctor', %s, %s, %s, 'active')
        """
        cursor.execute(user_query, (name, email, password_hash, age, dob, address))
        user_id = cursor.lastrowid
        
        # Insert doctor
        doctor_query = """
            INSERT INTO doctor (user_id, license_number, spec_id, spec_institute, doctor_desc)
            VALUES (%s, %s, %s, %s, 'New doctor')
        """
        cursor.execute(doctor_query, (user_id, license, spec_id, institute))
        
        conn.commit()
        print_success(f"Doctor registered! ID: {user_id}, Name: {name}")
        
    except mysql.connector.Error as e:
        conn.rollback()
        print_error(f"Registration failed: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


# ============================================================================
# VIEW RECORDS
# ============================================================================

def view_patients(conn):
    """View all patients"""
    clear_screen()
    print_header("ALL PATIENTS")
    
    cursor = conn.cursor()
    
    query = """
        SELECT u.user_id, u.user_name, u.email, u.age, p.height, p.weight, u.status
        FROM user u
        JOIN patient p ON u.user_id = p.user_id
        WHERE u.role = 'patient'
        ORDER BY u.user_id DESC
    """
    
    try:
        cursor.execute(query)
        patients = cursor.fetchall()
        
        if not patients:
            print("No patients registered yet.\n")
        else:
            # Header
            print(f"{'ID':<6} {'Name':<25} {'Email':<30} {'Age':<5} {'Height':<8} {'Weight':<8} {'Status':<10}")
            print("-" * 100)
            
            # Rows
            for p in patients:
                print(f"{p[0]:<6} {p[1]:<25} {p[2]:<30} {p[3]:<5} {p[4]:<8.1f} {p[5]:<8.1f} {p[6]:<10}")
            
            print(f"\n📊 Total patients: {len(patients)}")
        
    except mysql.connector.Error as e:
        print_error(f"Error: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


def view_doctors(conn):
    """View all doctors"""
    clear_screen()
    print_header("ALL DOCTORS")
    
    cursor = conn.cursor()
    
    query = """
        SELECT u.user_id, u.user_name, u.email, d.license_number, 
               s.spec_name, u.status
        FROM user u
        JOIN doctor d ON u.user_id = d.user_id
        LEFT JOIN specialization s ON d.spec_id = s.spec_id
        WHERE u.role = 'doctor'
        ORDER BY u.user_id DESC
    """
    
    try:
        cursor.execute(query)
        doctors = cursor.fetchall()
        
        if not doctors:
            print("No doctors registered yet.\n")
        else:
            # Header
            print(f"{'ID':<6} {'Name':<25} {'Email':<30} {'License':<20} {'Specialization':<20} {'Status':<10}")
            print("-" * 115)
            
            # Rows
            for d in doctors:
                spec = d[4] if d[4] else "N/A"
                print(f"{d[0]:<6} {d[1]:<25} {d[2]:<30} {d[3]:<20} {spec:<20} {d[5]:<10}")
            
            print(f"\n📊 Total doctors: {len(doctors)}")
        
    except mysql.connector.Error as e:
        print_error(f"Error: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


# ============================================================================
# APPOINTMENT MANAGEMENT
# ============================================================================

def create_appointment(conn):
    """Create appointment"""
    clear_screen()
    print_header("CREATE APPOINTMENT")
    
    # Show available doctors first
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.doctor_id, u.user_name, s.spec_name
        FROM doctor d
        JOIN user u ON d.user_id = u.user_id
        LEFT JOIN specialization s ON d.spec_id = s.spec_id
        WHERE u.status = 'active'
    """)
    doctors = cursor.fetchall()
    
    if not doctors:
        print_error("No doctors available!")
        cursor.close()
        input("Press Enter to continue...")
        return
    
    print("Available Doctors:")
    print(f"{'ID':<6} {'Name':<25} {'Specialization':<20}")
    print("-" * 55)
    for d in doctors:
        spec = d[2] if d[2] else "N/A"
        print(f"{d[0]:<6} {d[1]:<25} {spec:<20}")
    
    print()
    doctor_id = int(input("Select Doctor ID: ").strip())
    patient_id = int(input("Enter Patient ID: ").strip())
    symptoms = input("Symptoms: ").strip()
    schedule = input("Schedule (YYYY-MM-DD HH:MM:SS) or press Enter for now: ").strip()
    
    if not schedule:
        schedule = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        query = """
            INSERT INTO appointment (doctor_id, patient_id, scheduled_at, symptoms, status)
            VALUES (%s, %s, %s, %s, 'scheduled')
        """
        cursor.execute(query, (doctor_id, patient_id, schedule, symptoms))
        conn.commit()
        
        print_success(f"Appointment created! Scheduled for: {schedule}")
        
    except mysql.connector.Error as e:
        conn.rollback()
        print_error(f"Failed: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


def view_appointments(conn):
    """View all appointments"""
    clear_screen()
    print_header("ALL APPOINTMENTS")
    
    cursor = conn.cursor()
    
    query = """
        SELECT 
            a.appointment_id,
            doc_user.user_name as doctor,
            pat_user.user_name as patient,
            a.scheduled_at,
            a.symptoms,
            a.status
        FROM appointment a
        JOIN doctor d ON a.doctor_id = d.doctor_id
        JOIN user doc_user ON d.user_id = doc_user.user_id
        JOIN patient p ON a.patient_id = p.patient_id
        JOIN user pat_user ON p.user_id = pat_user.user_id
        ORDER BY a.scheduled_at DESC
    """
    
    try:
        cursor.execute(query)
        appointments = cursor.fetchall()
        
        if not appointments:
            print("No appointments scheduled yet.\n")
        else:
            # Header
            print(f"{'ID':<6} {'Doctor':<25} {'Patient':<25} {'Scheduled':<20} {'Status':<12}")
            print("-" * 95)
            
            # Rows
            for apt in appointments:
                print(f"{apt[0]:<6} {apt[1]:<25} {apt[2]:<25} {str(apt[3]):<20} {apt[5]:<12}")
            
            print(f"\n📊 Total appointments: {len(appointments)}")
        
    except mysql.connector.Error as e:
        print_error(f"Error: {e}")
    
    finally:
        cursor.close()
    
    input("\nPress Enter to continue...")


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu(conn):
    """Main application menu"""
    while True:
        clear_screen()
        print_header("🏥 MEDICIENT - Healthcare Management System")
        
        print("  [1] Register Patient")
        print("  [2] View All Patients")
        print("  [3] Register Doctor")
        print("  [4] View All Doctors")
        print("  [5] Create Appointment")
        print("  [6] View All Appointments")
        print("  [Q] Quit\n")
        
        choice = input("Select option: ").strip().upper()
        
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
        elif choice == 'Q':
            print("\n👋 Thank you for using Medicient!\n")
            break
        else:
            print_error("Invalid option!")
            input("Press Enter to continue...")


# ============================================================================
# DATABASE SETUP
# ============================================================================

def setup_database():
    """Setup database and tables"""
    clear_screen()
    print_header("DATABASE SETUP")
    
    print("Setting up Medicient database...\n")
    
    # Connect without database first
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        
        # Create database
        print("📦 Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS medicient")
        cursor.execute("USE medicient")
        print("✅ Database created/selected\n")
        
        # Create tables
        print("📋 Creating tables...")
        
        # User table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                user_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('doctor', 'patient', 'admin') NOT NULL,
                age INT NOT NULL,
                dob DATE NOT NULL,
                current_address VARCHAR(200) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('inactive', 'active', 'suspended') DEFAULT 'active'
            )
        """)
        
        # Specialization table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS specialization (
                spec_id INT PRIMARY KEY AUTO_INCREMENT,
                spec_name VARCHAR(50) NOT NULL UNIQUE,
                spec_desc TEXT,
                treats_diseases TEXT
            )
        """)
        
        # Patient table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient (
                patient_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL UNIQUE,
                height FLOAT NOT NULL,
                weight FLOAT,
                patient_desc TEXT,
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            )
        """)
        
        # Doctor table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctor (
                doctor_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL UNIQUE,
                license_number VARCHAR(50) NOT NULL UNIQUE,
                spec_id INT NOT NULL,
                spec_institute VARCHAR(100) NOT NULL,
                doctor_desc TEXT,
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (spec_id) REFERENCES specialization(spec_id)
            )
        """)
        
        # Appointment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointment (
                appointment_id INT PRIMARY KEY AUTO_INCREMENT,
                doctor_id INT NOT NULL,
                patient_id INT NOT NULL,
                scheduled_at TIMESTAMP NOT NULL,
                symptoms TEXT NOT NULL,
                status ENUM('scheduled', 'canceled', 'ongoing', 'ended') DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
                FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
            )
        """)
        
        conn.commit()
        print("✅ All tables created successfully!\n")
        
        cursor.close()
        conn.close()
        
        print_success("Database setup complete!")
        return True
        
    except mysql.connector.Error as e:
        print_error(f"Setup failed: {e}")
        return False


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    clear_screen()
    print("\n" + "="*70)
    print("  🏥 MEDICIENT - Healthcare Management System")
    print("  Simple Demo Version for Practicals")
    print("="*70 + "\n")
    
    # Check if database needs setup
    print("Checking database...\n")
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='medicient'
        )
        print("✅ Database connected!\n")
        conn.close()
        
    except mysql.connector.Error:
        print("⚠️  Database not found. Running setup...\n")
        input("Press Enter to setup database...")
        
        if not setup_database():
            print("\n❌ Setup failed. Please check MySQL is running.")
            return
        
        input("\nPress Enter to continue...")
    
    # Connect to database
    conn = get_connection()
    
    if not conn:
        print("\n❌ Could not connect to database.")
        print("\nMake sure:")
        print("  1. MySQL server is running: sudo systemctl start mysql")
        print("  2. Root password is correct (or empty)")
        return
    
    # Run main menu
    try:
        main_menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
