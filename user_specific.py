import sys
import getpass

uid = 0


class Root:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    @staticmethod
    def display_notes():
        import os
        try:
            with open('notes.txt', 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print("Oops. 'notes.txt' did't created. Creating file...")
            os.system("touch notes.txt")

    @staticmethod
    def display_userinfo():
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                if "0," in i:
                    rootlist = i.strip("\n").split(",")
                    print(f'Account type - Root. Username: "{rootlist[1]}". Hashed Password: "{rootlist[2]}"')

    @staticmethod
    def display_whole_db():
        with open('private/users.conf', 'r') as file:
            print(file.read())

    @staticmethod
    def root_change_user_credentials():
        from ux_classes import Secure
        oldusername = input("Enter old username: ")
        newusername = input("Enter new username: ")
        Secure().is_user_exists(newusername)
        Secure().check_for_commas(newusername)
        newpassword = Secure().hashpassword(getpass.getpass("Enter new password: "))
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                if oldusername in i:
                    original_list = i.strip("\n").split(",")
                    newlist = i.strip("\n").split(",")
                    newlist[1] = newusername
                    newlist[2] = newpassword
                    original_list = ",".join(original_list)
                    newlist = ",".join(newlist)
                    Secure().infile_change("private/users.conf", original_list, newlist)

    @staticmethod
    def root_change_password(username):
        from ux_classes import Secure
        newpassword = Secure().hashpassword(getpass.getpass("Enter new password: "))
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                if username in i:
                    original_list = i.strip("\n").split(",")
                    newlist = i.strip("\n").split(",")
                    newlist[2] = newpassword
                    original_list = ",".join(original_list)
                    newlist = ",".join(newlist)
                    Secure().infile_change("private/users.conf", original_list, newlist)

    @staticmethod
    def create_new_user(emptydb=False):
        global uid
        from ux_classes import Secure
        user_username = input("Enter username: ")
        Secure().is_user_exists(user_username)
        Secure().check_for_commas(user_username)
        user_password = Secure().hashpassword(getpass.getpass("Enter password: "))
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                uid += 1
        if emptydb:
            with open('private/users.conf', 'w') as file:
                file.write(f"{uid},{user_username},{user_password}")
        else:
            with open('private/users.conf', 'a') as file:
                file.write(f"\n{uid},{user_username},{user_password}")

    def check_answer(self, answer):
        if answer == "0":
            sys.exit(0)
        elif answer == "1":
            self.root_change_user_credentials()
        elif answer == "2":
            self.display_whole_db()
        elif answer == "3":
            self.display_userinfo()
        elif answer == "4":
            self.display_notes()
        elif answer == "5":
            self.create_new_user()
        elif answer == "6":
            username = input("Enter username: ")
            self.root_change_password(username)

    def display_info(self):
        print("Hello, Admin. What you would like to do?")
        print("""
0 - exit
1 - change user credentials
2 - display whole db
3 - display my userinfo
4 - display notes (notes.txt)
5 - create new user
6 - change user password""")
        answer = input("> ")
        self.check_answer(answer)


class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def change_user_credentials(self):
        from ux_classes import Secure
        oldusername = input("Enter your old (current) username: ")
        if oldusername != self.username:
            sys.exit(1)
        newusername = input("Enter your new username: ")
        Secure().is_user_exists(newusername)
        Secure().check_for_commas(newusername)
        oldpassword = Secure().hashpassword(getpass.getpass("Enter your old password: "))
        newpassword = Secure().hashpassword(getpass.getpass("Enter your new password: "))
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                listcont = i.strip("\n").split(",")
                if oldusername and oldpassword in listcont:
                    original_list = ",".join(listcont)
                    new_list = listcont[:]
                    new_list[1] = newusername
                    new_list[2] = newpassword
                    new_list = ",".join(new_list)
                    Secure().infile_change('private/users.conf', original_list, new_list)

    @staticmethod
    def display_my_userinfo(username, password):
        print(f"Account type - Normal. Username: {username}. Password: {password}")

    def change_my_password(self, username):
        from ux_classes import Secure
        if username != self.username:
            sys.exit(1)
        oldpassword = Secure().hashpassword(getpass.getpass("Enter old password: "))
        Secure().check_password(username, oldpassword)
        newpassword = Secure().hashpassword(getpass.getpass("Enter new password: "))
        with open('private/users.conf', 'r') as file:
            filecont = file.readlines()
            for i in filecont:
                if username in i:
                    original_list = i.strip("\n").split(",")
                    newlist = i.strip("\n").split(",")
                    newlist[2] = newpassword
                    original_list = ",".join(original_list)
                    newlist = ",".join(newlist)
                    Secure().infile_change("private/users.conf", original_list, newlist)

    def check_answer(self, answer):
        if answer == "0":
            sys.exit(0)
        elif answer == "1":
            self.change_user_credentials()
        elif answer == "2":
            self.display_my_userinfo(self.username, self.hashed_password)
        elif answer == "3":
            self.change_my_password(self.username)

    def display_info(self):
        print("""
0 - exit
1 - change my account credentials
2 - display my account info
3 - change account password""")
        answer = input("> ")
        self.check_answer(answer)
