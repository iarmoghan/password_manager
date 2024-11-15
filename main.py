import sqlite3
import tkinter as tk
from tkinter import messagebox
from utils.hashing import hash_password, verify_password
from utils.encryption import encrypt_password, decrypt_password
from utils.db_setup import initialize_db  # Import the database initialization function

# Initialize the database (Create tables if they don't exist)
initialize_db()

# Function to register a new user
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    password_hash = hash_password(password)  # Hash the password before saving

    # Insert the new user into the users table
    connection = sqlite3.connect('db/passwords.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        ''', (username, password_hash))
        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        connection.close()

# Function to login an existing user
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    # Fetch the stored password hash for the given username
    connection = sqlite3.connect('db/passwords.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT password_hash FROM users WHERE username = ?
    ''', (username,))
    stored_hash = cursor.fetchone()
    connection.close()

    if stored_hash and verify_password(password, stored_hash[0]):
        messagebox.showinfo("Success", "Login successful!")
        show_password_manager(username)  # Open the password manager after successful login
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to display the password manager interface
def show_password_manager(username):
    def save_password():
        service_name = entry_service.get()
        password = entry_service_password.get()
        encrypted_password = encrypt_password(password)  # Encrypt the password

        # Insert the encrypted password into the passwords table
        connection = sqlite3.connect('db/passwords.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO passwords (user_id, service_name, encrypted_password)
            VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)
        ''', (username, service_name, encrypted_password))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Password saved successfully!")

    def view_passwords():
        # Display the saved passwords
        connection = sqlite3.connect('db/passwords.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT service_name, encrypted_password FROM passwords
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
        ''', (username,))
        passwords = cursor.fetchall()
        connection.close()

        if passwords:
            listbox_passwords.delete(0, tk.END)  # Clear existing listbox entries
            for service, enc_password in passwords:
                decrypted_password = decrypt_password(enc_password)  # Decrypt the password
                listbox_passwords.insert(tk.END, f"{service}: {decrypted_password}")
        else:
            messagebox.showinfo("No passwords", "No passwords saved for this user.")

    def delete_password():
        service_name = entry_service.get()
        if not service_name:
            messagebox.showerror("Error", "Please provide a valid service name to delete.")
            return

        # Delete the selected password from the database
        connection = sqlite3.connect('db/passwords.db')
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM passwords WHERE user_id = (SELECT id FROM users WHERE username = ?)
            AND service_name = ?
        ''', (username, service_name))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", f"Password for {service_name} deleted successfully!")

        # Refresh the list of saved passwords
        listbox_passwords.delete(0, tk.END)
        view_passwords()

    def update_password():
        service_name = entry_service.get()
        new_password = entry_service_password.get()
        if not service_name or not new_password:
            messagebox.showerror("Error", "Please provide a valid service name and password to update.")
            return

        encrypted_password = encrypt_password(new_password)  # Encrypt the new password

        # Update the password in the database
        connection = sqlite3.connect('db/passwords.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE passwords SET encrypted_password = ?
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
            AND service_name = ?
        ''', (encrypted_password, username, service_name))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", f"Password for {service_name} updated successfully!")

        # Refresh the list of saved passwords
        listbox_passwords.delete(0, tk.END)
        view_passwords()

    # Hide the login form and display the password manager
    login_frame.pack_forget()
    password_manager_frame.pack(pady=10)

    button_save_password.config(command=save_password)
    button_view_passwords.config(command=view_passwords)
    button_delete_password.config(command=delete_password)
    button_update_password.config(command=update_password)

    # Add a Log Out button to go back to login
    button_log_out = tk.Button(password_manager_frame, text="Log Out", command=log_out)
    button_log_out.grid(row=6, column=0, pady=10, sticky="ew")  # Ensure it's placed in a new row and stretches across

# Log Out function to return to login
def log_out():
    # Hide the password manager frame
    password_manager_frame.pack_forget()
    
    # Show the login frame again
    login_frame.pack(pady=20)

# Exit function to close the app or go back
def exit_app():
    root.quit()  # Closes the window and exits the application

# Set up the main window
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x500")

# Initialize the login form
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

label_username = tk.Label(login_frame, text="Username:")
label_username.grid(row=0, column=0)
entry_username = tk.Entry(login_frame)
entry_username.grid(row=0, column=1)

label_password = tk.Label(login_frame, text="Password:")
label_password.grid(row=1, column=0)
entry_password = tk.Entry(login_frame, show="*")
entry_password.grid(row=1, column=1)

button_login = tk.Button(login_frame, text="Login", command=login_user)
button_login.grid(row=2, columnspan=2, pady=10)

button_register = tk.Button(login_frame, text="Register", command=register_user)
button_register.grid(row=3, columnspan=2)

# Exit Button on Login Form
button_exit = tk.Button(login_frame, text="Exit", command=exit_app)
button_exit.grid(row=4, columnspan=2)

# Initialize the password manager form
password_manager_frame = tk.Frame(root)

label_service = tk.Label(password_manager_frame, text="Service Name:")
label_service.grid(row=0, column=0)
entry_service = tk.Entry(password_manager_frame)
entry_service.grid(row=0, column=1)

label_service_password = tk.Label(password_manager_frame, text="Password:")
label_service_password.grid(row=1, column=0)
entry_service_password = tk.Entry(password_manager_frame, show="*")
entry_service_password.grid(row=1, column=1)

button_save_password = tk.Button(password_manager_frame, text="Save Password")
button_save_password.grid(row=2, columnspan=2, pady=10)

button_view_passwords = tk.Button(password_manager_frame, text="View Saved Passwords")
button_view_passwords.grid(row=3, columnspan=2)

button_delete_password = tk.Button(password_manager_frame, text="Delete Password")
button_delete_password.grid(row=4, columnspan=2)

button_update_password = tk.Button(password_manager_frame, text="Update Password")
button_update_password.grid(row=5, columnspan=2)

listbox_passwords = tk.Listbox(password_manager_frame, width=50, height=10)
listbox_passwords.grid(row=6, columnspan=2)

# Start the GUI loop
root.mainloop()
