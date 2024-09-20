from database import get_db_connection

class User:
    @staticmethod
    def register(username, password, is_admin=False):
        conn = get_db_connection()
        
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            return False  # User already exists

        conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def login(username, password):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        return user
