import sqlite3 as sql # python modules used
import datetime as dt
import tkinter as tk
import pandas as pd
from tkinter import messagebox
from tkinter import ttk
with sql.connect("updatedfile.db", detect_types=sql.PARSE_DECLTYPES) as db: # connection made to db file with data type detection
    cursor = db.cursor() # creating two cursors for interacting with the db file
    cursor1 = db.cursor()
shared_data = {"date": None, # dictionary used for Set Test Date
               "type": None,
               "level": None,
               "comments": "No Further Comments"}
current_date = dt.date.today().strftime("%Y-%m-%d") # Gets the current date (today's date)
# the create table statement is no longer needed as the table already exists
create_date_table = (
    "CREATE TABLE IF NOT EXISTS test_dates(test_date DATE, test_type TEXT, test_level TEXT, comments TEXT, time_stamp DATE)")
#creating the test date table with columns
# test_date, text_type, text_level, comments and time_stamp 
cursor.execute(create_date_table) # sql execution of creating the table

db.commit() # saves changes made to the db file

title_font = ("Times New Roman", 30) # setting a title font type with font family and size
medium_font = ("Times New Roman", 20) # setting a medium font type with font family and size


def show_details():
    messagebox.showinfo("Window", "After you have finished with this window you can close it") #tkinter pop up message 
    root = tk.Tk() # creating a tkinter window

    title_label = tk.Label(root, text="Tests", font=title_font, bg="grey") # title label for the tkinter window
    title_label.config(fg="white",bg="blue")
    title_label.pack()

    # the following code is for test dates that are today it has a title label a label with all the test dates
    # which has been added onto the tkinter window created
    current_label = tk.Label(root, text="Test For Today", bg="grey", font=title_font) 
    current_label.config(anchor="center")
    current_label.pack(pady=10)
    today_label = tk.Label(root, text=current_test(), bg="grey", font=medium_font, wraplengt=900)
    today_label.pack()
    
    separator = ttk.Separator(root, orient="horizontal") # separates the current test and upcoming test from each other
    separator.pack(fill="x") # creates a line that fills the whole x axis

    # the following code is for test dates that are in the future it has a title label and a label with all the test dates
    # which also has been added on the tkinter window created
    upcoming_label = tk.Label(root, text="Upcoming Tests", font=title_font, bg="grey")
    upcoming_label.pack()

    test_upcoming = tk.Label(root, text=upcoming_test(), bg="grey", font=medium_font,wraplengt=900)
    test_upcoming.pack()

    exit_button = tk.Button(root, text="Exit", command=lambda: root.destroy()) # button for closing the window
    exit_button.config(height=3, width=10, bg="blue", fg="white")
    exit_button.place(x=1120, y=745)

    # button for updating the text on the today_label and test_upcoming label if a new test is added or a test
    # needs to be removed
    refresh_button = tk.Button(root, text="Refresh Tests", command=lambda: update_labels())  
    refresh_button.config(height=3, width=10, bg="blue", fg="white")
    refresh_button.place(x=0, y=745)


    def update_labels(): # refresh button runs this function
        delete_date() # removes test dates that have past 
        today_label["text"] = current_test() # sets the text of the today_label to be current_test
        test_upcoming["text"] = upcoming_test() # sets the text of the test_upcoming to be upcoming_test
    root.geometry("1200x800") # sets the size of the tkinter window
    root.config(bg="grey") # sets the colour of the tkinter window
    root.attributes("-topmost", True) # makes the tkinter window appear at the top 
    root.resizable(height=False,width=False) # prevents the window from being resized


def upcoming_test(): # gets upcoming tests
    # sql has a limit of only 4 records to prevent flooding the tkinter window
    sql = """ SELECT test_date,test_type,test_level,comments FROM test_dates WHERE test_date > ? LIMIT 4 """
    resp = pd.read_sql_query(sql, db, params=(current_date,)) # converts the sql execution into a dataframe
    if resp.empty: # condition that the dataframe is empty
        return "No Test Set for the Future" # sets label text to be the return value 
    else: # if the other condition is not met then 
        return resp.to_csv(None, index= False) # returns the dataframe as a csv without the index



def current_test():  # gets tests that are today 
    # sql has a limit of only 3 records to prevent flooding the tkinter window
    sql = """ SELECT test_date,test_type,test_level,comments FROM test_dates WHERE test_date = ? LIMIT 3 """
    resp = pd.read_sql_query(sql, db, params=(current_date,)) # converts the sql execution into a dataframe
    if resp.empty: # condition that the dataframe is empty
        return "No Test Set for Today" # sets label text to be the return value 
    else: # if the other condition is not met then 
        return resp.to_csv(None, index = False) # returns the dataframe as a csv without the index

def update_stamp(): # updates time_stamp for all records in the test_dates table
    sql = """ UPDATE test_dates SET time_stamp = ? """
    cursor.execute(sql, [(current_date)]) # changes time_stamp to the current_date value
    db.commit() # saves the change made to every record time_stamp


def delete_date(): # removes dates from the test_dates table
    # deletes dates where time_stamp is greater than the test date
    delete_date = ("DELETE FROM test_dates WHERE time_stamp > test_date") 
    cursor.execute(delete_date) # executes the sql 
    db.commit() # saves the records deleted from the table 


def set_test(date, type, level, comment): # setting a test date and storing it in the test dates table
    # sql for inserting into the test_dates table
    insert_test ="""INSERT INTO test_dates (test_date, test_type, test_level, comments, time_stamp)
        VALUES (?,?,?,?,?)"""
    try: # loop that continues based on no error occuring
        dt.datetime.strptime(date, '%Y-%m-%d') # compares the date input to the format YYYY-MM-DD
        if date < current_date: # if date is less than current date (today's date)
            messagebox.showerror("Date","Date already past set a reasonable date") # return tkinter error message
        else:
            shared_data["date"] = date # stores the value in the dictionary
            if type == 1: # type being 1 means that a pure test is set
                shared_data["type"] = "Pure" # stores the type as pure in dictionary
                if level == 1: # level being 1 means that an AS test is set
                    shared_data["level"] = "AS" # stores level as AS in dictionary
                    if len(comment) < 250: # comment has to be less than 250 characters
                        shared_data["comments"] = comment # stores comment in dictionary
                        cursor.execute(insert_test, [(shared_data["date"]), # inserts record into the table
                                                     (shared_data["type"]),
                                                     (shared_data["level"]),
                                                     (shared_data["comments"]),
                                                     (current_date)])
                        db.commit() # saves changes made to the db file
                        return True # returns True for the tkinter main window
                    else: # when comment is not less than 250 characters
                        messagebox.showerror("Comment","Comment has to be less than 250 characters") # return tkinter error message
                elif level == 2: # level being 2 means that an A2 test is set
                    shared_data["level"] = "A2" # stores level as A2 in dictionary
                    if len(comment) < 250: # comment has to be less than 250 characters
                        shared_data["comments"] = comment # stores comment in dictionary
                        cursor.execute(insert_test, [(shared_data["date"]), # inserts record into the table
                                                     (shared_data["type"]),
                                                     (shared_data["level"]),
                                                     (shared_data["comments"]),
                                                     (current_date)])
                        db.commit() # saves changes made to the db file
                        return True # returns True for the tkinter main window
                    else: # when comment is not less than 250 characters return tkinter error message
                        messagebox.showerror("Comment","Comment has to be less than 250 characters") 
                        
                else: # level has to be either 1 or 2 if not return tkinter error message
                    messagebox.showerror("Level", "Test Level cannot be left blank") 
            elif type == 2: # type being 2 means that an applied test is set
                shared_data["type"] = "Applied" # stores the type as applied in dictionary
                if level == 1: # level being 1 means that an AS test is set
                    shared_data["level"] = "AS" # stores level as AS in dictionary
                    if len(comment) < 250: # comment has to be less than 250 characters
                        shared_data["comments"] = comment # stores comment in dictionary
                        cursor.execute(insert_test, [(shared_data["date"]), # inserts record into the table
                                                     (shared_data["type"]),
                                                     (shared_data["level"]),
                                                     (shared_data["comments"]),
                                                     (current_date)])
                        db.commit() # saves changes made to the db file
                        return True # returns True for the tkinter main window
                    else: # when comment is not less than 250 characters
                        messagebox.showerror("Comment","Comment has to be less than 250 characters") # return tkinter error message
                elif level == 2: # level being 2 means that an A2 test is set
                    shared_data["level"] = "A2" # stores level as A2 in dictionary
                    if len(comment) < 250: # comment has to be less than 250 characters
                        shared_data["comments"] = comment # stores comment in dictionary
                        cursor.execute(insert_test, [(shared_data["date"]), # inserts record into the table
                                                     (shared_data["type"]),
                                                     (shared_data["level"]),
                                                     (shared_data["comments"]),
                                                     (current_date)])
                        db.commit() # saves changes made to the db file
                        return True # returns True for the tkinter main window
                    else: # when comment is not less than 250 characters return tkinter error message
                        messagebox.showerror("Comment","Comment has to be less than 250 characters") 
                else: # level has to be 1 or 2 if not return tkinter error message
                    messagebox.showerror("Level", "Test Level cannot be left blank") 
            else: # type has to be 1 or 2 if not return tkinter error message
                messagebox.showerror("Type", "Test Type cannot be left blank")
    except: # if the user doesn't input a date in the format set then return tkinter error message
        messagebox.showerror("Date", "Date Format should be YYYY-MM-DD and not left blank")
