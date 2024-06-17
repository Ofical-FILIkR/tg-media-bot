import sqlite3


connection = sqlite3.connect('db_user.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
tg_id INTEGER NOT NULL PRIMARY KEY,
username TEXT NOT NULL,
telephone TEXT NOT NULL
)
''')

cursor.execute('''
INSERT INTO Users (tg_id, username, telephone) VALUES
( 0, "name" , +70000000000)
''')

connection.commit()
connection.close()