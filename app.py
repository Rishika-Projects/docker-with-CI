import os
import sqlite3
import requests

from fastapi import FastAPI

app = FastAPI()

DB_PATH = os.getenv("DB_PATH", "/data/app.db")


@app.get("/")
def home():
    return {
        "message": "FastAPI running with Docker Compose v1 Testing",
        "database": DB_PATH
    }


@app.get("/create")
def create_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    return {"message": "Database and users table created"}


@app.get("/users")
def get_users():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    connection.close()

    return {"users": users}


@app.get("/helper")
def call_helper():
    response = requests.get("http://helper:9000")
    return {
        "helper_response": response.text
    }