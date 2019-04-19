from tkinter import messagebox  # module for error messages on the tkinter page
import string # python modules 
import re
import bcrypt
from validate_email import validate_email
import yagmail
from create_connection import cursor, cursor1, db # importing the db connection from create_connection

shared_data = {"firstname": "blank",  # dictionary that stores the user register information
               "surname": "blank",    # through using the controller we can pass these variables
               "age": 0,        # to different frames
               "Class": "blank",
               "gender": "blank", }
create_student_table = ("""CREATE TABLE IF NOT EXISTS Students(ID INTEGER PRIMARY KEY,
                        Forename VARCHAR(30),
                        Surname VARCHAR(30) ,  Age INTEGER ,
                        class VARCHAR (3), Gender VARCHAR (30) ,
                         Username VARCHAR(30),Password VARCHAR(80), Email VARCHAR(30))""")

create_teacher_table = ("""CREATE TABLE IF NOT EXISTS Teachers( ID INTEGER PRIMARY KEY,
                        Forename VARCHAR(30) ,
                        Surname VARCHAR(30) ,  Age INTEGER ,
                        Class VARCHAR (3) , Gender VARCHAR (30),
                         Username VARCHAR(30), Password VARCHAR(80), Email VARCHAR(30))""")
# Sql statment to create the table where the user information will be stored
cursor.execute(create_student_table)  # executes the sql statement

# Sql statment to create the table where the user information will be stored
cursor.execute(create_teacher_table)  # executes the sql statement
db.commit()  # saves changes made to the sql file

def get_forename(user_id): # gets the user forename using the user id from the table Students
    sql_forename = """SELECT Forename FROM Students WHERE ID = ?"""
    cursor.execute(sql_forename, [(user_id)])
    return cursor.fetchone()[0] # returns the forename of the user
def get_surname(user_id): # gets the user surname using the user id from the table Students
    sql_surname = """SELECT Surname FROM Students WHERE ID = ?"""
    cursor.execute(sql_surname, [(user_id)])
    return cursor.fetchone()[0]# returns the surname of the user
def register1(firstname, surname, age, school_class, var, var1):  # Function for registration
    # first name has to be alphabetical characters only and between 2 and 20 characters
    if firstname.isalpha() is True and ((len(firstname) >= 2) and (len(firstname)) <=20):
        firstname.title() # first letter is captialised in first name
        # Surname has to be alphabetical characters only and between 2 and 20 characters
        if surname.isalpha() is True and ((len(surname) >= 2) and (len(surname)) <=20):
            surname.title() # first letter is captialised in surname
            try: # loop that works on error exceptions
                if (int(age) >=16): # trys to run this and age hasto be above 16
                    if school_class.isalnum() is True:
                        if var == 1:  # when var is 1 then gender is Male
                            if (var1 == 1) or (var1 == 2):
                                shared_data["firstname"] = firstname # stores all the values in the                               
                                shared_data["surname"] = surname     # in the dictionary
                                shared_data["age"] = int(age)
                                shared_data["gender"] = "Male"
                                shared_data["Class"] = school_class
                                return True
                            else: # if var1 is not 1 or 2 then return tkinter error message
                                messagebox.showerror(
                                    "School", "Please choose either Student or Teacher")
                        elif var == 2: # when var is 2 then gender is Female
                            if (var1 == 1) or (var1 == 2):
                                shared_data["firstname"] = firstname
                                shared_data["surname"] = surname
                                shared_data["age"] = int(age)
                                shared_data["gender"] = "Female"
                                shared_data["Class"] = school_class
                                return True
                            else: # if var1 is not 1 or 2 then return tkinter error message
                                messagebox.showerror(
                                    "School", "Please choose either Student or Teacher")
                        else: # if var is not 1 or 2 then return tkinter error message
                            messagebox.showerror("Gender", "Gender option cannot be left blank")
                    else: # if class hasn't been chosen then return tkinter error message
                        messagebox.showerror("Class", "Class option cannot be left blank")
                else: # if the user isn't above 16 then return tkinter error message
                    messagebox.showerror("Age", "You have to be 16 or older to use Maths Pro")
            except ValueError: # if the user didn't enter a number return tkinter error message
                messagebox.showerror("Age", "Please enter a number")
        else: # if surname isn't in the range or contains non alpha characters then return tkinter error
            messagebox.showerror("Surname", "Please enter a Proper Surname that is between 2 and 20 characters long")
    else: # if forename isn't in the range or contains non alpha characters then return tkinter error
        messagebox.showerror("First Name", "Please enter a proper First Name that is between 2 and 20 characters long")


def username_check(username):  # function for username vaildation
    # Checking the length of username is between 6 and 30 chracters
    if (len(username) >= 6) and (len(username) <=30):
        # sql statement for checking existing users
        # Checks student database for username
        fetchstudents = ("SELECT DISTINCT Students.Username from Students WHERE Username = ?")
        # Checkes teacher databaase for username
        fetchteachers = ("SELECT DISTINCT Teachers.Username from Teachers WHERE Username = ?")
        cursor.execute(fetchstudents, [(username)])  # executes the above query on the student table
        cursor1.execute(fetchteachers, [(username)])  # execute the above query on the teacher table
        checking = cursor.fetchall()  # stores the result of sql search done on the Student table
        checking1 = cursor1.fetchall() # stores the result of sql search done on the Teacher table
        if checking or checking1: # if checking or checking1 has values then return tkinter error
            messagebox.showerror("Username", "That username has been taken please try another one")
        else: # if checking and checking 1 is none then return true
            return True

    else: #if username isn't in the range then return tkinter error message
        messagebox.showerror(
            "Username", "Username has to be between 6 and 30 characters")


def password_check(password, password_confirm):  # function for password vaildation
    if len(password) >= 8:  # checks whether the password length is 8 chracterslong
        # checks for letters in the password
        if len(set(string.ascii_lowercase).intersection(password)) > 0:
            # checks for numbers or special characters in the password
            if (len(set(string.ascii_uppercase).intersection(password)) > 0):
                # checks for uppercase characters
                if (len(set(string.digits).intersection(password))) > 0:
                    # checks for special characters
                    if (len(set(string.punctuation).intersection(password))) > 0:
                        if password == password_confirm: # compare string of both passwords if match 
                            return True # return true 
                        else:
                            messagebox.showerror("Password", "Password don't match")
                            # tkinter error message when passwords don't match
                    
                    else: # tkinter error message when password doesn't contain special characters
                        messagebox.showerror(
                            "Password", "Password doesn't contain a special character")
                else:
                    # tkinter error message when the password doesn't contain digits
                    messagebox.showerror(
                        "Password", "Password don't contain numbers")
            else:
                messagebox.showerror(
                    "Password", "Password don't contain any uppercase characters")
                # tkinter error message when the password doesn't contain any uppercase characters
        else:
            messagebox.showerror(
                "Password", "Password don't contain any lowercase letters")
            # tkinter error message when the password doesn't contain any lowercase characters
    else:
        messagebox.showerror(
            "Password", "Password is not 8 characters long")
        # tkinter error message when the password isn't longer than 8 characters


def email_check(email):  # function for email vaildation
     #does a regex expression match to see if email is in the format example@example.com
    match = re.match(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email)
    is_valid = validate_email(email) # verifies where the email completely exists

    if match is None: # tkinter error message when email is not in the right format
        messagebox.showerror("Email", "Please enter a valid email address")
    elif is_valid is not True: # tkinter error message when email doesn't exist
        messagebox.showerror(
            "Email", "Email address doesn't exist please try another email address")
    else: # match is not none and is_valid is true then return true
        return True


def register2(username, password, confirm_password, email, var1):
    # checks whether a existing username with the username enter exists
    if username_check(username):
        # ensures the password passes all the vaildations
        if password_check(password, confirm_password): # has to return true
            password_store = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()) # hashes the password
            if email_check(email):  # ensures the email passes the vaildation
                if var1 == 1:  # inserts one whole record into student table
                    insert_student = (
                        "INSERT INTO Students(Forename,Surname,Age,Class,Gender,Username,Password,Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
                    cursor.execute(insert_student, [(shared_data["firstname"]), (shared_data["surname"]),
                                                    (shared_data["age"]), (shared_data["Class"]),
                                                    (shared_data["gender"]), (username), (password_store), (email)])
                    send_email(email, username) # sends an email to the user
                    db.commit()  # saves the changes to the database file
                    return True
                    
                elif var1 == 2:  # inserts one whole record into the teacher table
                    insert_teacher = (
                        "INSERT INTO Teachers(Forename,Surname,Age,Class,Gender,Username,Password,Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
                    cursor.execute(insert_teacher, [(shared_data["firstname"]), (shared_data["surname"]),
                                                    (shared_data["age"]), (shared_data["Class"]),
                                                    (shared_data["gender"]), (username), (password_store), (email)])
                    send_email(email, username) # sends an email to the user
                    db.commit()  # saves the changes to the database file
                    return True


def send_email(email, username): # used for sending an email to the user
    yag = yagmail.SMTP("mathspro0@gmail.com", oauth2_file="~/oauth2_creds1.json")
    # creates the API connection to mathspro0@gmail.com
    send_mail = (" Email Confirmation From Maths Pro", # contents of the email to send
                 " First Name:" + shared_data["firstname"],
                 "Surname:" + shared_data["surname"],
                 " Age:" + str(shared_data["age"]),
                 "Class: " + shared_data["Class"],
                 "Gender:" + shared_data["gender"],
                 "username:" + username)
    try: # trys to send the email if it doesn't work then a info message is returned
        yag.send(to=email, subject="Maths Pro Email Confirmation", contents=send_mail)
    except:
        messagebox.showinfo("Email","Due to a connect issue an email hasn't been sent")
