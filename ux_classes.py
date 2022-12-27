from user_specific import Root, User
import hashlib
import sys


class Secure:
    @staticmethod
    def hashpassword(passwd):
        for i in range(2):  # Двойной хеш + соль
            passwd = f"{passwd}VpiNCAruHfkbPNXYus6F2up1Y0OV8pEN"
            passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        return passwd

    @staticmethod
    def infile_change(filename, old_string, new_string):
        with open(filename) as file:
            contents = file.read()
            if old_string not in contents:
                sys.exit(1)

        with open(filename, 'w') as f:
            # print("Changed!")
            contents = contents.replace(old_string, new_string)
            f.write(contents)

    @staticmethod
    def check_username_and_password(username, password):
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                account = i.strip("\n").split(",")
                if (username in account) and (password in account) and ("0" in account):
                    Root(username, password).display_info()
                elif (username in account) and (password in account):
                    User(username, password).display_info()

    @staticmethod
    def check_for_commas(username):
        if "," in username:
            print("Oops, you have ',' in username.")
            sys.exit(1)

    @staticmethod
    def is_user_exists(username):
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                account = i.strip("\n").split(",")
                if username in account:
                    print("User exists!")
                    sys.exit(1)

    @staticmethod
    def check_password(username, password):
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                linestr = i.strip("\n").split(",")
                if username not in linestr:
                    pass
                elif (username in linestr) and (password in linestr):
                    print("OK.")
                else:
                    print("Wrong password.")
                    sys.exit(1)

    @staticmethod
    def check_is_database_empty():
        try:
            with open('private/users.conf'):
                import os
                if os.path.getsize('private/users.conf') == 0:
                    print("Database is empty.")
                    print("Now new admin user will be created...")
                    Root.create_new_user(emptydb=True)
        except FileNotFoundError:
            import os
            print("Script will create DB. Run app again.")
            if os.name == 'nt':
                os.system("mkdir private")
                os.system("cd private && type nul > users.conf")
                sys.exit(0)
            elif os.name == "posix":
                os.system("mkdir private && cd private && touch users.conf")
                sys.exit(0)
