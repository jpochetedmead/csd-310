import mysql.connector  # MySQL connection
from mysql.connector import errorcode
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
    print(f"\n✅ Database user {config['user']} connected to MySQL on host {config['host']} using database {config['database']}.")

    input("\n🔹 Press any key to continue...")  # Keeps the terminal open for review

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("❌ ERROR: Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("❌ ERROR: The specified database does not exist")
    else:
        print(f"❌ ERROR: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        db.close()
        print("\n🔌 MySQL connection closed.")