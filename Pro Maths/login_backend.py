import bcrypt # python modules used
import yagmail
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from remake_register import password_check,email_check # import functionality from different files
from create_connection import cursor, cursor1, db


def get_id_student(username): # function for getting the student id
    # sql that takes the username and returns ID
    sql = "SELECT ID FROM Students WHERE username = ?" 
    cursor.execute(sql, [(username)]) # execution of the sql
    return cursor.fetchone()[0] # returns the integer value of ID


def back_button(school):
    # This is used for the help Page so that a student or teacher is directed back to the right page
    if school is "Student": # if student then return S
        return "S"
    elif school is "Teacher": # if teacher then return Y
        return "T"
    else:
        return "M" # else is just return to main meun


def login_in(username, password): # checks using student check and teacher check function 
    if student_check(username, password) is True and teacher_check(username, password) is False:
        return "S" # S is returned to stand for student
    elif student_check(username, password) is False and teacher_check(username, password) is True:
        return "T" # T is returned to stand for teacher
    else: # if neither condition is met then it returns false
        return False


def forgot_password(email, new_pass, confirm_pass): # Used to change the user password if forgotten
    if (student_email(email) is not False and teacher_email(email) is False):
        if password_check(new_pass, confirm_pass) is True: # validation for password from remake_register
            password_store = bcrypt.hashpw(new_pass.encode("utf8"), bcrypt.gensalt()) # hashes the new password
            update_student = ("UPDATE Students SET password=? WHERE email=?")
            # updates the password based on the user email and it being a student
            cursor.execute(update_student, [(password_store), (email)]) # performs the update on the Student table
            db.commit() # saves changes made 
            return True # refers back to the tkinter page


    elif (student_email(email) is False and teacher_email(email) is not False):
        if password_check(new_pass, confirm_pass) is True: # validation for password from remake_register
            password_store = bcrypt.hashpw(new_pass.encode("utf8"), bcrypt.gensalt()) # hashes the new password
            update_student = ("UPDATE Teachers SET password=? WHERE email=?")
            # updates the password based on the user email and it being a teacher
            cursor.execute(update_student, [(password_store), (email)])
            # performs the update on the Teacher table 
            db.commit() # saves changes made 
            return True # refers back to the tkinter page 
        

    else: # if either condition is met then it returns an tkinter error message
        messagebox.showerror("Email", "Email doesn't exist either message support or register as you haven't made an account") # this is error message


def student_check(username, password):
    # Used for the login function this checks against the username
    # and password the user enters in students table
    find_user = ("SELECT username,password FROM Students WHERE username = ?")
    # sql statement for getting the username and password
    cursor.execute(find_user, [(username)])
    #executes the above sql code
    checking = cursor.fetchone()
    # fetchs one of the values
    if checking is not None:
        # if there are values in check then it goes through this process
        db_user, db_password = checking # gets username and password stored in the database
        if (username == db_user) and (bcrypt.checkpw(password.encode("utf8"), db_password) is True):
            #checks the database username and password against the username and password stored
            return True # if condition met return true
    else:
        return False # if condition not met return False


def teacher_check(username, password):
    # Used for the login function this checks against the username and password the user enters in students table
    find_user1 = ("SELECT username,password FROM Teachers WHERE username = ?")
    # sql statement for getting the username and password
    cursor1.execute(find_user1, [(username)]) #executes the above sql code
    checking1 = cursor1.fetchone() # fetchs one of the values
    if checking1 is not None: # if there are values in check then it goes through this process
        db_user1, db_password1 = checking1 # gets username and password stored in the database
        if (username == db_user1) and (bcrypt.checkpw(password.encode("utf8"), db_password1) is True):
            #checks the database username and password against the username and password stored
            return True # if condition met return true
    else:
        return False # if condition not met return False


def student_email(email): # checks the email the user entered against the student database
    find_student = ("SELECT Students.email FROM Students WHERE email = ?")
    # sql statement checks based on email variable condition
    cursor.execute(find_student, [(email)]) # execution of sql statement
    result = cursor.fetchone() # gets one value
    if result is not None: # checks based on condition that there is values to check
        db_email = result # sets the value db_email based on result
        if email == db_email: # checks user input against database value
            return True # if condition is met it returns true

    else:
        return False # if condition not met it returns false


def teacher_email(email): # checks the email the user entered against the teacher database
    find_teacher = ("SELECT Teachers.email FROM Teachers WHERE email = ?")
    # sql statement checks based on email variable condition
    cursor1.execute(find_teacher, [(email)]) # execution of sql statement
    checking = cursor1.fetchone() # gets one value
    if checking is not None: # checks based on condition that there is values to check
        db_email = checking # sets the value db_email based on result
        if email == db_email: # checks user input against database value
            return True # if condition is met it returns true
    else: 
        return False # if condition not met it returns false


def support_email(): # Used to send an email to Maths Pro
    support_window = tk.Tk() # Creates a new tkitner window 
    support_window.withdraw() # removes the box the tkinter window makes
    support_window.attributes("-topmost", True) # makes the window appear over the tkinter frames

    yag = yagmail.SMTP("mathspro0@gmail.com", oauth2_file="~/oauth2_creds1.json")
    # creates the API connection to the mathspro0@gmail.com email 

    # asks the user for their email address 
    email = simpledialog.askstring("Email", "Please enter your email address", parent=support_window)
    if email is not None: # email cannot be empty
        if email_check(email) is True: # validation from remake_register 
            text = simpledialog.askstring( # Message window for the user to enter a message 
                "Input", "Enter your problem or advice to send to Maths Pro", parent=support_window)
        
            send_mail = ("Email to Maths Pro", # Email to be send to the user
                         text, "From:",email) 
            if text is not None: # Only sends emails with contents in text
                try:
                    yag.send(subject="Maths Pro Support Email", contents=send_mail) # sends the email with the user email address
                    support_window.destroy() # gets rid of the window
                    return True
                except: # tkinter error message if there is a problem with yagmail 
                    messagebox.showinfo("Email","Due to a connection issue an email hasn't been sent")
                    support_window.destroy()
            else:
                messagebox.showerror( # tkinter error message if text is left none
                    "Support", "Please type in a message in order for it to be sent to support")
                support_window.destroy() # gets rid of the window
    else: # tkinter error message if text is email is none
        messagebox.showerror("Email","Please enter a email address and don't leave it blank")

def terminate():
    # prompts the user to answer a yes or no question
    ask = messagebox.askquestion("Maths Pro"
            ,"Do you wish to exit Maths Pro?", icon="warning")
    if ask == "yes": # if answer is yes then it terminates the whole program
        exit()
    # if no it does nothing
