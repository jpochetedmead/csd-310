import mysql.connector
from dotenv import dotenv_values  # Load environment variables

# Load credentials from .env file
secrets = dotenv_values(".env")

# Database configuration using .env values
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Function to display films
def show_films(cursor, title):
    """
    Executes an INNER JOIN query on the film table 
    to display selected film details in a formatted manner.
    """
    query = """
        SELECT 
            film.film_name AS Name, 
            film.film_director AS Director, 
            genre.genre_name AS Genre, 
            studio.studio_name AS 'Studio Name' 
        FROM film 
        INNER JOIN genre ON film.genre_id = genre.genre_id 
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    
    cursor.execute(query)
    films = cursor.fetchall()

    # Print formatted title
    print(f"\n-- {title} --")

    # Iterate over the dataset and display results
    for film in films:
        print(f"\nFilm Name: {film[0]}")
        print(f"Director: {film[1]}")
        print(f"Genre Name ID: {film[2]}")  # Matches the format from the expected output
        print(f"Studio Name: {film[3]}")

# Try connecting to MySQL
try:
    db = mysql.connector.connect(**config)
    print(f"\n✅ Connected to MySQL database: {config['database']} on host {config['host']}")

    cursor = db.cursor()

    # Step 1: Display initial films
    show_films(cursor, "DISPLAYING FILMS")

    # Step 2: Insert a new movie ("Interstellar" instead of "Star Wars")
    insert_query = """
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    new_movie = ("Interstellar", "2014", 169, "Christopher Nolan", 3, 2)  
    # studio_id = 3 (Universal Pictures), genre_id = 2 (SciFi)
    cursor.execute(insert_query, new_movie)
    db.commit()

    # Step 3: Display films after insertion
    show_films(cursor, "DISPLAYING FILMS AFTER INSERTION")

    # Step 4: Update the film "Alien" to be a Horror film
    update_query = "UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'"
    cursor.execute(update_query)
    db.commit()

    # Step 5: Display films after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATING 'ALIEN' TO HORROR")

    # Step 6: Delete the movie "Gladiator"
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
    cursor.execute(delete_query)
    db.commit()

    # Step 7: Display films after deletion
    show_films(cursor, "DISPLAYING FILMS AFTER DELETING 'GLADIATOR'")

    input("\n🔹 Press any key to close the connection...")  # Keeps terminal open for review

except mysql.connector.Error as err:
    print(f"❌ ERROR: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\n🔌 MySQL connection closed.")