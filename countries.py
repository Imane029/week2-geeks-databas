import requests
import psycopg2
import random
import sys


DB_NAME = "countries"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"  
DB_PORT = "5432"  

API_URL = "https://restcountries.com/v3.1/all"

def create_table(conn):
    """
    Cree la table 'countries' dans la base de donnees si elle n'existe pas deja.
    La table inclut des colonnes pour le nom, la capitale, le drapeau, la sous-region et la population.
    """
    try:
        cur = conn.cursor()
        print("Creation de la table 'countries'...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                capital VARCHAR(255),
                flag TEXT,
                subregion VARCHAR(255),
                population BIGINT
            );
        """)
        print("La table 'countries' a ete creee avec succes ou existe deja.")
        conn.commit()
    except (psycopg2.Error, Exception) as e:
        print(f"Erreur lors de la creation de la table : {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def get_random_countries_data(num_countries=10):
    """
    Recupere une liste de tous les pays de l'API REST Countries,
    selectionne un echantillon aleatoire de 10, et extrait les attributs requis.
    """
    print(f"Recuperation des donnees pour {num_countries} pays aleatoires...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  
        all_countries = response.json()

        
        random_countries = random.sample(all_countries, num_countries)
        
        country_list = []
        for country in random_countries:
            
            name = country.get('name', {}).get('common', 'N/A')
            capital = country.get('capital', ['N/A'])[0] if isinstance(country.get('capital'), list) and country.get('capital') else 'N/A'
            flag = country.get('flags', {}).get('svg', 'N/A')
            subregion = country.get('subregion', 'N/A')
            population = country.get('population', 0)

            country_list.append((name, capital, flag, subregion, population))
        
        print("Donnees des pays recuperees avec succes.")
        return country_list

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recuperation des donnees de l'API : {e}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")
        return []

def insert_countries_data(conn, countries_data):
    """
    Insere la liste des pays dans la table 'countries'.
    """
    if not countries_data:
        print("Aucune donnee de pays a inserer. Sortie.")
        return

    try:
        cur = conn.cursor()
        print("Insertion des donnees des pays dans la base de donnees...")
        
        insert_query = """
            INSERT INTO countries (name, capital, flag, subregion, population)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
        """

        
        cur.executemany(insert_query, countries_data)
        
        conn.commit()
        print(f"Insertion reussie de {cur.rowcount} nouveaux pays.")

    except (psycopg2.Error, Exception) as e:
        print(f"Erreur lors de l'insertion des donnees : {e}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

if __name__ == "__main__":
    try:
        
        print("Tentative de connexion a la base de donnees...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connexion reussie !")

       
        create_table(conn)

        
        countries_data = get_random_countries_data()

        
        insert_countries_data(conn, countries_data)

    except psycopg2.OperationalError as e:
        print(f"La connexion a echoue : {e}")
        print("Veuillez verifier les informations de connexion de votre base de donnees (DB_NAME, DB_USER, etc.)")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Connexion a la base de donnees fermee.")