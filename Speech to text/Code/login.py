from importer import customtkinter as ctk
import mysql.connector
import bcrypt

# MySQL configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "user_db",
}

# Create a connection to MySQL
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Create users table if it doesn't exist
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Save user credentials to the database
def save_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username already exists

# Validate user credentials during login
def validate_credentials(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def setup_signup_gui():
    """Create the signup GUI interface."""
    signup_root = ctk.CTk()
    signup_root.title("Signup")
    signup_root.geometry("1000x1000")

    # Flag to track signup success
    signup_successful = [False]  # Using a mutable type to modify in nested functions

    # Main frame
    frame = ctk.CTkFrame(signup_root, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title label
    ctk.CTkLabel(
        frame, text="User Signup", font=("Arial", 20)
    ).pack(pady=20)

    # Username label and entry
    ctk.CTkLabel(
        frame, text="Username:", font=("Arial", 14)
    ).pack(anchor="w", padx=20)
    username_entry = ctk.CTkEntry(frame, width=250)
    username_entry.pack(pady=10)

    # Password label and entry
    ctk.CTkLabel(
        frame, text="Password:", font=("Arial", 14)
    ).pack(anchor="w", padx=20)
    password_entry = ctk.CTkEntry(frame, show="*", width=250)
    password_entry.pack(pady=10)

    # Label to display messages
    message_label = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color="red")
    message_label.pack(pady=10)

    # Signup button
    def handle_signup():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            if save_user(username, password):
                signup_successful[0] = True  # Mark signup as successful
                message_label.configure(text="Signup successful!", text_color="green")
                lets_start_button.pack(pady=10)
            else:
                message_label.configure(text="Username already exists.", text_color="red")
        else:
            message_label.configure(text="Both fields are required.", text_color="red")

    signup_button = ctk.CTkButton(
        frame, text="Signup", command=handle_signup
    )
    signup_button.pack(pady=10)

    # Back button
    def go_back():
        signup_root.destroy()
        setup_login_gui()

    back_button = ctk.CTkButton(
        frame, text="Back", command=go_back
    )
    back_button.pack(pady=10)

    # Let's Start button
    def lets_start():
        signup_root.destroy()

    lets_start_button = ctk.CTkButton(
        frame, text="Let's Start", command=lets_start
    )
    lets_start_button.pack_forget()  # Initially hidden

    signup_root.mainloop()
    return signup_successful[0]

def setup_login_gui():
    """Create the login GUI interface."""
    login_root = ctk.CTk()
    login_root.title("Login")
    login_root.geometry("1000x1000")

    # Authentication status flag
    authenticated = [False]  # Using a mutable type to modify in nested functions

    # Main frame
    frame = ctk.CTkFrame(login_root, corner_radius=15)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title label
    ctk.CTkLabel(
        frame, text="User Login", font=("Arial", 20)
    ).pack(pady=20)

    # Username label and entry
    ctk.CTkLabel(
        frame, text="Username:", font=("Arial", 14)
    ).pack(anchor="w", padx=550)
    username_entry = ctk.CTkEntry(frame, width=250)
    username_entry.pack(pady=10)

    # Password label and entry
    ctk.CTkLabel(
        frame, text="Password:", font=("Arial", 14)
    ).pack(anchor="w", padx=550)
    password_entry = ctk.CTkEntry(frame, show="*", width=250)
    password_entry.pack(pady=10)

    # Login button
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_credentials(username, password):
            authenticated[0] = True  # Set authentication status to True
            login_root.destroy()  # Close login window on success
        else:
            ctk.CTkLabel(
                frame, text="Invalid credentials. Try again.", text_color="red"
            ).pack(pady=5)

    login_button = ctk.CTkButton(
        frame, text="Login", command=handle_login
    )
    login_button.pack(pady=10)

    # Signup redirect button
    def open_signup():
        login_root.destroy()
        signup_gui = setup_signup_gui()
        if signup_gui:  # Check if signup was successful
            authenticated[0] = True

    signup_button = ctk.CTkButton(
        frame, text="Signup", command=open_signup
    )
    signup_button.pack(pady=10)

    # Run the GUI and return authentication status
    login_root.mainloop()
    return authenticated[0]

if __name__ == "__main__":
    initialize_database()  # Ensure database is set up
    login_gui = setup_login_gui()
    login_gui.mainloop()