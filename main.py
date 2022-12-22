import getpass
from ux_classes import Secure

if __name__ == '__main__':
    Secure().check_is_database_empty()
    username = input("Enter username: ")
    password = Secure().hashpassword(getpass.getpass("Enter password: "))
    Secure().check_username_and_password(username, password)
