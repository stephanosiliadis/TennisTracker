"""
@author: Stefanos Iliadis
"""

import sqlite3
from tkinter import messagebox


class Register(object):
    """
    Creates a Database(username, email, password with that order)
    for the users and registers the user to the database if all requirements are True
    """

    def __init__(self, users_db: str = "localhost.db", table: str = "users"):
        self.users_db = users_db
        self.table = table

        self.conn = sqlite3.connect(self.users_db)
        self.c = self.conn.cursor()

        self.c.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table} (
            username text NOT NULL,
            email text NOT NULL,
            password text NOT NULL
        )"""
        )

        self.conn.commit()
        self.conn.close()

    def register_user(self, user_data: list) -> bool:
        self.user_data = user_data

        self.conn = sqlite3.connect(self.users_db)
        self.conn.row_factory = lambda cursor, row: row[0]
        self.c = self.conn.cursor()

        self.c.execute(f"SELECT username FROM {self.table}")
        usernames = self.c.fetchall()

        self.c.execute(f"SELECT password FROM {self.table}")
        passwords = self.c.fetchall()

        email = user_data[1]
        valid_email = "@" in email and "." in email

        complete_inputs = (
            user_data[0] != "" and user_data[1] != "" and user_data[2] != ""
        )

        valid_inputs = len(user_data[0]) >= 3 and len(user_data[2]) >= 3

        username_used = user_data[0] in usernames

        if not complete_inputs:
            messagebox.showerror(
                "Invalid username or password",
                "One or more entries are blank, make sure to fill in all the required fields",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif not valid_inputs:
            messagebox.showerror(
                "Invalid username and password",
                "Username and password must be more than 3 characters",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif not valid_email:
            messagebox.showerror(
                "Invalid email",
                "Please enter a valid email address including the @ sign and .youremailservice",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif username_used:
            messagebox.showerror(
                "Invalid username",
                "The username you provided are already in use by another user",
            )
            self.conn.commit()
            self.conn.close()
            return False

        else:
            messagebox.showinfo(
                "Successful Registration",
                f"{user_data[0]}, your account has been created",
            )
            self.conn.execute(
                f"INSERT INTO {self.table} VALUES (?, ?, ?)", self.user_data
            )
            self.conn.commit()
            self.conn.close()
            return True


class Login(object):
    def __init__(self, users_db: str = "localhost.db", table: str = "users"):
        self.users_db = users_db
        self.table = table

        self.conn = sqlite3.connect(self.users_db)
        self.c = self.conn.cursor()

        self.conn.commit()
        self.conn.close()

    def login_user(self, user_data: list) -> bool:
        self.user_data = user_data

        self.conn = sqlite3.connect(self.users_db)
        self.conn.row_factory = lambda cursor, row: row[0]
        self.c = self.conn.cursor()

        self.c.execute(f"SELECT username FROM {self.table}")
        usernames = self.c.fetchall()

        self.c.execute(f"SELECT password FROM {self.table}")
        passwords = self.c.fetchall()

        username = self.user_data[0]
        password = self.user_data[1]

        complete_inputs = username != "" and password != ""

        user_found = username in usernames and password in passwords

        if not complete_inputs:
            messagebox.showerror(
                "Invalid username or password",
                "One or more entries are blank, make sure to fill in all the required fields",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif not user_found:
            messagebox.showerror(
                "Invalid username and password",
                "There is no user with that username and password",
            )
            self.conn.commit()
            self.conn.close()
            return False

        else:
            self.conn.commit()
            self.conn.close()
            return True

    def update_password(
        self, username: str, new_password: str, passowrd_repeated: str
    ) -> bool:
        self.conn = sqlite3.connect(self.users_db)
        self.c = self.conn.cursor()

        complete_inputs = new_password != ""
        valid_inputs = len(new_password) >= 3
        same_inputs = new_password == passowrd_repeated

        if not complete_inputs:
            messagebox.showerror(
                "Invalid username or password",
                "One or more entries are blank, make sure to fill in all the required fields",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif not valid_inputs:
            messagebox.showerror(
                "Invalid username and password",
                "Username and password must be more than 3 characters",
            )
            self.conn.commit()
            self.conn.close()
            return False

        elif not same_inputs:
            messagebox.showerror(
                "Invalid password confirmation",
                "Please confirm password correctly",
            )
            self.conn.commit()
            self.conn.close()
            return False

        else:
            self.c.execute(
                f"UPDATE {self.table} SET password = ? WHERE username = ?",
                (new_password, username),
            )
            messagebox.showinfo(
                "Password Updated", f"Your new password is {new_password}"
            )
            self.conn.commit()
            self.conn.close()
