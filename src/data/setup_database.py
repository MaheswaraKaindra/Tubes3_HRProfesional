# src/data/setup_database.py

import mysql.connector
from mysql.connector import Error as MySQLError
import os

def setup_database():
    # Preventing the "NameError: name 'connection' is not defined" error
    connection = None

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect (
            host        = "localhost",
            user        = "hr_admin",
            password    = ""
        )
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS HRProfesional_schema")
        print("Database created.")

        # Use the database
        cursor.execute("USE HRProfesional_schema")

        # Read schema.sql
        sql_directory = os.path.dirname(__file__)
        schema_path = os.path.join(sql_directory, 'schema.sql')

        with open(schema_path, 'r') as file:
            schema_sql = file.read().split(';')

        for command in schema_sql:
            if command.strip() != '':
                try:
                    cursor.execute(command)
                    print(f"\nExecuted command: {command.strip()}")
                except MySQLError as e:
                    print(f"\nError executing command: {command.strip()}\nError: {e}")
        connection.commit()
        print("Database setup completed successfully.")

    except MySQLError as e:
        print(f"Error connecting to MySQL server: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup script executed.")