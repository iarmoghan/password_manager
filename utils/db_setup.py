import sqlite3

# Initialize the SQLite database
def initialize_db():
    # Connect to the database (creates it if it doesn't exist)
    connection = sqlite3.connect('db/passwords.db')
    cursor = connection.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create the passwords table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print("Database initialized successfully!")

# Run the function when the script is executed
if __name__ == "__main__":
    initialize_db()
