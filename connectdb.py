import mysql.connector

def connectDB():
    con = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'giuxethongminh'
    )
    return con