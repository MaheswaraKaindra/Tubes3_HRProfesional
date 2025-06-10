# src/data/setup_database.py

import mysql.connector
from mysql.connector import Error as MySQLError
import os

def setup_database():
    # Preventing the "NameError: name 'connection' is not defined" error
    connection = None
    cursor = None

    try:
        # Connect to MySQL server
        connection = mysql.connector.connect (
            host        = "localhost",
            user        = "root",
            password    = "meteor"
        )
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS HRProfesional_schema")
        cursor.execute("USE HRProfesional_schema")
        print("Database created.")

        # Use the database
        cursor.execute("USE HRProfesional_schema")

        # Read schema.sql
        sql_directory = os.path.dirname(__file__)
        schema_path = os.path.join(sql_directory, 'schema.sql')

        with open(schema_path, 'r') as file:
            schema_sql = file.read()

        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
        for stmt in statements:
            cursor.execute(stmt)
            print(f"Executed: {stmt.split()[0]}")    

        for stmt in statements:
            cursor.execute(stmt)
            print(f"Executed: {stmt.split()[0]}")

        # Debug print XD
        connection.commit()
        print("Database setup completed successfully.")


    except MySQLError as e:
        print(f"Error connecting to MySQL server: {e}")
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup script executed.")