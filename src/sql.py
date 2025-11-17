import pymysql.cursors
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def create(use_db=True):
    try:
        credentials = st.session_state.get('db_credentials', {})
        params = dict(
            host=credentials.get('host') or os.getenv('DB_HOST', 'localhost'),
            port=int(credentials.get('port') or os.getenv('DB_PORT', 3306)),
            user=credentials.get('user') or os.getenv('DB_USER', 'your_username'),
            password=credentials.get('password') or os.getenv('DB_PASSWORD', 'your_password'),
            cursorclass=pymysql.cursors.DictCursor,
        )
        db_name = os.getenv('DB_NAME')
        if use_db and db_name:
            params['database'] = db_name
        return pymysql.connect(**params)
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

def check_database_exists(db_name=None):
    connection = create(use_db=False)
    if not connection:
        return False
    try:
        if not db_name:
            db_name = os.getenv('DB_NAME')
        with connection.cursor() as cursor:
            cursor.execute("show databases")
            databases = [row['Database'] for row in cursor.fetchall()]
            exists = db_name in databases
            return exists
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False
    finally:
        connection.close()

def initialize(db_name=None):
    connection = create(use_db=False)
    if not connection:
        raise RuntimeError("Failed to connect to the server (use_db=False).")
    try:
        if not db_name:
            db_name = os.getenv('DB_NAME')
        with connection.cursor() as cursor:
            cursor.execute(f"create database if not exists `{db_name}`")
            connection.commit()
            cursor.execute(f"use `{db_name}`")
            connection.commit()
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, 'r') as file:
                sql_commands = file.read()
                for command in sql_commands.split(';'):
                    command = command.strip()
                    if not command or 'create database' in command.lower() or command.lower().startswith('use'):
                        continue
                    cursor.execute(command)
            connection.commit()
    finally:
        connection.close()

def reinitialize(db_name=None):
    connection = create(use_db=False)
    if not connection:
        raise RuntimeError("Failed to connect to the server (use_db=False).")
    try:
        if not db_name:
            db_name = os.getenv('DB_NAME')
        with connection.cursor() as cursor:
            cursor.execute(f"""
                select concat('KILL ', id, ';') as kill_cmd
                from information_schema.processlist
                where db = '{db_name}' and id != connection_id()
            """)
            kill_commands = cursor.fetchall()
            for row in kill_commands:
                try:
                    cursor.execute(row['kill_cmd'])
                except Exception as e:
                    print(f"Error killing connection: {e}")
            connection.commit()
            cursor.execute(f"drop database if exists `{db_name}`")
            connection.commit()
            initialize()
    finally:
        connection.close()

def populate():
    connection = create(use_db=True)
    if not connection:
        raise RuntimeError("Failed to connect to the database (use_db=True).")
    try:
        populate_path = os.path.join(os.path.dirname(__file__), "populate.sql")
        with connection.cursor() as cursor:
            with open(populate_path, 'r') as file:
                sql_commands = file.read()
                for command in sql_commands.split(';'):
                    cmd = command.strip()
                    if not cmd:
                        continue
                    cursor.execute(cmd)
            connection.commit()
    finally:
        connection.close()

