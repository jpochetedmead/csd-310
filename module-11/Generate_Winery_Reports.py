import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Connection
try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor()
    print("\n✅ Successfully connected to the Bacchus Winery database.\n")

except mysql.connector.Error as err:
    print(f"\n❌ Database connection error: {err}\n")
    exit()

# Queries for reports
queries = {
    "Supplier Delivery Performance": """
        SELECT s.SupplierName, so.ExpectedDeliveryDate, so.ActualDeliveryDate, 
               DATEDIFF(so.ActualDeliveryDate, so.ExpectedDeliveryDate) AS DelayDays
        FROM SupplyOrder so
        JOIN Supplier s ON so.SupplierID = s.SupplierID
        ORDER BY DelayDays DESC;
    """,
    
    "Wine Sales Trends": """
        SELECT w.WineName, d.DistributorName, SUM(st.QuantitySold) AS TotalQuantity, 
               SUM(st.SalePrice * st.QuantitySold) AS TotalRevenue
        FROM SalesTransaction st
        JOIN Wine w ON st.WineID = w.WineID
        JOIN Distributor d ON st.DistributorID = d.DistributorID
        GROUP BY w.WineID, d.DistributorID
        ORDER BY TotalRevenue DESC;
    """,
    
    "Employee Work Hours by Quarter": """
        SELECT 
            e.Name AS EmployeeName, 
            e.Role, 
            e.DepartmentID, 
            CONCAT('Q', QUARTER(w.WorkDate), ' ', YEAR(w.WorkDate)) AS Quarter,
            SUM(w.HoursWorked) AS TotalHoursWorked
        FROM WorkHours w
        JOIN Employee e ON w.EmployeeID = e.EmployeeID
        WHERE w.WorkDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY e.EmployeeID, Quarter
        ORDER BY e.Name, Quarter;
    """
}

# Function to execute and display queries
def display_report(report_name, query):
    """Executes a SQL query and prints the results in a formatted way."""
    try:
        print(f"\n📊 --- {report_name} ---")
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Print column headers
        print(" | ".join(column_names))
        print("-" * 80)

        # Print data rows
        for row in rows:
            print(" | ".join(str(item) for item in row))
    
    except mysql.connector.Error as err:
        print(f"\n❌ Error retrieving {report_name}: {err}\n")

# Run reports
for report_name, query in queries.items():
    display_report(report_name, query)

# Close connection
cursor.close()
conn.close()
print("\n✅ Database connection closed.\n")