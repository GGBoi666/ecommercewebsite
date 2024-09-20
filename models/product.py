from database import get_db_connection

class Product:
    @staticmethod
    def add_product(name, price, stock, description, image_url, category_id):
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, price, stock, description, image_url, category_id) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, price, stock, description, image_url, category_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_products(sort_by='name'):
        conn = get_db_connection()
        query = f'SELECT * FROM products ORDER BY {sort_by}'
        products = conn.execute(query).fetchall()
        conn.close()
        return products

    @staticmethod
    def get_product_by_id(product_id):
        conn = get_db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return product

    @staticmethod
    def get_low_stock_products(threshold=5):
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products WHERE stock <= ?', (threshold,)).fetchall()
        conn.close()
        return products

    @staticmethod
    def delete_product(product_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
