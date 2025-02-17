import mysql.connector  # MySQL connection
from dotenv import dotenv_values  # Load environment variables

# Load credentials from .env file
secrets = dotenv_values(".env")

# Database configuration using .env values
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # Enables warnings for debugging
}

# Try connecting to MySQL
try:
    db = mysql.connector.connect(**config)
    print(f"\n✅ Connected to MySQL database: {config['database']} on host {config['host']}")

    cursor = db.cursor()

    # Query 1: Select all fields from the "studio" table
    print("\n-- DISPLAYING Studio RECORDS --")
    query1 = "SELECT studio_id, studio_name FROM studio;"
    cursor.execute(query1)
    for studio in cursor.fetchall():
        print(f"\nStudio ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}")

    # Query 2: Select all fields from the "genre" table
    print("\n-- DISPLAYING Genre RECORDS --")
    query2 = "SELECT genre_id, genre_name FROM genre;"
    cursor.execute(query2)
    for genre in cursor.fetchall():
        print(f"\nGenre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}")

    # Query 3: Select films with runtime < 2 hours
    print("\n-- DISPLAYING Short Film RECORDS --")
    query3 = "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;"
    cursor.execute(query3)
    for film in cursor.fetchall():
        print(f"\nFilm Name: {film[0]}")
        print(f"Runtime: {film[1]}")

    # Query 4: List films grouped by director
    print("\n-- DISPLAYING Director RECORDS in Order --")
    query4 = "SELECT film_name, film_director FROM film ORDER BY film_director;"
    cursor.execute(query4)
    for film in cursor.fetchall():
        print(f"\nFilm Name: {film[0]}")
        print(f"Director: {film[1]}")

    input("\n🔹 Press any key to close the connection...")  # Keeps terminal open for review

except mysql.connector.Error as err:
    print(f"❌ ERROR: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\n🔌 MySQL connection closed.")
