'''
HANDLES KEYS OF THE USERS SECURELY 
'''
#==============================
# encryption Key Handling
#===============================
from utils import filesystem ,security
import errors
import os 
def save_encryption_key(dirpath:str,auto_generate:bool=False,key:str='')->None:
    '''
    saves the encryption key if not given auto generates it if auto_generate is True
    
    :param dirpath: path of folder to save key to 
    :param auto_generate: if true random key is generated
    :type auto_generate: bool
    :param key: key provided by user if auto_generate is false 
    :type key: str
    :returns None:when key is saved
    :raises InvalidArgumentError: if key is not provided for auto_generate = false
    :raises FolderNotFoundError: when folder is missing
    :raises GeneralFileError: if cannot save or convert key 
    '''
    # invalid args
    if not auto_generate and not key:
        raise errors.InvalidArgumentError(f'no key is given for auto_generate = False')
    # dir check
    if not filesystem.is_dir_exists(dirpath):
        raise errors.FolderNotFoundError(f'folder not found {dirpath}')
    # generating filepath
    filepath = os.path.join(dirpath,'encryption.key')
    # encryption
    try:
        
        if auto_generate:
            # auto generating key 
            fernet_key = security.generate_fernet_key()
        else:
            # not auto generated converting key to fernet safe 
            fernet_key = security.convert_into_fernet_key(key)
        # saving key 
        filesystem.write_raw_binary_file(
                filepath=filepath,
                data=fernet_key,
                overwrite=True
            )
        return None
    except Exception as e :
        raise errors.GeneralFileError(f'Could not save key : {str(e).strip()}')
def load_encryption_key(filepath:str)->bytes:
    '''
    saves the encryption key if not given auto generates it if auto_generate is True
    
    :param filepath: path of folder t
    :returns None:when key is saved
    :raises FolderNotFoundError: when folder is missing
    :raises GeneralFileError: if cannot load
    '''
    try:
        # file check
        if not filesystem.is_file_exists(filepath):
            raise errors.FolderNotFoundError(f'folder not found {filepath}')
        
        key = filesystem.read_raw_binary_file(filepath)
        return key
    except Exception as e :
        raise errors.GeneralFileError(f'Could not load key : {str(e).strip()}')
# ==============================================================
# security passphrase handling
# ==============================================================

def create_passphrase(dirpath:str,passphrase:str,encryption_key:bytes)->None:
    '''
    Saves Passphrase for app
    saves the encryption key if not given auto generates it if auto_generate is True
    
    :param dirpath: path of folder to save key to 
    :param passphrase: key provided by user if auto_generate is false 
    :type passphrase: str
    :returns None:when key is saved
    :raises FolderNotFoundError: when folder is missing
    :raises SecurityError: when encryption fails
    :raises GeneralFileError: if cannot save or convert key 
    '''
   # dir check
    if not filesystem.is_dir_exists(dirpath):
        raise errors.FolderNotFoundError(f'folder not found {dirpath}')
    # generating filepath
    filepath = os.path.join(dirpath,'passphrase.key')
    try:
        # encrypting passphrase
        encrypted_passphrase = security.encrypt(
            key=encryption_key,
            data=passphrase
            )
    except Exception as e:
        raise errors.SecurityError(f'Could not encrypt passphrase: {str(e).strip()}')
    try:
        # saving sudo key 
        filesystem.write_raw_binary_file(
                filepath=filepath,
                data=encrypted_passphrase,
                overwrite=True
            )
        return None
    except Exception as e :
        raise errors.GeneralFileError(f'Could not save passphrase : {str(e).strip()}')
def load_passphrase(
        filepath:str,
        encryption_key:bytes
    )->str:
    '''
    Loads passphrase from the saved location

    :params file_name: name of file 
    :param encryption_key: fernet key for decrypting data
    :returns passphrase: if found passphrase and decrypted it
    :raises FolderNotFoundError: when parent folder is missing
    :raises SecurityError: when decryption fails
    :raises GeneralFileError: if cannot load passphrase
    '''
     # dir check
    if not filesystem.is_file_exists(filepath):
        raise errors.FileNotFoundError(f'Parent folder not found {filepath}')
    try:
        # loading passphrase from the location
        encrypted_passphrase = filesystem.read_raw_binary_file(filepath)
        # decrypting passphrase
        decrypted_passphrase = security.decrypt(
            key=encryption_key,
            data=encrypted_passphrase
            )
        if decrypted_passphrase is None:
            raise errors.SecurityError(f'Could Not Decrypt Data : Invalid Key Provided or passphrase File Is Corrupted')
        return decrypted_passphrase
    except Exception as e :
        raise errors.GeneralFileError(f'Could not save passphrase : {str(e).strip()}')
 
#===========================================
# Passwords Handling
#===========================================  
def save_password(
        dirpath:str,
        file_name:str,
        password:str,
        encryption_key:bytes
        )->None:
    '''
    Saves the password to the specified location

    :params dirpath: path of folder to save password to
    :params file_name: name of file 
    :params password: root password provided by user 
    :param encryption_key: fernet key for encrypting data
    :returns None: when key is saved
    :raises FolderNotFoundError: when parent folder is missing
    :raises SecurityError: when encryption fails
    :raises GeneralFileError: if cannot save password
    '''
     # dir check
    if not filesystem.is_dir_exists(dirpath):
        raise errors.FolderNotFoundError(f'Parent folder not found {dirpath}')
    try:
        # generating filepath
        filepath = os.path.join(dirpath,file_name)
        # encrypting password
        encrypted_password = security.encrypt(
            key=encryption_key,
            data=password
            )
    except Exception as e:
        raise errors.SecurityError(f'Could not encrypt password: {str(e).strip()}')
    try:
        # saving sudo key 
        filesystem.write_raw_binary_file(
                filepath=filepath,
                data=encrypted_password,
                overwrite=True
            )
        return None
    except Exception as e :
        raise errors.GeneralFileError(f'Could not save password : {str(e).strip()}')
    
def load_password(
        filepath:str,
        encryption_key:bytes
    )->str:
    '''
    Loads password from the saved location

    :params dirpath: path of folder to save password to
    :params file_name: name of file 
    :param encryption_key: fernet key for decrypting data
    :returns password: if found password and decrypted it
    :raises FolderNotFoundError: when parent folder is missing
    :raises GeneralFileError: if cannot save key
    '''
     # file check
    if not filesystem.is_file_exists(filepath):
        raise errors.FileNotFoundError(f'Parent folder not found {filepath}')
    try:
        # loading password from the location
        encrypted_password = filesystem.read_raw_binary_file(filepath)
        # decrypting password
        decrypted_password = security.decrypt(
            key=encryption_key,
            data=encrypted_password
            )
        if decrypted_password is None:
            raise errors.SecurityError(f'Could Not Decrypt Data : Invalid Key Provided or Password File Is Corrupted')
        return decrypted_password
    except Exception as e :
        raise errors.GeneralFileError(f'Could not load password : {str(e).strip()}')
