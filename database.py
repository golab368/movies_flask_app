import os
import psycopg2
from dotenv import load_dotenv

CREATE_TEST_TABLE = "CREATE TABLE IF NOT EXISTS favorite(id SERIAL PRIMARY KEY, favorite_movie TEXT UNIQUE);"
INSERT_IN_TABLE = "INSERT INTO favorite(favorite_movie) VALUES (%s) ON CONFLICT (favorite_movie) DO NOTHING;"
SELECT_TABLE = "SELECT * FROM favorite;"
SELECT_FAVORITE_FROM_TABLE ="SELECT favorite_movie FROM favorite;"
DELETE_FROM_FAVORITE = "DELETE FROM favorite WHERE favorite_movie = (%s);"

load_dotenv()

database_uri = os.environ["DATABASE_URI"]
connection = psycopg2.connect(database_uri)


with connection:
    with connection.cursor() as cursor:
        cursor.execute(CREATE_TEST_TABLE)

def insert_data(favorite_movie):
    with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_IN_TABLE, (favorite_movie,),)

def show_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TABLE)
            return cursor.fetchall()

def delete_from_favorite(favorite_movie):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(DELETE_FROM_FAVORITE, (favorite_movie,),)

def show_favorite():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_FAVORITE_FROM_TABLE)
            all = [i[0] for i in cursor.fetchall()]
            return all
