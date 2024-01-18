import sqlite3

con = sqlite3.connect("task.db")
cursor = con.cursor()

cursor.execute("""
    INSERT INTO tasks(task_date,start_time,end_time,task)
    VALUES
    ('2024-01-16','15:20:10','16:50:10','Complete a project');
""")

con.commit()
