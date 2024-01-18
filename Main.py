import sqlite3
import datetime
from tabulate import tabulate  # pip install tabulate

# Create connection with task.db file
con = sqlite3.connect("task.db")
# Create cursor object that can work with SQL commands
cursor = con.cursor()

# Create tasks table if that doesnt exists
# .execute() - execute SQL command to database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    id integer primary key autoincrement,
    task_date date not null,
    start_time time,
    end_time time,
    task text,
    completed boolean default false
    )
""")

# function to show all tasks
def show_tasks():
    # define global variables (that created outside of function)
    global con, cursor
    # create date object of today date
    today = datetime.datetime.now()
    # calculate start of the week by using function timedelta
    startofweek = today - datetime.timedelta(days = today.weekday())
    # create list of date objects of current week
    weekdates = [startofweek + datetime.timedelta(days = i) for i in range(7)]

    # for every date in list
    for date in weekdates:
        # create a string in this format "yyyy-mm-dd" for database usage
        strdate = date.strftime("%Y-%m-%d")
        # print current date day name
        print(date.strftime("%A"))
        # select all tasks by current date and sort tasks by start time
        cursor.execute(f"""
            SELECT * FROM tasks
            WHERE task_date = '{strdate}'
            ORDER BY start_time;
        """)
        # read result from cursor (database)
        rows = cursor.fetchall()
        # if no results present
        if len(rows) <= 0:
            print("\tNo tasks")
        else:
            # auto tabulation to fancy print data
            print( tabulate( rows, headers= ['ID', 'Date', 'Start', 'End', 'Task', 'Completed'] ) )
        # print new line
        print()

# function to add new task
def add_task():
    # define global variables (that created outside of function)
    global con, cursor
    # input all required data
    year = input("input a year: ")
    month = input("input a month: ")
    day = input("input a day: ")
    task = input("input a task: ")
    start_time = input("input start time: ")
    end_time = input("input end time: ")

    # create tuple with all data
    data = (f"{year}-{month}-{day}", start_time, end_time, task)
    # "prepared" sql query to insert new record in DB
    cursor.execute("""
        INSERT INTO tasks(task_date,start_time,end_time,task)
        VALUES
        (?,?,?,?);
    """, data) # question marks replaced by data from "data" variable
    # save inserted data in DB
    con.commit()

# function to delete task
def delete_task():
    # define global variables (that created outside of function)
    global con, cursor
    # input task id to delete
    id = input("Input task id to delete: ")
    # sql delete command, delete by id because each task have unique id
    cursor.execute(f"""
        DELETE FROM tasks WHERE id = {id};
    """)
    # save changes
    con.commit()

# function to edit task
def edit_task():
    # define global variables (that created outside of function)
    global con, cursor
    # input all required data
    id = input("Input task id to edit: ")
    year = input("input a year: ")
    month = input("input a month: ")
    day = input("input a day: ")
    task = input("input a task: ")
    start_time = input("input start time: ")
    end_time = input("input end time: ")

    # create tuple with all data
    data = (f"{year}-{month}-{day}", start_time, end_time, task, id)
    # "prepared" sql query to update records in DB by id
    cursor.execute("""
        UPDATE tasks SET
        task_date = ?,start_time = ?,end_time = ?,task = ?
        WHERE id = ?;
    """, data) # question marks replaced by data from "data" variable
    # save changes
    con.commit()

# function to mark task as completed
def mark_as_completed():
    # define global variables (that created outside of function)
    global con, cursor
    # input task id to mark as complete
    id = input("Input task id to mark as complete: ")
    # sql query to update record field in DB by id
    cursor.execute(f"""
        UPDATE tasks SET
        completed = 1
        WHERE id = {id};
    """)
    # save changes
    con.commit()

# infinite loop
while True:
    # print info to user
    print('Select action:')
    print('\t1: Show this week\'s tasks')
    print('\t2: Add task')
    print('\t3: Mark task as completed')
    print('\t4: Edit task')
    print('\t5: Delete task')
    print('\t6: Exit')
    # read user choice
    choice = int(input('Choice: '))
    # if wrong number - skip iteration (reask)
    if choice < 1 or choice > 6:
        print('Wrong action number!')
        continue # skip iteration

    # depending on choice - call one of functions
    if choice == 1:
        show_tasks()
    elif choice == 2:
        add_task()
    elif choice == 3:
        mark_as_completed()
    elif choice == 4:
        edit_task()
    elif choice == 5:
        delete_task()
    elif choice == 6:
        break # end loop


# close connection to DB
con.close()
