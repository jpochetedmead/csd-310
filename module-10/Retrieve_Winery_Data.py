import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Database Connection
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()
    print("\n✅ Connected to BacchusWinery database successfully.\n")

except mysql.connector.Error as err:
    print(f"\n❌ Error: {err}")
    exit()

# Function to display table data with column names
def display_table(table_name):
    try:
        print(f"\n--- {table_name} ---")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # Get column names

        # Print column headers
        print(" | ".join(column_names))
        print("-" * 80)

        # Print table data
        for row in rows:
            print(" | ".join(str(item) for item in row))

    except mysql.connector.Error as err:
        print(f"\n❌ Error retrieving data from {table_name}: {err}")

# List of tables to display
tables = [
    "Department", "Employee", "WorkHours", "Wine", "Supplier",
    "SupplyOrder", "Inventory", "Distributor", "SalesTransaction", "WineDistributor"
]

# Display all tables
for table in tables:
    display_table(table)

# Close the connection
cursor.close()
conn.close()
print("\n✅ Database connection closed.\n")
