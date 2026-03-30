import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

DEFAULT_ITERATIONS = 600_000
SALT_SIZE = 16


def gen_salt() -> bytes:
    """Generate a random salt for key derivation."""
    return os.urandom(SALT_SIZE)


def derive_key(
    master_password: str, 
    salt: bytes, 
    iterations: int = DEFAULT_ITERATIONS
) -> bytes:
    """Derive a secure key from password and salt using PBKDF2.
    
    Args:
        master_password: The master password string.
        salt: Random salt bytes.
        iterations: Number of iterations (default: 600,000).
        
    Returns:
        URL-safe base64 encoded derived key.
    """
    password_bytes = master_password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return urlsafe_b64encode(kdf.derive(password_bytes))


def encrypt_data(key: bytes, plaintext: str) -> bytes:
    """Encrypt plaintext using Fernet symmetric encryption.
    
    Args:
        key: Encryption key from derive_key().
        plaintext: Data to encrypt.
        
    Returns:
        Encrypted ciphertext.
    """
    cipher = Fernet(key)
    return cipher.encrypt(plaintext.encode('utf-8'))


def decrypt_data(key: bytes, ciphertext: bytes) -> str:
    """Decrypt ciphertext using Fernet symmetric encryption.
    
    Args:
        key: Encryption key from derive_key().
        ciphertext: Data to decrypt.
        
    Returns:
        Decrypted plaintext.
    """
    cipher = Fernet(key)
    return cipher.decrypt(ciphertext).decode('utf-8')