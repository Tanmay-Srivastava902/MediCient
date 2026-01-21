def main_menu():
    options= [
        "app_setup",
        "user_profile",
        "medicines_available",# names wise or 
        "doctors_available",# category wise
        "dashboard" # redirects to main dashboard
    ]
    pass
def initial_setup_menu():
    options = [
        "complete_setup",
        "verify_installation",
        "show_install_info",
        "show_app_info",
        "change_app_key",
        "reinstall_app",
        "uninstall_app",
        "start_app"
    ]
    pass

def initial_app_menu():
    # always used for first non login system
    options = [
        "show_app_info",
        "Login/Register",
        "test_app",
        "our_features",
        "update_app",
        "close_app"

    ]
    pass
def patient_dashboard():
    # always pop_up when patient is first logged in 
    options =[
        "main_menu",
        "user_profile",
        "disease_info",
        "medications_info",
        "inform_doctor",
        "book_appointment",
        "doctor_desk",
        "update_tracker",
        "show_tracker",
        "show_patient_report",
        "log_out"
        
    ]
    pass
def doctor_dashboard():
    # always popped when a doctor logged in
    options = [
        "user_profile",
        "review_patients"
        "add_patients",
        "remove_patients"
        # only doctor can add medicines or review medicines and only add specializations
        # only if no user is taking medications for that then
        "manage_medicines",
        "show_appointments",
        "show_current_cases"
        "review_emergency_cases",
        "show_monthly_report"
        "log_out"
    ]
    pass
def admin_dashboard():
    # always when logged in as admin with the master password
    options =[
        "manage_doctors",
        "manage_medicines",
        "manage_patients",
        "manage_specialization "
        "manage_users",
        "update_app_info",
        "update_app_configurations",
        "log_out"

    ]
    pass
def user_profile():
    # manages user profile

    options =[
        "show_profile",
        "update_profile",
        "log_out",
        "delete_account"
    ]
    pass
def doctor_profile():
    # manages doctors professional profile (public profile)
    options  = [
        "show_public_profile",
        "update_specialization",
        "update_doctor_id",
        "update_work_location",
        "update_desc"
    ]
    pass
def patient_profile():
      # manages patients profile  ( patient cannot add or remove medications and disease of his_her)
    options  = [
        "show_patient_profile",
        "update_disease_",
        "update_doctor_id",
        "update_work_location",
        "update_desc"
    ]
    pass
def review_patients():
    # used to manage patients by doctors 
    """patients info here full details"""
    options =[
        "enter patient id to find ",
        "enter disease id to select patients"
    ]
    pass
def show_appointments():
    pass