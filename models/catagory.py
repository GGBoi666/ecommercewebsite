from database import get_db_connection

class Catagory:
    @staticmethod
    def add_catagory(name):
        conn = get_db_connection()
        conn.execute('INSERT INTO catagories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_catagories():
        conn = get_db_connection()
        catagories = conn.execute('SELECT * FROM catagories').fetchall()
        conn.close()
        return catagories

    @staticmethod
    def delete_catagory(catagory_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM catagories WHERE id = ?', (catagory_id,))
        conn.commit()
        conn.close()
