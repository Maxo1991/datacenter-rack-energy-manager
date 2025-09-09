import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="db",
            user="root",
            password="rootpass",
            database="datacenter"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
        else:
            raise Exception("Failed connection to database")
    except Error as e:
        raise Exception(f"Connection error: {e}")
