# from passlib.context import CryptContext
# 
# class UserDB():
#     username: str
#     first_name: str
#     last_name: str
#     phone_number: str
#     password: str

#     def __init__(self, username, first_name, last_name, phone_number, password):
#         self.username = username
#         self.first_name = first_name
#         self.last_name = last_name
#         self.phone_number = phone_number
#         self.password = password

# bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# users = {
#     "anthonytast": UserDB(
#         username="anthonytast",
#         first_name="Anthony",
#         last_name="Tast",
#         phone_number="631-925-7508",
#         password=bcrypt_context.hash("SuperSecretPW")
#     ),
#     "testuser": UserDB(
#         username="testuser",
#         first_name="Dev",
#         last_name="Tester",
#         phone_number="1-800",
#         password=bcrypt_context.hash("test")
#     )
# }

import sqlite3

DATABASE_NAME = "database/users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                password TEXT
            )
        ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()