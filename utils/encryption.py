from cryptography.fernet import Fernet
from utils.key_manager import load_key

# Load the encryption key
key = load_key()
fernet = Fernet(key)

# Encrypt a plain text password
def encrypt_password(plain_password):
    return fernet.encrypt(plain_password.encode()).decode()

# Decrypt an encrypted password
def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()
