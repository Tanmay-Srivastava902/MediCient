
# Appointments
from .appointments import (
	get_user_role as appointment_get_user_role,
	is_doctor_exists,
	is_patient_exists,
	is_patient_appointment,
	is_doctor_appointment,
	is_appointment_exists,
	search_doctor,
	know_patient_id,
	know_appointment_id,
	book_appointment,
	view_appointment,
	cancel_appointment,
	update_appointment_status
)

# Doctors
from .doctors import (
	get_user_role as doctor_get_user_role,
	validate_doctor_license,
	show_available_specifications,
	is_specification_valid,
	know_doctor_id,
	complete_doctor_profile
)

# Medical History
from .medical_history import (
	get_user_role as medical_history_get_user_role,
	is_doctor_exists as medical_history_is_doctor_exists,
	is_patient_exists as medical_history_is_patient_exists,
	is_doctor_medical_history,
	is_disease_exists,
	is_appointment_exists as medical_history_is_appointment_exists,
	is_medical_history_exists,
	add_medical_history,
	view_medical_history,
	update_medical_history_status
)

# Patients
from .patients import (
	get_user_role as patient_get_user_role,
	is_specification_valid as patient_is_specification_valid,
	know_patient_id as patient_know_patient_id,
	complete_patient_profile
)

# Users
from .users import (
	is_user_exists,
	verify_admin_identity,
	get_user_role as user_get_user_role,
	verify_user_role,
	know_your_user_id,
	know_spec_id,
	know_disease_id,
	register,
	login,
	add_specialization,
	add_disease
)
# Exported symbols
__all__ = [
	# Appointments
	'appointment_get_user_role', 'is_doctor_exists', 'is_patient_exists', 'is_patient_appointment',
	'is_doctor_appointment', 'is_appointment_exists', 'search_doctor', 'know_patient_id',
	'know_appointment_id', 'book_appointment', 'view_appointment', 'cancel_appointment', 'update_appointment_status',

	# Doctors
	'doctor_get_user_role', 'validate_doctor_license', 'show_available_specifications',
	'is_specification_valid', 'know_doctor_id', 'complete_doctor_profile',

	# Medical History
	'medical_history_get_user_role', 'medical_history_is_doctor_exists', 'medical_history_is_patient_exists',
	'is_doctor_medical_history', 'is_disease_exists', 'medical_history_is_appointment_exists',
	'is_medical_history_exists', 'add_medical_history', 'view_medical_history', 'update_medical_history_status',

	# Patients
	'patient_get_user_role', 'patient_is_specification_valid', 'patient_know_patient_id', 'complete_patient_profile',

	# Users
	'is_user_exists', 'verify_admin_identity', 'user_get_user_role', 'verify_user_role',
	'know_your_user_id', 'know_spec_id', 'know_disease_id', 'register', 'login',
	'add_specialization', 'add_disease'
]