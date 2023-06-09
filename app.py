from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import datetime
import sys, os

from application.authentication import Register, Login
from application.components import navbar


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Root Settings:
root = Tk()
root.title("Tennis Tracker | Login")
root.iconbitmap(resource_path("static\\tennisappicon.ico"))
x = (root.winfo_screenwidth() // 2) - 250
y = int(root.winfo_screenheight() * 0.1) - 50
root.geometry("500x720+" + str(x) + "+" + str(y))
root.resizable(False, False)

# Create DataBase Connection and Cursor:
conn = sqlite3.connect(resource_path("data\\tennis_stats.db"))
c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS users (
 username text NOT NULL,
 email text NOT NULL,
 password text NOT NULL
 )"""
)

c.execute(
    """CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username text NOT NULL,
        date TEXT,
        aspect TEXT,
        description TEXT,
        completed INTEGER,
        FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
 )"""
)


# Functions:
def home_callback():
    add_record_frame.grid_forget()
    base_frame.grid(row=0, column=0)


def add_callback():
    base_frame.grid_forget()
    add_record_frame.grid(row=0, column=0)


def profile_callback():
    conn = sqlite3.connect(resource_path("data\\tennis_stats.db"))
    c = conn.cursor()
    username = get_username(base_frame)
    user = [
        (username),
    ]

    c.execute("SELECT * FROM users WHERE username = ?", user)
    user_data = c.fetchall()
    c.execute("SELECT * FROM stats WHERE username = ?", user)
    records = c.fetchall()

    c.execute("SELECT completed FROM stats WHERE username = ? AND completed = 0", user)
    incomplete_records = len(c.fetchall())

    c.execute("SELECT completed FROM stats WHERE username = ? AND completed = 1", user)
    complete_records = len(c.fetchall())

    profile = Tk()
    if username[-1] == "s":
        title = f"{username}' Profile"
    else:
        title = f"{username}'s Profile"
    profile.title(title)
    profile.iconbitmap(resource_path("static\\tennisappicon.ico"))
    x = (profile.winfo_screenwidth() // 2) - 250
    y = int(profile.winfo_screenheight() * 0.1) - 50
    profile.geometry("500x500+" + str(x) + "+" + str(y))
    profile.resizable(False, False)

    profile_frame = Frame(
        master=profile,
        width=500,
        height=500,
        bg="#77DD77",
    )
    profile_frame.grid(row=0, column=0)

    profile_data_frame = Frame(
        master=profile_frame,
        width=450,
        height=450,
        bg="#66C166",
        highlightthickness=3,
        highlightbackground="#fdfd96",
    )
    profile_data_frame.place(relx=0.05, rely=0.05)

    username_label_profile = Label(
        master=profile_data_frame,
        text=f"Username: {username}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.1)

    password_label_profile = Label(
        master=profile_data_frame,
        text=f"Password: {user_data[0][2]}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.25)

    email_label_profile = Label(
        master=profile_data_frame,
        text=f"Email: {user_data[0][1]}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.4)

    records_label_profile = Label(
        master=profile_data_frame,
        text=f"Total Records: {len(records)}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.55)

    complete_records_label_profile = Label(
        master=profile_data_frame,
        text=f"Complete Records: {complete_records}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.7)

    incomplete_records_label_profile = Label(
        master=profile_data_frame,
        text=f"Incomplete Records: {incomplete_records}",
        font=("Arial", 15, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.2, rely=0.85)

    conn.commit()
    conn.close()


def logout_callback():
    msg = messagebox.askokcancel("Tennis Tracker", "Do you want to log out?")
    if msg == True:
        base_frame.grid_forget()
        user_label.destroy()
        display_canvas.destroy()
        login_frame.grid(row=0, column=0)
        root.title("Tennis Tracker | Login")
    else:
        pass


def on_enter(event):
    event.widget["background"] = "#66C166"
    event.widget["foreground"] = "#FFB6C1"
    event.widget["font"] = ("Arial", 11, "bold", "underline")


def on_leave(event):
    event.widget["background"] = "#66C166"
    event.widget["foreground"] = "#fdfd96"
    event.widget["font"] = ("Arial", 11, "bold")


def change_password_callback():
    username = username_entry.get()
    password_new = new_password_entry.get()
    password_new_repeated = new_password_repeat_entry.get()

    admin = Login(users_db=resource_path("data\\tennis_stats.db"))
    password_updated = admin.update_password(
        username=username,
        new_password=password_new,
        passowrd_repeated=password_new_repeated,
    )

    if password_updated:
        new_password.destroy()

    else:
        new_password.focus()


def new_password_callback():
    global new_password, username_entry, new_password_entry, new_password_repeat_entry
    new_password = Tk()
    new_password.title("Tennis Tracker | New Password")
    new_password.iconbitmap(resource_path("static\\tennisappicon.ico"))
    x = (new_password.winfo_screenwidth() // 2) - 250
    y = int(new_password.winfo_screenheight() * 0.1) - 50
    new_password.geometry("500x500+" + str(x) + "+" + str(y))
    new_password.resizable(False, False)

    base_frame = Frame(
        master=new_password,
        width=500,
        height=500,
        bg="#77DD77",
    )
    base_frame.grid(row=0, column=0)

    # Add Widgets to the Base Frame:
    entry_frame = Frame(
        master=base_frame,
        width=450,
        height=450,
        bg="#66C166",
        highlightbackground="#fdfd96",
        highlightthickness=3,
    )
    entry_frame.place(relx=0.05, rely=0.05)

    username_label = Label(
        master=entry_frame,
        text="Username",
        font=("Arial", 11, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.1, rely=0.1)

    new_password_label = Label(
        master=entry_frame,
        text="New Password",
        font=("Arial", 11, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.1, rely=0.3)

    new_password_repeat_label = Label(
        master=entry_frame,
        text="Repeat Password",
        font=("Arial", 11, "bold"),
        bg="#66C166",
        fg="#fdfd96",
    ).place(relx=0.1, rely=0.5)

    username_entry = Entry(
        master=entry_frame,
        border=3,
        font=("Arial", 12, "bold"),
        fg="#fdfd96",
        bg="#77DD77",
    )
    username_entry.place(relx=0.15, rely=0.2)

    new_password_entry = Entry(
        master=entry_frame,
        border=3,
        font=("Arial", 12, "bold"),
        fg="#fdfd96",
        bg="#77DD77",
    )
    new_password_entry.place(relx=0.15, rely=0.4)

    new_password_repeat_entry = Entry(
        master=entry_frame,
        border=3,
        font=("Arial", 12, "bold"),
        fg="#fdfd96",
        bg="#77DD77",
    )
    new_password_repeat_entry.place(relx=0.15, rely=0.6)

    change_password_btn = Button(
        master=entry_frame,
        text="Change Password",
        fg="#fdfd96",
        bg="#66C166",
        border=3,
        width=20,
        command=change_password_callback,
    ).place(relx=0.3, rely=0.75)


def go_to_register():
    login_frame.grid_forget()
    register_frame.grid(row=0, column=0)
    root.title("Tennis Tracker | Registration")


def go_to_login():
    register_frame.grid_forget()
    login_frame.grid(row=0, column=0)
    root.title("Tennis Tracker | Login")


def login_callback():
    username = username_entry_login.get()
    password = password_entry_login.get()

    user = (username, password)

    admin = Login(users_db=resource_path("data\\tennis_stats.db"))
    logged = admin.login_user(user)

    if logged:
        username_entry_login.delete(0, END)
        password_entry_login.delete(0, END)
        login_frame.grid_forget()
        base_frame.grid(row=0, column=0)
        welcome_user(username)
        display_data()

    root.focus()


def register_callback():
    username = username_entry_register.get()
    email = email_entry_register.get()
    password = password_entry_register.get()

    user = (username, email, password)

    admin = Register(users_db=resource_path("data\\tennis_stats.db"))
    registration = admin.register_user(user)

    if registration:
        username_entry_register.delete(0, END)
        email_entry_register.delete(0, END)
        password_entry_register.delete(0, END)
        register_frame.grid_forget()
        base_frame.grid(row=0, column=0)
        welcome_user(username)
        display_data()

    root.focus()


def display_data():
    global display_canvas
    conn = sqlite3.connect(resource_path("data\\tennis_stats.db"))
    c = conn.cursor()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Custom.Vertical.TScrollbar",
        background="#66C166",
        troughcolor="#66C166",
        bordercolor="#66C166",
        arrowcolor="#fdfd96",
        gripcount=0,
    )
    style.map("Custom.Vertical.TScrollbar", background=[("active", "#fdfd96")])

    display_canvas = Canvas(
        master=base_frame,
        width=480,
        height=550,
        bg="#66C166",
        highlightbackground="#fdfd96",
        highlightthickness=3,
    )
    display_canvas.place(relx=0.02, rely=0.2)

    scrollbar = ttk.Scrollbar(
        master=base_frame,
        orient="vertical",
        command=display_canvas.yview,
        style="Custom.Vertical.TScrollbar",
    )
    scrollbar.place(relx=0.96, rely=0.2, height=550)

    display_canvas.configure(yscrollcommand=scrollbar.set)
    display_canvas.bind(
        "<Configure>",
        lambda e: display_canvas.configure(scrollregion=display_canvas.bbox("all")),
    )

    display_frame = Frame(
        master=display_canvas,
        bg="#66C166",
    )
    display_canvas.create_window((0, 0), window=display_frame, anchor="nw")

    display_date_label = Label(
        master=display_frame,
        text="Dates",
        font=("Arial", 11, "bold", "underline"),
        bg="#66C166",
        fg="#fdfd96",
    )
    display_date_label.grid(row=0, column=0, padx=10, pady=10)

    display_aspect_label = Label(
        master=display_frame,
        text="Game Aspects",
        font=("Arial", 11, "bold", "underline"),
        bg="#66C166",
        fg="#fdfd96",
    )
    display_aspect_label.grid(row=0, column=1, padx=10, pady=10)

    display_desc_label = Label(
        master=display_frame,
        text="Improvements",
        font=("Arial", 11, "bold", "underline"),
        bg="#66C166",
        fg="#fdfd96",
    )
    display_desc_label.grid(row=0, column=2, padx=10, pady=10)

    display_state_label = Label(
        master=display_frame,
        text="Completed",
        font=("Arial", 11, "bold", "underline"),
        bg="#66C166",
        fg="#fdfd96",
    )
    display_state_label.grid(row=0, column=3, padx=10, pady=10)

    username = get_username(base_frame)
    c.execute(
        "SELECT id, date, aspect, description, completed FROM stats WHERE username=?",
        (username,),
    )
    data = c.fetchall()

    for i in range(len(data)):
        id, date, aspect, description, completed = data[i]
        Label(
            master=display_frame,
            text=date,
            font=("Arial", 11, "bold"),
            bg="#66C166",
            fg="#fdfd96",
        ).grid(row=i + 1, column=0, padx=10, pady=10)

        Label(
            master=display_frame,
            text=aspect,
            font=("Arial", 11, "bold"),
            bg="#66C166",
            fg="#fdfd96",
        ).grid(row=i + 1, column=1, padx=10, pady=10)

        Label(
            master=display_frame,
            text=description,
            font=("Arial", 11, "bold"),
            bg="#66C166",
            fg="#fdfd96",
        ).grid(row=i + 1, column=2, padx=10, pady=10)

        current_state = IntVar(value=completed)
        Checkbutton(
            master=display_frame,
            command=lambda id=id, current_state=current_state: completed_callback(
                current_state.get(), id
            ),
            variable=current_state,
            onvalue=1,
            offvalue=0,
            bg="#66C166",
            selectcolor="#77DD77",
            fg="#fdfd96",
            activebackground="#66C166",
        ).grid(row=i + 1, column=3, padx=10, pady=10)

    # Update display_frame and configure scroll region of display_canvas
    display_frame.update_idletasks()
    display_canvas.configure(scrollregion=display_canvas.bbox("all"))
    conn.commit()
    conn.close()


def completed_callback(state, id):
    conn = sqlite3.connect(resource_path("data\\tennis_stats.db"))
    c = conn.cursor()

    c.execute("UPDATE stats SET completed = ? WHERE id = ?", (state, id))

    conn.commit()
    display_data()
    conn.close()


def submit_callback():
    conn = sqlite3.connect(resource_path("data\\tennis_stats.db"))
    c = conn.cursor()

    date = date_entry.get()
    aspect = game_aspect_entry.get()
    desc = description_entry.get()
    valid_inputs = date != "" and aspect != "" and desc != ""
    valid_date = check_format(date)

    if valid_inputs and valid_date:
        date_entry.delete(0, END)
        game_aspect_entry.delete(0, END)
        description_entry.delete(0, END)
        username = get_username(base_frame)
        values = (username, date, aspect, desc, 0)
        c.execute(
            "INSERT INTO stats (username, date, aspect, description, completed) VALUES (?, ?, ?, ?, ?)",
            values,
        )

        messagebox.showinfo("Record Added", f"Successfully added the record of {date}")
        root.focus()

    else:
        messagebox.showerror(
            "Invalid Inputs",
            "One or more text fields are empty, make sure to fill all required fields",
        )

    conn.commit()
    display_data()
    conn.close()


def get_username(container):
    for child in container.winfo_children():
        if isinstance(child, Label):
            label_text = child.cget("text")
            if label_text.startswith("Welcome back"):
                return label_text.split("\n")[-1]
    return None


def welcome_user(user):
    global user_label
    user_label = Label(
        master=base_frame,
        text=f"Welcome back,\n{user}",
        font=("Arial", 17, "bold"),
        bg="#77DD77",
        fg="#fdfd96",
    )
    user_label.place(relx=0.30, rely=0.1)
    if user[-1] == "s":
        title = f"Tennis Tracker | {user}' Tracker"
    else:
        title = f"Tennis Tracker | {user}'s Tracker"
    root.title(title)


def check_format(date):
    try:
        datetime.datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        messagebox.showerror(
            "Error", "Incorrect date format. Please enter date in dd/mm/yyyy format."
        )
        return False


# Create Base Frame:
base_frame = Frame(
    master=root,
    width=500,
    height=750,
    bg="#77DD77",
)
base_frame.grid(row=0, column=0)

nav = navbar(
    master=base_frame,
    dimensions=(500, 75),
    color="#66C166",
)

nav_title = Label(
    master=nav,
    text="Tennis Tracker",
    fg="#fdfd96",
    bg="#66C166",
    font=("Arial", 15, "bold"),
)
nav_title.place(relx=0.1, rely=0.03)

nav_img = Image.open(resource_path("static\\tennisappicon.png"))
nav_img = nav_img.resize((32, 32), Image.LANCZOS)
nav_logo = ImageTk.PhotoImage(nav_img)

logo_label = Label(
    master=nav,
    image=nav_logo,
    bg="#66C166",
).place(relx=0.03, rely=0.03)

home_img = Image.open(resource_path("static\\home.png"))
home_img = home_img.resize((28, 28), Image.LANCZOS)
home_btn_img = ImageTk.PhotoImage(home_img)

home_btn = Button(
    master=nav,
    image=home_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=home_callback,
)
home_btn.place(relx=0.6, rely=0.03)

profile_img = Image.open(resource_path("static\\user.png"))
profile_img = profile_img.resize((28, 28), Image.LANCZOS)
profile_btn_img = ImageTk.PhotoImage(profile_img)

profile_btn = Button(
    master=nav,
    image=profile_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=profile_callback,
)
profile_btn.place(relx=0.7, rely=0.03)

add_img = Image.open(resource_path("static\\more.png"))
add_img = add_img.resize((28, 28), Image.LANCZOS)
add_btn_img = ImageTk.PhotoImage(add_img)

add_btn = Button(
    master=nav,
    image=add_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=add_callback,
)
add_btn.place(relx=0.8, rely=0.03)


logout_img = Image.open(resource_path("static\\logout.png"))
logout_img = logout_img.resize((28, 28), Image.LANCZOS)
logout_btn_img = ImageTk.PhotoImage(logout_img)

logout_btn = Button(
    master=nav,
    image=logout_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=logout_callback,
)
logout_btn.place(relx=0.9, rely=0.03)

# Create New Record Frame:
add_record_frame = Frame(
    master=root,
    width=500,
    height=750,
    bg="#77DD77",
)
add_record_frame.grid(row=0, column=0)

nav2 = navbar(
    master=add_record_frame,
    dimensions=(500, 75),
    color="#66C166",
)

nav_title = Label(
    master=nav2,
    text="Tennis Tracker",
    fg="#fdfd96",
    bg="#66C166",
    font=("Arial", 15, "bold"),
)
nav_title.place(relx=0.1, rely=0.03)


nav_logo = ImageTk.PhotoImage(nav_img)
logo_label = Label(
    master=nav2,
    image=nav_logo,
    bg="#66C166",
).place(relx=0.03, rely=0.03)

profile_btn = Button(
    master=nav2,
    image=profile_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=profile_callback,
)
profile_btn.place(relx=0.7, rely=0.03)

home_btn = Button(
    master=nav2,
    image=home_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=home_callback,
)
home_btn.place(relx=0.6, rely=0.03)

add_btn = Button(
    master=nav2,
    image=add_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=add_callback,
)
add_btn.place(relx=0.8, rely=0.03)

logout_btn = Button(
    master=nav2,
    image=logout_btn_img,
    bg="#66C166",
    activebackground="#66C166",
    border=0,
    text=None,
    command=logout_callback,
)
logout_btn.place(relx=0.9, rely=0.03)

# Add Widgets to the Record Frame:
entry_frame = Frame(
    master=add_record_frame,
    width=350,
    height=400,
    bg="#66C166",
    highlightbackground="#fdfd96",
    highlightthickness=3,
)
entry_frame.place(relx=0.15, rely=0.15)

date_label = Label(
    master=entry_frame,
    text="Date:",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
date_label.place(relx=0.1, rely=0.05)

date_entry = Entry(
    master=entry_frame,
    width=30,
    border=3,
    bg="#77DD77",
    fg="#fdfd96",
    font=("Arial", 11, "bold"),
)
date_entry.place(relx=0.05, rely=0.15)

game_aspect_label = Label(
    master=entry_frame,
    text="Game Aspect:",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
game_aspect_label.place(relx=0.1, rely=0.35)

game_aspect_entry = Entry(
    master=entry_frame,
    width=30,
    border=3,
    bg="#77DD77",
    fg="#fdfd96",
    font=("Arial", 11, "bold"),
)
game_aspect_entry.place(relx=0.05, rely=0.45)

description_label = Label(
    master=entry_frame,
    text="Improvement:",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
description_label.place(relx=0.1, rely=0.65)

description_entry = Entry(
    master=entry_frame,
    width=30,
    border=3,
    bg="#77DD77",
    fg="#fdfd96",
    font=("Arial", 11, "bold"),
)
description_entry.place(relx=0.05, rely=0.75)

submit_button = Button(
    master=entry_frame,
    text="Submit",
    fg="#fdfd96",
    bg="#66C166",
    width=10,
    border=3,
    command=submit_callback,
    activeforeground="#66C166",
    activebackground="#fdfd96",
)
submit_button.place(relx=0.4, rely=0.9)


# Create the register frame
register_frame = Frame(
    master=root,
    width=500,
    height=750,
    bg="#77DD77",
)
register_frame.grid(row=0, column=0)

inputs_frame = Frame(
    master=register_frame,
    width=450,
    height=700,
    bg="#66C166",
    highlightbackground="#fdfd96",
    highlightthickness=3,
)
inputs_frame.place(relx=0.05, rely=0.01)


username_label_register = Label(
    master=inputs_frame,
    text="Username",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
username_label_register.place(relx=0.05, rely=0.05)

username_entry_register = Entry(
    master=inputs_frame,
    width=30,
    border=3,
    font=("Arial", 12, "bold"),
    fg="#fdfd96",
    bg="#77DD77",
)
username_entry_register.place(relx=0.1, rely=0.1)

email_label_register = Label(
    master=inputs_frame,
    text="Email Address",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
email_label_register.place(relx=0.05, rely=0.2)

email_entry_register = Entry(
    master=inputs_frame,
    width=30,
    border=3,
    font=("Arial", 12, "bold"),
    fg="#fdfd96",
    bg="#77DD77",
)
email_entry_register.place(relx=0.1, rely=0.25)

password_label_register = Label(
    master=inputs_frame,
    text="Password",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
password_label_register.place(relx=0.05, rely=0.35)

password_entry_register = Entry(
    master=inputs_frame,
    width=30,
    border=3,
    font=("Arial", 12, "bold"),
    fg="#fdfd96",
    bg="#77DD77",
)
password_entry_register.place(relx=0.1, rely=0.4)

register_btn = Button(
    master=inputs_frame,
    text="Register",
    fg="#fdfd96",
    bg="#66C166",
    width=20,
    border=3,
    command=register_callback,
    activeforeground="#66C166",
    activebackground="#fdfd96",
)
register_btn.place(relx=0.3, rely=0.5)

go_to_login_label = Label(
    master=register_frame,
    text="Already have an account?",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
go_to_login_label.place(relx=0.2, rely=0.6)

go_to_login_btn = Button(
    master=register_frame,
    text="Login",
    fg="#fdfd96",
    bg="#66C166",
    width=4,
    border=0,
    font=("Arial", 11, "bold"),
    command=go_to_login,
    activebackground="#66C166",
)
go_to_login_btn.place(relx=0.58, rely=0.6)
go_to_login_btn.bind("<Enter>", on_enter)
go_to_login_btn.bind("<Leave>", on_leave)

# Create the login frame:
login_frame = Frame(
    master=root,
    width=500,
    height=750,
    bg="#77DD77",
)
login_frame.grid(row=0, column=0)

inputs_frame = Frame(
    master=login_frame,
    width=450,
    height=700,
    bg="#66C166",
    highlightbackground="#fdfd96",
    highlightthickness=3,
)
inputs_frame.place(relx=0.05, rely=0.01)


username_label_login = Label(
    master=inputs_frame,
    text="Username",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
username_label_login.place(relx=0.05, rely=0.05)

username_entry_login = Entry(
    master=inputs_frame,
    width=30,
    border=3,
    font=("Arial", 12, "bold"),
    fg="#fdfd96",
    bg="#77DD77",
)
username_entry_login.place(relx=0.1, rely=0.1)

password_label_login = Label(
    master=inputs_frame,
    text="Password",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
password_label_login.place(relx=0.05, rely=0.2)

password_entry_login = Entry(
    master=inputs_frame,
    width=30,
    border=3,
    font=("Arial", 12, "bold"),
    fg="#fdfd96",
    bg="#77DD77",
)
password_entry_login.place(relx=0.1, rely=0.25)

forgot_password_btn = Button(
    master=inputs_frame,
    text="Forgot my password",
    fg="#fdfd96",
    bg="#66C166",
    border=0,
    font=("Arial", 11, "bold"),
    width=20,
    command=new_password_callback,
    activebackground="#66C166",
)
forgot_password_btn.place(relx=0.05, rely=0.3)
forgot_password_btn.bind("<Enter>", on_enter)
forgot_password_btn.bind("<Leave>", on_leave)

login_btn = Button(
    master=inputs_frame,
    text="Login",
    fg="#fdfd96",
    bg="#66C166",
    width=20,
    border=3,
    command=login_callback,
    activeforeground="#66C166",
    activebackground="#fdfd96",
)
login_btn.place(relx=0.3, rely=0.35)

go_to_register_label = Label(
    master=login_frame,
    text="Don't have an account?",
    font=("Arial", 11, "bold"),
    bg="#66C166",
    fg="#fdfd96",
)
go_to_register_label.place(relx=0.26, rely=0.45)

go_to_register_btn = Button(
    master=login_frame,
    text="Register",
    fg="#fdfd96",
    bg="#66C166",
    width=8,
    border=0,
    font=("Arial", 11, "bold"),
    command=go_to_register,
    activebackground="#66C166",
)
go_to_register_btn.place(relx=0.6, rely=0.45)
go_to_register_btn.bind("<Enter>", on_enter)
go_to_register_btn.bind("<Leave>", on_leave)

img = Image.open(resource_path("static\\tennisappicon.png"))
img = img.resize((200, 200), Image.LANCZOS)
logo = ImageTk.PhotoImage(img)
logo_label = Label(master=login_frame, image=logo, bg="#66C166").place(
    relx=0.3, rely=0.55
)

app_label = Label(
    master=login_frame,
    text="Tennis Tracker",
    fg="#fdfd96",
    bg="#66C166",
    font=("Arial", 20, "bold", "italic"),
)
app_label.place(relx=0.3, rely=0.85)

# Commit the changes to the database
conn.commit()
conn.close()

# Show and hide frames:
register_frame.grid_forget()
base_frame.grid_forget()
add_record_frame.grid_forget()

# Run App:
root.mainloop()
