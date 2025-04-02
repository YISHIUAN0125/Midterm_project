import sqlite3
import hashlib

class Database:
    def __init__(self, db_name='Midterm_project/my_web.db'): 
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )"""  
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_input TEXT,
                llm_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""" 
        )
        
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""" 
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS literature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                author TEXT,
                abstract TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""" 
        )

        self.conn.commit()
        return True

    def create_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True 
        except sqlite3.IntegrityError:
            return False
        finally:
            self.conn.commit() 

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        return user[0] if user else None 

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.close()
    print("✅ Table create successfully")
