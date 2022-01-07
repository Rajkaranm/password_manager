import psycopg2
from config import config
from tabulate import tabulate


class PasswordManager:

    def __init__(self):
        try:
            # Getting parameters from config file
            params = config()
            
            # Connecting to database
            self.connection = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def menu(self) -> None:
        """ To print the usable command (menu) """
        print("\n1. To add a new password.")
        print("2. To read your password.")
        print("3. To update your password.")
        print("4. Exit.\n")


def main():
    manager = PasswordManager()
    print("""
            #########################################
            #                                       #
            #       Matrix Password Manager         #
            #                                       #
            #########################################
            """)
    manager.menu()
    print("Type the number of the command to execute that command!")
    while True:
        command = input("command-$ ")

        if command.lower() == "4" or command.lower() == "exit":
            print("\n[MESSAGE] - Have a nice day!\n")
            break
        elif command.lower() == "1":
            print("\n[MESSAGE] - Data successfully added to database!\n")
        elif command.lower() == "2":
            print("\n[MESSAGE] - Your data!\n")
        elif command.lower() == "3":
            print("\n[MESSAGE] - Data updated successfully\n")
        elif command.lower() == "help":
            manager.menu()

if __name__ == "__main__":
    main()
