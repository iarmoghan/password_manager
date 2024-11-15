# Password Manager

## Overview
This is a Password Manager application designed to securely manage users' passwords. The app enables users to store, view, update, and delete passwords for various services. It uses cryptographic techniques such as hashing and encryption to protect users' data.

## Features
- **User Registration**: Allows users to create a secure account with password hashing.
- **User Login**: Authenticates users via hashed passwords.
- **Password Management**: Securely stores, retrieves, updates, and deletes passwords for services.
- **Encryption**: Uses AES encryption to protect passwords stored for various services.
- **Password Hashing**: Uses bcrypt for securely storing user passwords.

## Requirements
- Python 3.6+
- Required Python libraries:
  - Tkinter (for GUI)
  - sqlite3 (for database)
  - bcrypt (for password hashing)
  - cryptography (for encryption)

