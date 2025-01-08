from login import setup_login_gui
from gui import setup_gui


def main():
    # Start the login GUI
    login_successful = setup_login_gui()  # This will return True if login is successful

    if login_successful:  # Proceed only if login was successful
        app = setup_gui()  # Initialize the main GUI from gui.py
        app.mainloop()
    else:
        print("Login failed or cancelled. Exiting application.")


if __name__ == "__main__":
    main()
