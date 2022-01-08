# AUTHOR - rajkaran
# YEAR - 2022 ;)

# External module
import psycopg2
from psycopg2 import sql
from tabulate import tabulate

# internal module
from config import config

class PasswordManager:

    def __init__(self):
        self.user = input("Enter your user name: ")
        try:
            # Getting parameters from config file
            params = config()
            
            # Connecting to database
            self.connection = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def menu(self) -> None:
        """ To print the usable command (menu) """
        print("\n------------Menu------------")
        print("\n1. To add a new password.")
        print("2. To read your password.")
        print("3. To update your password.")
        print("4. To delete your password.")
        print("5. Exit.\n")

    def insert(self, user_name, email, password, website) -> bool:
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
        except Exception as e:
            print(e)
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

    def get_data(self):
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

    def print_password(self) -> bool:
        print(tabulate(self.get_data(), headers=["ID", "UserName", "email", "Password", "Website"]))

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
    print(">>Type the number of the command to execute that command!\n")
    while True:
        try:
            command = input("command-$ ")

            match command:
                case "5" | "exit":
                    print("\n>>Have a nice day!\n")
                    break
                case "1":
                    user_name = input("Enter your user name: ")
                    email = input("Enter your email: ")
                    password = input("Enter your password: ")
                    website = input("Enter name of website: ")

                    if manager.insert(user_name, email, password, website):
                        print("\n>>Data successfully added to database!\n")
                    else:
                        print("\n>>Something went wrong!")

                case "2":
                    print("\n>>Your data!\n")
                    manager.print_password()

                case "3":
                    print("\n>>Data updated successfully\n")

                case "4":
                    manager.print_password()
                    try:
                        ID = int(input("\nEnter ID of the password which you want to delete: "))
                        if manager.delete(ID):
                            print("\n>>Data deleted successfully")
                        else:
                            print("\n>>Something went wrong!")
                    except Exception as e:
                        print("\n>>Only Enter ID of the password!\n")

                case "help":
                    manager.menu()

        except Exception as e:
            print("Something went wrong", e)

if __name__ == "__main__":
    main()
