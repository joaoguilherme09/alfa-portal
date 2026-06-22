import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="zephyr.proxy.rlwy.net",
            user="root",
            password="mesNlDsQeXxAYRfWdTOJOMvBvHRWixsE",
            database="railway",
            port=19496
        )
        if connection.is_connected():
            print("MYSQL CONECTADO!")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def get_cursor(connection):
    return connection.cursor(dictionary=True)