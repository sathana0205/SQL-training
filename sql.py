import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="sathana",
    database="sathana"
)
if conn.is_connected():
   print("connection successfull")
else:
   print("connection failed")   