import psycopg2

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
passwords = ["postgres", "admin", "root", "", "password", "1234"]

for pwd in passwords:
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=pwd)
        print(f"Success with password: '{pwd}'")
        conn.close()
        break
    except Exception as e:
        print(f"Failed with '{pwd}': {str(e).strip()}")
