import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="auth-db1576.hstgr.io",
            user="u726483483_alfa_user",
            password="Alfa25062026profissionalizantes",
            database="u726483483_alfa_portal",
            port=3306
        )
        if connection.is_connected():
            print("MYSQL CONECTADO!")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def get_cursor(connection):
    return connection.cursor(dictionary=True)