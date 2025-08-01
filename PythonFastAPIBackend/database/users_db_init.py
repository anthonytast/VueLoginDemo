from passlib.context import CryptContext
import sqlite3

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
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

    # adds initial user to the db
    cursor.execute("SELECT 1 FROM users WHERE username = 'anthonytast'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (username, first_name, last_name, phone_number, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'testuser',
            'Dev',
            'Test',
            '1-800',
            bcrypt_context.hash('test')
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()