# AUTHOR - rajkaran
# YEAR - 2022 ;)

# External module
import psycopg2
from psycopg2 import sql
from tabulate import tabulate

# Internal module
from config import config
import random
import subprocess
import platform
import hashlib

from user import User
from crypto import Cryptography 

class PasswordManager:

    def __init__(self):
        self.user = input("Enter your user name: ")
        self.master_passwd = hashlib.sha384(input("Enter the master password: ").encode()).hexdigest()
        self.key = self.master_passwd[41:-50]
        self.user_present = False
        self.crypto = Cryptography()

        # Getting parameters from config file
        params = config()
        params['password'] = self.crypto.Decrypt(params['password'], self.key)

        try:
            # Connecting to database
            self.connection = psycopg2.connect(**params)


        except (Exception, psycopg2.DatabaseError) as error:
            pass
        
        try:
            user = User()
            all_user = user.get_user(self.connection)

            if self.user in all_user:
                self.user_present = True
        except:
            print("Something went Wrong")

    def menu(self) -> None:
        """ To print the usable command (menu) """
        print("\n------------Menu------------")
        print("\n1. To add a new password.")
        print("2. To read your password.")
        print("3. To update your password.")
        print("4. To delete your password.")
        print("Enter 'e' or 'exit' to exit.\n")

    def insert(self, user_name, email, password, website) -> bool:
        password = self.crypto.Encrypt(password, self.key)
        """ Function to insert password details into database """
        psql_insert_command = """INSERT INTO {} (user_name, email, password, website)
                                 VALUES (%s, %s, %s, %s);
                              """
        psql_table_create_command = """CREATE TABLE {} (
                                        id BIGSERIAL PRIMARY KEY,
                                        user_name VARCHAR(50),
                                        email VARCHAR(100),
                                        password VARCHAR(100) NOT NULL,
                                        website VARCHAR(100) NOT NULL
                                        ); 
                                    """
        cur = self.connection.cursor()
        try:
            if self.table_exits(self.user):
                cur.execute(sql.SQL(psql_insert_command).format(sql.Identifier(self.user)), [user_name, email, password, website])
            else:
                cur.execute(sql.SQL(psql_table_create_command).format(sql.Identifier(self.user)))
                cur.execute(sql.SQL(psql_insert_command).format(sql.Identifier(self.user)), [user_name, email, password, website])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

        self.connection.commit()
        cur.close()
        return True


    def table_exits(self, tableName) -> bool:
        """ Function to check if table exits in database or not """
        psql_command = "SELECT * FROM information_schema.tables WHERE table_name=%s"
        cur = self.connection.cursor()
        cur.execute(psql_command, (tableName,))
        cur.close()
        return bool(cur.rowcount)

    def get_data(self) -> list:
        """ Function to get data from the database """
        psql_command = "SELECT * FROM {};"
        data = []

        try:
            cur = self.connection.cursor()
            cur.execute(sql.SQL(psql_command).format(sql.Identifier(self.user)))
            row = cur.fetchone()

            for _ in range(cur.rowcount):
                data.append(list(row))
                row = cur.fetchone()

            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        for j in range(len(data)):
            data[j][3] = self.crypto.Decrypt(data[j][3], self.key)

        return data

    def delete(self, ID) -> bool:
        """ Function to delete row (password) from database """
        psql_delete_command = "DELETE FROM {} WHERE id = %s"
        try:
            cur = self.connection.cursor()
            cur.execute(sql.SQL(psql_delete_command).format(sql.Identifier(self.user)), [ID])
            self.connection.commit()
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        return True

    def update(self, ID, password) -> bool:
        password = self.crypto.Encrypt(password, self.key)
        """ Function to update password in database """
        psql_update_command = """UPDATE {}
                                SET password = %s
                                WHERE id = %s
        """
        try:
            cur = self.connection.cursor()
            cur.execute(sql.SQL(psql_update_command).format(sql.Identifier(self.user)), [password, ID])
            self.connection.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        return True

    def print_password(self) -> bool:
        print(tabulate(self.get_data(), headers=["ID", "UserName", "email", "Password", "Website"]))
        print("\n\n")

# Function  to generate random password
def generate_random_password(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&amp;*1234567890"
    password = ""
    for _ in range(length + 1):
        password += random.choice(characters)
    return password

# python program to copy password to clipboard
def copy2clip(txt):
    if platform.system() == 'Windows':
        cmd='echo ' + txt.strip() + '| clip'
    elif platform.system() == 'Darwin':
        cmd='echo ' + txt.strip() + '| pbcopy'
    
    return subprocess.check_call(cmd, shell=True)

# Main function (Execution start from here)
def main():
    global manager
    manager = PasswordManager()
    print("""
            #########################################
            #                                       #
            #       Matrix Password Manager         #
            #                                       #
            #########################################
    """)
    if manager.user_present:
        manager.menu()
        print(">>Type the number of the command to execute that command!\n")
        while True:
            try:
                command = input("command-$ ")

                match command:
                    case "e" | "exit":
                        print("\n>>Have a nice day!\n")
                        break
                    case "1":
                        to_generate_passwd = input("Do you want to generate random password (Y/n): ")
                        if to_generate_passwd.lower() == "y":
                            length = int(input("Enter the length of the password: "))
                            user_name = input("Enter your user name: ")
                            email = input("Enter your email: ")
                            password = generate_random_password(length)
                            website = input("Enter name of website: ")
                        else:
                            user_name = input("Enter your user name: ")
                            email = input("Enter your email: ")
                            password = input("Enter your password: ")
                            website = input("Enter name of website: ")

                        should_save = input("Please cross check your details, Should we push your details to database (Y/n): ")
                        
                        if should_save.lower() == "y":
                            if manager.insert(user_name, email, password, website):
                                print("\n>>Data successfully added to database!\n")
                            else:
                                print("\n>>Something went wrong!")

                    case "2":
                        print("\n>>Your data!\n")
                        manager.print_password()

                    case "3":
                        manager.print_password()
                        ID = int(input(">>Enter ID of password which you want to update: "))
                        password = input("Now Enter the password: ")
                        if manager.update(ID, password):
                            print("\n>>Data updated successfully\n")
                        else:
                            print("\n>>Something went wrong!")

                    case "4":
                        manager.print_password()
                        try:
                            ID = int(input("\nEnter ID of the password which you want to delete: "))
                            if manager.delete(ID):
                                print("\n>>Data deleted successfully")
                            else:
                                print("\n>>Something went wrong!")
                        except:
                            print("\n>>Only Enter ID of the password!\n")

                    case "help":
                        manager.menu()

            except Exception as e:
                print("Something went wrong", e)

if __name__ == "__main__":
    main()
