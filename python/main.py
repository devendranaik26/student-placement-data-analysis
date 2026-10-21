import os
import mysql.connector
from dotenv import load_dotenv

# Load credentials from the .env file
load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    if connection.is_connected():
        print("MySQL connected successfully!")
        print("Database: student_placement_db")

    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)
