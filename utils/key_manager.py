from cryptography.fernet import Fernet

# Generate and save a key
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    print("Encryption key generated and saved to 'key.key'.")

# Load the saved key
def load_key():
    with open('key.key', 'rb') as key_file:
        return key_file.read()

if __name__ == "__main__":
    generate_key()  # Run this script to generate the key
