from create_connection import cursor, cursor1, db # importing the db connection from create_connection
import matplotlib.pyplot as plt # python library modules used
import matplotlib.dates as mdates
import pandas as pd
plt.style.use(["bmh", "seaborn-talk"]) # sets the style for the graphs 

# All functions take in user_id to plot the graph about specific users  
def correct_graphs(user_id): 
    dates_pure = [] # lists that stores dates and correct from pure results
    correct_pure = []
    # sql for getting the dates and correct from table pure results in the db file
    # using the user_id
    sql_pure = """SELECT time_stamp,SUM(Correct) FROM pure_results 
                WHERE user_id = ? GROUP BY time_stamp"""
    cursor.execute(sql_pure, [(user_id)]) # executing the sql 
    for a in cursor.fetchall(): # storing the result in the pure lists
        dates_pure.append(a[0])
        correct_pure.append(a[1])
    dates_applied = [] # list that stores dates and correct from applied result
    correct_applied = []
    # sql for getting the dates and correct from table applied results
    # in the db file using the user_id

    sql_applied = """SELECT time_stamp, SUM(Correct) FROM applied_results
                    WHERE user_id = ? GROUP BY time_stamp"""
    cursor.execute(sql_applied, [(user_id)]) # executing the sql
    for b in cursor.fetchall():
        dates_applied.append(b[0])
        correct_applied.append(b[1]) # storing the result the applied lists

    plt.figure(1) # creates the figure for the graph to be plot
    plt.subplot(211) # creates a subplot for the pure graph 
    plt.plot(dates_pure,correct_pure) # plots the pure values on one subplot
    plt.ylabel("Questions Correct") # labels the y axis
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis 
    plt.title("Pure Maths Correct Progress") # puts a title on the graph

    plt.subplot(212) # creates another subplot for applied graph
    plt.plot(dates_applied, correct_applied, "-g")
    #plots the applied values on the other subplot and sets the line colour green
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis
    plt.ylabel("Questions Correct") # labels the y axis
    plt.title("Applied Maths Correct Progress") # puts a title on the graph

    plt.tight_layout() # changes the layout to be tight
    plt.show() # shows the graphs made
def incorrect_graphs(user_id):
    dates_pure = [] # four lists 2 for pure and 2 for applied
    incorrect_pure = []
    dates_applied = []
    incorrect_applied = []
    # Sql that perform the same task but on different tables pure_results and applied_results
    # using the user_id getting the incorrect values along with there respective date

    sql_pure = """SELECT time_stamp,SUM(Incorrect) FROM pure_results
                WHERE user_id = ? GROUP BY time_stamp"""
    sql_applied = """SELECT time_stamp, SUM(Incorrect) FROM applied_results
                    WHERE user_id = ? GROUP BY time_stamp"""
    cursor.execute(sql_pure, [(user_id)]) #executes the pure statement 
    for a in cursor.fetchall(): # appends all the values to the two pure lists
        dates_pure.append(a[0])
        incorrect_pure.append(a[1])
    cursor.execute(sql_applied, [(user_id)]) # executes the applied statement
    for b in cursor.fetchall(): # appends all the value to the two applied lists
        dates_applied.append(b[0])
        incorrect_applied.append(b[1])

    plt.figure(1) # creates the figure for the graph to be plot
    plt.subplot(211) # creates a subplot for the pure graph 
    plt.plot(dates_pure,incorrect_pure) # plots the pure values on one subplot
    plt.ylabel("Questions Incorrect") # labels the y axis
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis
    plt.title("Pure Maths Incorrect Progress") # puts a title on the graph

    plt.subplot(212) # creates another subplot for applied graph
    plt.plot(dates_applied, incorrect_applied, "-g")
    #plots the applied values on the other subplot and sets the line colour green
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis
    plt.ylabel("Questions Incorrect") # labels the y axis
    plt.title("Applied Maths Incorrect Progress") # puts a title on the graph

    plt.tight_layout()# changes the layout to be tight
    plt.show() # shows the graphs made

def total_graph_correct(user_id):
    dates = [] # Two lists one for dates the other for correct
    correct = []
    # Sql that combines correct (along with the date connected to it) from both tables into
    # one value and groups the dates together hence returning it back in order
    # using the user_id

    sql = """SELECT time_stamp,SUM(Correct) total FROM
(SELECT time_stamp,Correct FROM pure_results WHERE user_id = ?
UNION ALL SELECT time_stamp, Correct FROM applied_results WHERE user_id = ?)
t GROUP BY time_stamp"""
    cursor.execute(sql, [(user_id), (user_id)]) # executes th sql statement
    for a in cursor.fetchall(): # appends the results found to the two lists
        dates.append(a[0])
        correct.append(a[1])
        
    plt.plot(dates, correct, label="Total Correct Progress") # plots the data
                                                             # and sets a label on it
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis
    plt.ylabel("Questions Correct") # labels the y axis
    plt.title("A Level Maths Total Correct Progress") # gives the graph a title
    plt.figure(1).autofmt_xdate() # formats the x axis to prevent overlap on the figure
    plt.show() # shows the graph


def total_graph_incorrect(user_id):
    dates = [] # Two lists one for dates the other for incorrect
    incorrect = []
    # Sql that combines incorrect (along with the date connected to it)
    # from both tables into one value and groups the dates together
    # hence returning it back in order using the user_id

    sql = """SELECT time_stamp,SUM(Incorrect) total
FROM (SELECT time_stamp,Incorrect FROM pure_results WHERE user_id = ?
UNION ALL SELECT time_stamp, Incorrect FROM applied_results WHERE user_id = ?)
t GROUP BY time_stamp"""
    cursor.execute(sql, [(user_id), (user_id)])# executes th sql statement
    for a in cursor.fetchall(): # appends the results found to the two lists
        dates.append(a[0])
        incorrect.append(a[1])
        
    plt.figure(1) # creates the figure for the graph to be plot
    plt.plot(dates, incorrect, label="Incorrect Progess") # plots the data and sets a label on it
    plt.xlabel("Dates of Maths Question Attempted") # labels the x axis
    plt.ylabel("Incorrect Questions") # labels the y axis
    plt.title("A Level Maths Total Incorrect Progress") # gives the graph a title
    plt.figure(1).autofmt_xdate() # formats the x axis to prevent overlap
    plt.show() # shows the graph

def graph_total_questions(user_id):
    dates = [] # two lists one for dates the other for total questions
    total_questions = []
    # sql that combines total_question (along with the date connected to it)
    # from both tables into one value and groups the dates together
    # hence returning it back in order using the user_id
    
    sql = """SELECT time_stamp,SUM(total_questions) total
FROM (SELECT time_stamp,total_questions
FROM pure_results WHERE user_id = ?
UNION ALL SELECT time_stamp,total_questions
FROM applied_results WHERE user_id = ?) t GROUP BY time_stamp"""
    cursor.execute(sql, [(user_id), (user_id)]) # executes the sql 
    for a in cursor.fetchall(): # appends the data found to the two lists
        dates.append(a[0])
        total_questions.append(a[1])
        
    plt.figure(1) # creates the figure for the graph to be plot
    plt.plot(dates, total_questions) # plots the data on the figure
    plt.xlabel("Dates of Questions Attempted") # labels the x axis
    plt.ylabel("Total Questions Attempted") # labels the y axis
    plt.title("A Level Maths Total Questions Attempted") # gives the graph a title
    plt.figure(1).autofmt_xdate()# formats the x axis to prevent overlap
    plt.show() # shows the graph


def score_graph(user_id):
    dates = [] # two lists one for dates the other for total questions
    total_score = []
    # sql that combines score (along with the date connected to it)
    # from both tables into one value and groups the dates together
    # hence returning it back in order using the user_id
    
    sql = """SELECT time_stamp,SUM(score) total FROM
(SELECT time_stamp,score FROM pure_results WHERE user_id = ? UNION ALL SELECT time_stamp,score
FROM applied_results WHERE user_id = ?) t GROUP BY time_stamp"""
    cursor.execute(sql, [(user_id), (user_id)]) # executes sql statement
    for a in cursor.fetchall(): # appends the data to the two lists
        dates.append(a[0])
        total_score.append(a[1])
        
    plt.figure(1) # creates the figure for the graph to be plot
    plt.plot(dates, total_score) # plots the data on the figure
    plt.xlabel("Date") # labels the x axis
    plt.ylabel("Current Score") # labels the y axis
    plt.title("A level Score Progess") # gives the graph a title
    plt.figure(1).autofmt_xdate() # formats the x axis to prevent overlap
    plt.show() # shows the graph

def total_score(user_id):
     # sql that combines score  from both tables into one value
    sql = """SELECT SUM(score) total FROM
(SELECT score FROM pure_results WHERE user_id = ?
UNION ALL SELECT score FROM applied_results WHERE user_id = ?) t """
    
    # converting the sql into a pandas dataframe
    resp = pd.read_sql_query(sql, db, params=[(user_id), (user_id)])
    if resp["total"][0] is None: # condition that dataframe is empty
        return "No Score" # no score is returned
    
    else: # if data frame is not empty
        return resp.to_csv(None, header = False, index = False)
        # convert into a comma separate file with no header or index 
