import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "dynamic_impact_tool")
        )
        print("MySQL connection successful")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection failed: {err}")
        raise
