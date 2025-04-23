import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DataBase():
    def __init__(self):
        self.mysqlConnection = None
        self.cursor = None
        
    
    def __enter__(self):
        self.mysqlConnection = mysql.connector.connect(
            host="localhost", #port 3306
            user="flaskproject",
            password=os.getenv("DB_PASSWORD"),
            database="db_info"
        )
        try:
            self.cursor = self.mysqlConnection.cursor()
            return self
        except mysql.connector.Error as error:
            print(f"Error while connecting to MySQL: {error}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.mysqlConnection:
            if exc_type is None:
                self.mysqlConnection.commit()
            else:
                self.mysqlConnection.rollback()
            self.mysqlConnection.close()