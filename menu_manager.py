import psycopg2
from configparser import ConfigParser
from menu_item import MenuItem

class MenuManager:
    @classmethod
    def _get_db_connection(cls):
        config = ConfigParser()
        config.read('database.ini')
        params = config['postgresql']
        conn = psycopg2.connect(**params)
        return conn

    @classmethod
    def get_by_name(cls, item_name):
        conn = cls._get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Menu_Items WHERE item_name = %s;", (item_name,))
            result = cur.fetchone()
            if result:
                item_id, name, price = result
                item = MenuItem(name, price)
                item.item_id = item_id
                return item
            return None
        except psycopg2.Error as e:
            print(f"Erreur lors de la recherche par nom : {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def all_items(cls):
        conn = cls._get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Menu_Items;")
            results = cur.fetchall()
            items = []
            for item_id, name, price in results:
                item = MenuItem(name, price)
                item.item_id = item_id
                items.append(item)
            return items
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération de tous les articles : {e}")
            return []
        finally:
            cur.close()
            conn.close()