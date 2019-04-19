from create_connection import cursor

# This function takes in the username and school to return
# the details of the user
# It sets header and result as global variables so that they can be used for the
# update widgets function in the main file
# it formats the header and result to pretty the print that is returned
def view_info(user, school):
    global header
    global result
    header = ("Forename", "Surname", "Age", "Class")
    widths = [len(cell) for cell in header]
    result = "blank"

    if school is "Student":
        view = ("SELECT Forename,Surname,Age,Class FROM Students WHERE username = ?")
        cursor.execute(view, [(user)])
        student_check = cursor.fetchone()
        for i, cell in enumerate(student_check):
            widths[i] = max(len(str(cell)), widths[i])
        formatted_row = '       '.join('{:%d}' % width for width in widths)
        header = formatted_row.format(*header)
        result = formatted_row.format(*student_check)
        return "S"
    elif school is "Teacher":
        view = ("SELECT Forename,Surname,Age,Class FROM Teachers WHERE username = ?")
        cursor.execute(view, [(user)])
        teacher_check = cursor.fetchone()
        for i, cell in enumerate(teacher_check):
            widths[i] = max(len(str(cell)), widths[i])

        formatted_row = '       '.join('{:%d}' % width for width in widths)
        header = formatted_row.format(*header)
        result = formatted_row.format(*teacher_check)
        return "T"
