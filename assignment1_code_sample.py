import os
import pymysql
import subprocess
from urllib.request import urlopen

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_user_input():
    user_input = input("Enter your name: ").strip()
    if not user_input.isalpha():
        raise ValueError("Invalid name: must contain only letters.")
    return user_input


def send_email(to, subject, body):
    try:
        subprocess.run(["mail", "-s", subject, to], input=body.encode(), check=True)
    except Exception as e:
        print(f"Error sending email: {e}")


def get_data():
    url = "https://secure-api.com/get-data"
    try:
        response = urlopen(url)
        return response.read().decode()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (data, "Another Value"))
            connection.commit()
    except Exception as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    try:
        user_input = get_user_input()
        data = get_data()
        if data:
            save_to_db(data)
        send_email("admin@example.com", "User Input", user_input)
    except Exception as e:
        print(f"Unexpected error: {e}")
