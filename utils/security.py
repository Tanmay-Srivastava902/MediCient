'''Manages encryption and hashing for security'''

from cryptography.fernet import Fernet, InvalidToken


# ============================================================================
# ENCRYPTION KEY MANAGEMENT
# ============================================================================

def generate_fernet_key() -> bytes:
    """
    Generates a new Fernet encryption key.
    
    Returns:
        bytes: A URL-safe base64-encoded 32-byte key
        
    Note: Caller must store this key securely. Losing the key means losing
          access to all encrypted data.
    """
    return Fernet.generate_key()


def create_fernet_instance(key: bytes) -> Fernet:
    """
    Creates a Fernet cipher instance.
    
    Args:
        key: Encryption key (from generate_fernet_key)
        
    Returns:
        Fernet: Configured cipher instance
        
    Note: Internal function - use encrypt/decrypt instead
    """
    return Fernet(key)


# ============================================================================
# ENCRYPTION / DECRYPTION
# ============================================================================

def encrypt(key: bytes, data: str) -> bytes:
    """
    Encrypts string data using Fernet symmetric encryption.
    
    Args:
        key: Encryption key (from generate_fernet_key)
        data: Plain text to encrypt
        
    Returns:
        bytes: Encrypted data (base64-encoded)
        
    Example:
        key = generate_fernet_key()
        encrypted = encrypt(key, "secret message")
    """
    fernet = create_fernet_instance(key)
    return fernet.encrypt(data.encode())


def decrypt(key: bytes, data: bytes) -> str | None:
    """
    Decrypts Fernet-encrypted data.
    
    Args:
        key: Encryption key (same one used to encrypt)
        data: Encrypted bytes (from encrypt function)
        
    Returns:
        str: Decrypted plain text
        None: If key is invalid or data is corrupted
        
    Example:
        decrypted = decrypt(key, encrypted)
        if decrypted:
            print(f"Message: {decrypted}")
    """
    try:
        fernet = create_fernet_instance(key)
        return fernet.decrypt(data).decode()
    except (InvalidToken, ValueError):
        print("❌ Invalid key or corrupted data")
        return None


# ============================================================================
# HASHING (ONE-WAY)
# ============================================================================

def hash_data(data: str) -> str:
    """
    Creates SHA-256 hash of data (one-way, cannot be decrypted).
    
    Args:
        data: String to hash
        
    Returns:
        str: Hexadecimal hash (64 characters)
        
    Use Cases:
        - Password storage (store hash, not password)
        - Data integrity verification
        - Creating unique identifiers
        
    Example:
        password_hash = hash_data("user_password")
        # Store password_hash in database, not actual password
    """
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()


# ============================================================================
# BASE64 UTILITIES 
# ============================================================================

def encode_base64_urlsafe(data: str) -> str:
    """
    Encodes string to URL-safe base64.
    
    Note: Only needed if you're doing base64 encoding for purposes OTHER
          than Fernet (which handles base64 internally).
    """
    import base64
    return base64.urlsafe_b64encode(data.encode()).decode()


def decode_base64_urlsafe(data: str) -> str:
    """
    Decodes URL-safe base64 to string.
    
    Note: Only needed if you're doing base64 decoding for purposes OTHER
          than Fernet (which handles base64 internally).
    """
    import base64
    return base64.urlsafe_b64decode(data).decode()


# ============================================================================
# TESTS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SECURITY MODULE TEST SUITE")
    print("="*60)

    # Test 1: Key Generation
    print("\n[TEST 1] Generate Encryption Key")
    try:
        key = generate_fernet_key()
        # Verify it's a valid Fernet key by creating instance
        Fernet(key)
        print(f"✅ Generated valid key: {key}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # generating random key to test further
    key = Fernet.generate_key()
    # Test 2: Encryption
    print("\n[TEST 2] Encrypt Data")
    test_data = "SECURE DATA: SECRET! 🔒❤️"
    encrypted = encrypt(key, test_data)
    print(f"✅ Encrypted: {encrypted}")

    # Test 3: Decryption (Correct Key)
    print("\n[TEST 3] Decrypt Data (Correct Key)")
    decrypted = decrypt(key, encrypted)
    if decrypted == test_data:
        print(f"✅ Decrypted correctly: {decrypted}")
    else:
        print(f"❌ Mismatch! Got: {decrypted}")

    # Test 4: Decryption (Wrong Key)
    print("\n[TEST 4] Decrypt Data (Wrong Key)")
    wrong_key = generate_fernet_key()
    result = decrypt(wrong_key, encrypted)
    if result is None:
        print("✅ Correctly rejected wrong key")
    else:
        print(f"❌ Should have returned None, got: {result}")

    # Test 5: Hashing
    print("\n[TEST 5] Hash Data")
    hash1 = hash_data("password123")
    hash2 = hash_data("password123")
    hash3 = hash_data("password124")
    
    if hash1 == hash2:
        print("✅ Same input produces same hash")
    else:
        print("❌ Inconsistent hashing")
        
    if hash1 != hash3:
        print("✅ Different input produces different hash")
    else:
        print("❌ Hash collision!")
    
    print(f"   Hash: {hash1}")

    # Test 6: Base64 Encoding 
    print("\n[TEST 6] Base64 Encoding")
    encoded = encode_base64_urlsafe(test_data)
    decoded = decode_base64_urlsafe(encoded)
    if decoded == test_data:
        print(f"✅ Base64 round-trip successful")
    else:
        print(f"❌ Base64 failed")

    # Test 7: Hash Irreversibility
    print("\n[TEST 7] Hash Is One-Way")
    original = "my_password"
    hashed = hash_data(original)
    print(f"   Original: {original}")
    print(f"   Hash: {hashed}")
    print("✅ Cannot reverse hash to get original (by design)")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETE ✅")
    print("="*60)