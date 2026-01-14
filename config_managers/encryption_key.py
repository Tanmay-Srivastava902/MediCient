'''Manages application encryption key lifecycle'''

import utils
from results import Result


# ============================================================================
# ENCRYPTION KEY MANAGEMENT
# ============================================================================

def init_encryption_key(dirpath: str, filepath: str, key: bytes) -> Result:
    """
    Initializes or updates the application's encryption key.
    
    Args:
        dirpath: Directory where key will be stored
        filepath: Full path to key file
        key: Fernet encryption key (from utils.generate_fernet_key())
        
    Returns:
        Result: Success with confirmation message, or failure with error code
        
    Error Codes:
        401: Directory doesn't exist
        410: Invalid key or file operation failed
        
    Note: Always overwrites existing key - this is intentional for re-initialization
    
    Example:
        key = utils.generate_fernet_key()
        result = init_encryption_key('~/.config/.medicient', '~/.config/.medicient/app_encryption.key', key)
    """
    try:
        # Check directory exists
        if not utils.is_dir_exists(dirpath):
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Directory does not exist: {dirpath}"
            )
        
        # Validate key format (try to create Fernet instance)
        try:
            from cryptography.fernet import Fernet
            Fernet(key)  # Raises ValueError if invalid
        except (ValueError, Exception) as e:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Invalid Fernet key: {str(e)}"
            )
        
        # Store the key (always overwrite for re-initialization)
        result = utils.write_binary_file(filepath, key, overwrite=True)
        
        if result.ok:
            return Result(
                success=True,
                data=f"Encryption key initialized: {filepath}"
            )
        else:
            return Result(
                success=False,
                error_code=410,
                error_msg=f"Failed to write key: {result.error_msg}"
            )
            
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Unexpected error: {str(e)}"
        )


def load_encryption_key(filepath: str) -> Result:
    """
    Loads the application's encryption key from disk.
    
    Args:
        filepath: Full path to key file
        
    Returns:
        Result: Success with key as bytes in .data, or failure with error code
        
    Error Codes:
        404: Key file doesn't exist
        410: Failed to read key file
        
    Example:
        result = load_encryption_key('~/.config/.medicient/app_encryption.key')
        if result.ok:
            key = result.data  # bytes
    """
    try:
        result = utils.read_binary_file(filepath)
        
        if result.ok:
            return Result(
                success=True,
                data=result.data  # bytes
            )
        else:
            # Pass through the error from file operation
            return result
            
    except Exception as e:
        return Result(
            success=False,
            error_code=410,
            error_msg=f"Failed to load key: {str(e)}"
        )


def ensure_encryption_key(dirpath: str, filepath: str) -> Result:
    """
    Ensures encryption key exists, creating it if necessary.
    
    This is a convenience function for setup scripts that combines:
    1. Check if key exists
    2. If not, create directory and generate key
    3. Return the key
    
    Args:
        dirpath: Directory where key should be stored
        filepath: Full path to key file
        
    Returns:
        Result: Success with key in .data, or failure with error code
        
    Example:
        result = ensure_encryption_key('~/.config/.medicient', '~/.config/.medicient/app_encryption.key')
        if result.ok:
            key = result.data  # Ready to use!
    """
    # Try to load existing key
    result = load_encryption_key(filepath)
    if result.ok:
        return result  # Key already exists
    
    # Key doesn't exist - create it
    # First ensure directory exists
    if not utils.is_dir_exists(dirpath):
        dir_result = utils.create_dir(
                dirpath=dirpath,
                mode=0o700  # Owner only (secure!)
            )
        if not dir_result.ok:
            return Result(
                success=False,
                error_code=401,
                error_msg=f"Failed to create key directory: {dir_result.error_msg}"
            )
    
    # Generate new key
    key = utils.generate_fernet_key()
    
    # Initialize it
    init_result = init_encryption_key(dirpath, filepath, key)
    if not init_result.ok:
        return init_result
    
    # Return the newly created key
    return Result(
        success=True,
        data=key
    )
