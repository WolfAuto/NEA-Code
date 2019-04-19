from create_connection import cursor

# All of these functions gets all the students from the student table
# sort_gender does the sort starting will all the females and then male
# sort_age is sorted in ascending order
# get students is in ascending order of ID
# sort_surname,forename is in alphabetical order of surname and forename
# sort_class goes in number then letter order e.g 12C,12D,13C,13D
# all of these functions have a sql that is executed which is then returned as
# result
def get_students():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def sort_age():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students ORDER BY Age ASC """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def sort_surname():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students ORDER BY Surname"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def sort_class():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students ORDER BY class """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def sort_forename():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students ORDER BY Forename"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def sort_gender():
    sql = """ SELECT ID, Forename, Surname, Age, class, gender FROM students ORDER BY Gender"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
