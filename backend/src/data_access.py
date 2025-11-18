import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="temp"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM your_table;")

for row in cursor.fetchall():
    print(row)

conn.close()
