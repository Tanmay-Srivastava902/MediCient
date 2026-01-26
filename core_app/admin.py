# # In config_managers/encryption_and_passwords.py
# from mysql.connector.abstracts import MySQLCursorAbstract
# from data_operators import records , table
# from utils import prompt , filesystem , security
# import errors
# import datetime
# def verify_admin_password(provided_password: str, encryption_key: bytes) -> bool:
#     """
#     Verify if provided password matches stored admin password
    
#     Logic:
#     1. Load encrypted admin password from file
#     2. Decrypt it using encryption_key
#     3. Compare with provided_password
#     4. Return True/False
#     """

#     # Load encrypted password
#     encrypted_stored = filesystem.read_raw_binary_file()
    
#     # Decrypt
#     decrypted = security.decrypt(key=encryption_key, data=encrypted_stored)
    
#     # Compare
#     return decrypted == provided_password
