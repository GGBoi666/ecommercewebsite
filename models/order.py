from database import get_db_connection

class Order:
    @staticmethod
    def create_order(user_id, total_price, cart_items):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO orders (user_id, total_price, status) VALUES (?, ?, ?)', (user_id, total_price, 'Pending'))
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, item['id'], item['quantity']))
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_orders():
        conn = get_db_connection()
        orders = conn.execute('SELECT * FROM orders').fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_user_orders(user_id):
        conn = get_db_connection()
        orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()
        return orders

    @staticmethod
    def get_total_sales():
        conn = get_db_connection()
        total = conn.execute('SELECT SUM(total_price) FROM orders').fetchone()[0]
        conn.close()
        return total

    @staticmethod
    def get_pending_order_count():
        conn = get_db_connection()
        pending = conn.execute('SELECT COUNT(*) FROM orders WHERE status = "Pending"').fetchone()[0]
        conn.close()
        return pending
