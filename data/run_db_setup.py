import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def setup_db():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if DB exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='nifty100'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE nifty100")
            print("Database 'nifty100' created.")
        else:
            print("Database 'nifty100' already exists.")
        
        cursor.close()
        conn.close()
        
        # Connect to nifty100 and run db_setup.sql
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname='nifty100', user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        with open('data/db_setup.sql', 'r') as f:
            cursor.execute(f.read())
        conn.commit()
        cursor.close()
        conn.close()
        print("Schema setup successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_db()
