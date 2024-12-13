from gui import *
import pandas as pd
import os

def setup() -> None:
    """
    Establishes the login csv if it doesn't already exist.
    """
    if os.path.exists('login.csv'):
        print('login file is present')
    else:
        print('New login file made')
        df = pd.DataFrame({'Users': [], 'Passwords': []})
        df.to_csv('login.csv')


def main():
    """
    Does the Qt application stuff
    """
    application = QApplication([])  # Initializes the Qt application
    window = MainWindow()  # Creates an instance of MainWindow
    window.show()  # Displays the main window
    application.exec()  # Starts the application's event loop


if __name__ == '__main__':
    setup()  # Sets up the login csv
    main()  # Runs the main application
    
