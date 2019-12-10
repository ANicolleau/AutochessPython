import mysql.connector

database = mysql.connector.connect(user='root', password='root',
                                   host='127.0.0.1')
mycursor = database.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

database.close()
