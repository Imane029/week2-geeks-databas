import psycopg2
from configparser import ConfigParser

class MenuItem:
    def __init__(self, name, price):
        self.item_name = name
        self.item_price = price
        self.item_id = None

    def _get_db_connection(self):
        config = ConfigParser()
        config.read('database.ini')
        params = config['postgresql']
        conn = psycopg2.connect(**params)
        return conn

    def save(self):
        conn = self._get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Menu_Items (item_name, item_price) VALUES (%s, %s) RETURNING item_id;",
                        (self.item_name, self.item_price))
            self.item_id = cur.fetchone()[0]
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Erreur lors de la sauvegarde de l'article : {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    def delete(self):
        conn = self._get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Menu_Items WHERE item_name = %s;", (self.item_name,))
            conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Erreur lors de la suppression de l'article : {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    def update(self, new_name, new_price):
        conn = self._get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Menu_Items SET item_name = %s, item_price = %s WHERE item_name = %s;",
                        (new_name, new_price, self.item_name))
            conn.commit()
            self.item_name = new_name
            self.item_price = new_price
            return True
        except psycopg2.Error as e:
            print(f"Erreur lors de la mise à jour de l'article : {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()