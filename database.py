import sqlite3
import hashlib

class AuthUtils:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    @staticmethod
    def is_valid_username(username):
        # username can't be empty
        return len(username) > 0

    @staticmethod
    def is_valid_password(password):
        # password must be at least 4 characters long and contain both letters and numbers
        return len(password) >= 4 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password) 

class Database:
    def __init__(self, db_name='my_web.db'):
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
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )""" 
        )
        
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )""" 
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS literature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                title TEXT,
                author TEXT,
                abstract TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )""" 
        )

        self.conn.commit()

    def create_user(self, username: str, password: str):
        hashed_password = AuthUtils.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return self.cursor.lastrowid  # Return row ID of the newly created user
        except sqlite3.IntegrityError:
            return None  # Return None if failed to create user (e.g., username already exists)

    def get_user_id(self, username: str):
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def authenticate_user(self, username: str, password: str):
        hashed_password = AuthUtils.hash_password(password)
        self.cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return self.cursor.fetchone()

    def add_note(self, user_id: int, user_input="", llm_response=""):
        self.cursor.execute("INSERT INTO notes (user_id, user_input, llm_response) VALUES (?, ?, ?)", (user_id, user_input, llm_response))
        self.conn.commit()
        return True

    def get_notes(self, user_id: int):
        self.cursor.execute("SELECT id, user_input, llm_response FROM notes WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_origin_note(self, note_id):
        self.cursor.execute("SELECT id, user_input, llm_response FROM notes WHERE id = ?", (note_id,))
        return self.cursor.fetchall()
    def delete_note(self, note_id: int):
        self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        return True

    def add_todo(self, user_id: int, task: str):
        self.cursor.execute("INSERT INTO todos (user_id, task) VALUES (?, ?)", (user_id, task))
        self.conn.commit()
        return True

    def get_todos(self, user_id: int):
        self.cursor.execute("SELECT id, task, completed FROM todos WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
    
    def delete_todo(self, todo_id:int, task: str):
        self.cursor.execute("DELETE FROM todos WHERE id = ? and task = ?", (todo_id, task))
        self.conn.commit()
        return True

    def add_literature(self, user_id: int, date: str, title: str, author: str, abstract: str):
        self.cursor.execute("INSERT INTO literature (user_id, date, title, author, abstract) VALUES (?, ?, ?, ?, ?)", (user_id, date, title, author, abstract))
        self.conn.commit()
        return True

    def get_literature(self, user_id: int):
        self.cursor.execute("SELECT id, date, title, author, abstract FROM literature WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def delete_literature(self, literature_id: int):
        self.cursor.execute("DELETE FROM literature WHERE id = ?", (literature_id,))
        self.conn.commit()
        return True

    def update_literature(self, literature_id: int, date: str, title: str, author: str, abstract: str):
        self.cursor.execute("UPDATE literature SET date = ?, title = ?, author = ?, abstract = ? WHERE id = ?", (date, title, author, abstract, literature_id))
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()

db = Database()

if __name__ == "__main__":
    db = Database()
    db.create_tables()
    db.close()
    print("✅ Tables created successfully")
