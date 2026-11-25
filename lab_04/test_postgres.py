import psycopg2
from psycopg2 import sql

DB_USER = "appuser"
DB_PASSWORD = "supersecret"
DB_HOST = "127.0.0.1"  #localhost
DB_PORT = "5432"
DB_NAME = "appdb"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("PostgreSQL Connected successfully!")
    print(f"PostgreSQL version: {version[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"PostgreSQL Connection failed: {e}")
