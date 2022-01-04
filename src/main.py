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

def main():
    print("""
            #########################################
            #                                       #
            #       Matrix Password Manager         #
            #                                       #
            #########################################
            """)

    while True:
        commandEntered = input("command-$ ")

        if commandEntered.lower() == "e" or commandEntered.lower() == "exit":
            print("\n[MESSAGE] - Have a nice day!\n")
            break
        elif commandEntered.lower() == "n":
            print("\n[MESSAGE] - Data successfully added to database!\n")
        elif commandEntered.lower() == "g":
            print("\n[MESSAGE] - Your data!\n")
        elif commandEntered.lower() == "u":
            print("\n[MESSAGE] - Data updated successfully\n")

if __name__ == "__main__":
    main()
