'''THIS MODULE CREATES THE SCHEMA FILE FOR MYSQL USE IN CASE OF CORRUPTED schema.sql'''

DEFAULT_DATABASE_SCHEMA = '''-- Medicient Database Schema
-- Created: January 9, 2026
-- This file creates the complete database schema for the medicient medical management system

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS medical_history;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS disease;
DROP TABLE IF EXISTS specialization;
DROP TABLE IF EXISTS user;

-- Create user table (base table - no dependencies)
CREATE TABLE user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('doctor', 'patient', 'admin') NOT NULL,
    age INT NOT NULL,
    dob DATE NOT NULL,
    current_address VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('inactive', 'active', 'suspended') NOT NULL DEFAULT 'inactive'
);

-- Create specialization table (base table - no dependencies)
CREATE TABLE specialization (
    spec_id INT PRIMARY KEY AUTO_INCREMENT,
    spec_name VARCHAR(30) NOT NULL UNIQUE,
    spec_desc TEXT NOT NULL,
    treats_diseases TEXT NOT NULL
);

-- Create disease table (base table - no dependencies)
CREATE TABLE disease (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(50) NOT NULL UNIQUE,
    symptoms TEXT NOT NULL,
    disease_desc TEXT NOT NULL,
    medicines_preferred TEXT NOT NULL,
    precautions_needed TEXT NOT NULL
);

-- Create patient table (depends on user)
CREATE TABLE patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    height FLOAT NOT NULL,
    weight FLOAT,
    patient_desc TEXT,
    current_location TEXT,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Create doctor table (depends on user and specialization)
CREATE TABLE doctor (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    spec_id INT NOT NULL,
    skills TEXT,
    doctor_desc TEXT,
    spec_institute VARCHAR(50) NOT NULL,
    work_location TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (spec_id) REFERENCES specialization(spec_id)
);

-- Create medical_history table (depends on doctor, patient, and disease)
CREATE TABLE medical_history (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    disease_id INT NOT NULL,
    symptoms TEXT,
    treatment TEXT,
    medicines TEXT,
    prevention TEXT,
    diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'recovered') NOT NULL DEFAULT 'active',
    note TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (disease_id) REFERENCES disease(disease_id)
);

-- Create appointment table (depends on doctor, patient, and optionally medical_history)
CREATE TABLE appointment (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    scheduled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    symptoms TEXT NOT NULL,
    medical_history_id INT,
    status ENUM('scheduled', 'canceled', 'ongoing', 'ended') NOT NULL DEFAULT 'scheduled',
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (medical_history_id) REFERENCES medical_history(record_id)
);

-- Updating auto increment (as doctor id ,patient id and appointment id is to be shared with users)
ALTER TABLE doctor AUTO_INCREMENT = 100000;
ALTER TABLE patient AUTO_INCREMENT = 100000;
ALTER TABLE appointment AUTO_INCREMENT = 10000000;
'''

import os 
import utils 
from results import Result


def create_database_schema(filepath: str) -> Result:
    """
    Creates the Medicient database schema SQL file.
    
    This generates a schema.sql file that can be used to:
    - Set up a fresh database installation
    - Recover from corrupted schema files
    - Recreate database structure after errors
    
    Args:
        filepath: Path where schema.sql should be created
    
    Returns:
        Result: Success with file path, or failure with error code
    
    Error Codes:
        401: Parent directory doesn't exist
        410: Failed to write schema file
    
    Example:
        result = create_database_schema('configs/schema.sql')
        if result.ok:
            print(f"Schema created at: {result.data}")
    """
    try:
        # Check parent directory exists
        parent_folder = os.path.dirname(filepath)
        if not utils.is_dir_exists(parent_folder) and parent_folder:
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory does not exist: {parent_folder}"
            )
        
        # Write schema file
        result = utils.write_txt_file(
            filepath=filepath,
            data=DEFAULT_DATABASE_SCHEMA,
            overwrite=True  # Always overwrite (regenerate schema)
        )
        
        if not result.ok:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Failed to write schema: {result.error_msg}"
            )
        
        return Result(
            success=True,
            data=f"Medicient schema created at {filepath}"
        )
    
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e)}"
        )
