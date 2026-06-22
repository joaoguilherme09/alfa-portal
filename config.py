import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'alfa-portal-secret-2026')

    MYSQL_HOST     = os.getenv('MYSQL_HOST')
    MYSQL_PORT     = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER     = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB       = os.getenv('MYSQL_DB')