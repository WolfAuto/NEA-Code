import pandas as pd
from tkinter import messagebox
import datetime as dt
import random
import re
from login_backend import get_id_student
from create_connection import cursor, cursor1, db

current_date = dt.date.today().strftime("%Y-%m-%d") # current date

# two database for storing pure and applied results
create_pure_table = """CREATE TABLE IF NOT EXISTS pure_results
(maths_id INTEGER PRIMARY KEY, user_id INTEGER, level TEXT , score INTEGER ,
total_questions INTEGER, Correct INTEGER, Incorrect INTEGER,  time_stamp DATE,
FOREIGN KEY (user_id) REFERENCES Students(ID))"""
create_applied_table = """CREATE TABLE IF NOT EXISTS applied_results
(maths_id INTEGER PRIMARY KEY, user_id INTEGER, level TEXT , score INTEGER ,total_questions INTEGER,
Correct INTEGER, Incorrect INTEGER, time_stamp DATE,FOREIGN KEY (user_id) REFERENCES Students(ID))"""
cursor.execute(create_pure_table)
cursor.execute(create_applied_table)
create_question_table = """CREATE TABLE IF NOT EXISTS
maths_questions(question_id INTEGER PRIMARY KEY, test_type TEXT,test_level TEXT, question TEXT, answer TEXT) """
cursor.execute(create_question_table)
db.commit() # saves changes made to db file

question_store = [] # list for storing all the questions attempted

def make_question(question_text, type, level, answer): # function for making questions
    # sql for inserting a question into maths questions
    insert_question = ( """INSERT INTO maths_questions 
                    (test_type, test_level, question, answer)
                    VALUES (?, ?, ?, ?) """)
    answer_string = str(answer) # makes sure answer is in string form
    match = re.match("[\w,\s,.]*$",question_text) # ensures a space and alphanumeric characters in question text
    if match is not None and (len(question_text) >= 50): # question text has to be longer than 50
        if type is 1: # when type is 1 question type is pure
            question_type = "Pure"
            if level is 1: # when level is 1 question type is AS
                if answer_string.isalnum() is True: # ensures question meets alphanumeric validation 
                    question_level = "AS"
                    
                    cursor.execute(insert_question, [(question_type), # executes inserts question into db
                                                     (question_level),
                                                     (question_text),
                                                     (str(answer))])
                    db.commit() # saves changes made and returns true
                    return True
                else: # error message when answer doesn't meet alpha-numeric validation
                    messagebox.showerror(
                        "Answer", "Answer cannot be left blank and no spaces in answer")
            elif level is 2: # when level is 2 question type is A2
                if answer_string.isalnum() is True: # ensures question meets alphanumeric validation 
                    question_level = "A2"
                    
                    cursor.execute(insert_question, [(question_type), # executes insert question into db
                                                     (question_level),
                                                     (question_text),
                                                     (str(answer))])
                    db.commit() # saves changes made and returns true
                    return True
                else: # error message when answer doesn't meet alpha-numeric validation
                    messagebox.showerror(
                        "Answer", "Answer cannot be left blank and no spaces in answer")
            else: # level can only be 1 or 2 if not then return error message
                messagebox.showerror("Level", "Level cannot be left blank")
        elif type is 2: # when type is 2 then question type is applied
            question_type = "Applied"
            if level is 1: # when level is 1 question type is AS
                if answer_string.isalnum() is True: # ensures question meets alphanumeric validation 
                    question_level = "AS"
                    cursor.execute(insert_question, [(question_type), # executes insert question into db
                                                     (question_level),
                                                     (question_text),
                                                     (str(answer))])
                    db.commit() # saves changes made and returns true
                    return True
                else: # error message when answer doesn't meet alpha-numeric validation
                    messagebox.showerror(
                        "Answer", "Answer cannot be left blank and no spaces in answer")
            elif level is 2:
                if answer_string.isalnum() is True: # error message when answer doesn't meet alpha-numeric validation
                    question_level = "A2"
                    cursor.execute(insert_question, [(question_type), # executes insert question into db
                                                     (question_level),
                                                     (question_text),
                                                     (str(answer))])
                    db.commit() # saves changes made and returns true
                    return True
                else: # error message when answer doesn't meet alpha-numeric validation
                    messagebox.showerror(
                        "Answer", "Answer cannot be left blank and no spaces in answer")
            else: # when level is not 1 or 2 then return error message
                messagebox.showerror("Level", "Level cannot be left blank")
        else: # when type is not 1 or 2 then return error message
            messagebox.showerror("Type", "Type cannot be left blank")
    else: # when question doesn't meet the length requirement or regex expression return error message
        messagebox.showerror("Question", "Question cannot be left blank and make a reasonable question")


def random_num(total):
    while len(question_store) is not total: # loop for running
        data = random.randint(0, total-1) #creates a random number between 0 and total
        if (data in question_store) is False: # if number is not in the list then
            question_store.append(data) # append to list
            return data # return the value received
    return "stop"


def get_question(type, level): # takes in params type and level
    query = "SELECT question,answer FROM maths_questions WHERE test_type = ? AND test_level = ?" # sql query
    resp = pd.read_sql_query(query, db, params=[(type), (level)]) # converts sql query into a pandas dataframe
    query1 = "SELECT COUNT(question_id) FROM maths_questions WHERE test_type=? AND test_level=?"
    # gets total amount of questions for the specific type and level (amount of records that met the requirements)
    cursor1.execute(query1, [(type), (level)]) # calculates the value of above query
    total = cursor1.fetchone()[0] # stores the value to a variable total
    rand_num = random_num(total) # runs the function to generate a non-duplicate random number
    if rand_num is not "stop": # continues until rand_num is stop
        return [resp["question"][rand_num], resp["Answer"][rand_num]] # returns the question and answer 
    else:
        return ["No more Questions", "END"]


def compare_answers(user_input, actual_answer): # takes in user input an actual answer
    if user_input.find(",") is not -1: # looks for , between answers
        mylist = user_input.split(",") # creates a list by spliting the valeues using commas
        mylist.sort(key=int) # sorts the list in numerical order
        user_input = ",".join(mylist) # creates the string back by joining the values using a comma from the list
        if str(user_input) == str(actual_answer): # compares the two strings
            return True # if same then true
        else:
            return False # if not the same then false
    else: # done if the answer is separated by commas
        if str(user_input) == str(actual_answer): # compare strings
            return True # if same then true
        else:
            return False # if not then same then false

def end_loop(loop, user, correct, incorrect, score, level, total):
    if total == 0: # no questions attempted
        question_store.clear() # clears all values in question store
        return False
    else:
        store_id = get_id_student(user) # gets the user id using get_student
        total = len(question_store)
        # gets the len of question store for total questions attempted
        if loop is "Pure": # if loop is pure
            sql = """INSERT INTO pure_results (user_id,level, score, Correct, Incorrect,total_questions, time_stamp)
                    VALUES (?, ?, ?, ?, ?, ?,?) """ # sql for inserting a record into pure_results table
            cursor.execute(sql, [(store_id), (level), (score), (correct),
                                 (incorrect), (total), (current_date)]) # executes the statment with python variales 

        elif loop is "Applied": # if loop is applied
            sql = """INSERT INTO applied_results (user_id,level, score, Correct, Incorrect,total_questions, time_stamp)
                    VALUES (?, ?, ?, ?, ?, ?,?) """ # sql for inserting a record into applied_results table
            cursor.execute(sql, [(store_id), (level), (score), (correct),
                                 (incorrect), (total), (current_date)]) # executes the statment with python variales 
        db.commit() # saves changes made to database file
        question_store.clear() # removes all the values in question_store
        return True
