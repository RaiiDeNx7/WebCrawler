import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Establish connection
def get_connection():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

# Create table if not exists
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            url TEXT PRIMARY KEY,
            recipe_data TEXT,
            last_crawled TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Insert or update recipe
def insert_or_update_recipe(url, recipe_data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO recipes (url, recipe_data, last_crawled)
        VALUES (%s, %s, %s)
        ON CONFLICT (url)
        DO UPDATE SET recipe_data = EXCLUDED.recipe_data,
                      last_crawled = EXCLUDED.last_crawled;
    ''', (url, recipe_data, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

# Read recipe by URL
def read_recipe(url):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT url, recipe_data, last_crawled FROM recipes WHERE url = %s;", (url,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

# Example usage
if __name__ == '__main__':
    create_table()
    insert_or_update_recipe("https://example.com/recipe1", "Sample recipe content")
    recipe = read_recipe("https://example.com/recipe1")
    print(recipe)
