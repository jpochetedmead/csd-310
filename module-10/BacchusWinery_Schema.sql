-- Create the database
CREATE DATABASE IF NOT EXISTS BacchusWinery;
USE BacchusWinery;

-- Create Department Table
CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL
);

-- Create Employee Table
CREATE TABLE Employee (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(100),
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Create Work Hours Table
CREATE TABLE WorkHours (
    WorkHoursID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT,
    WorkDate DATE NOT NULL,
    HoursWorked INT CHECK (HoursWorked >= 0),
    LogTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

-- Create Wine Table (Updated)
CREATE TABLE Wine (
    WineID INT AUTO_INCREMENT PRIMARY KEY,
    WineName VARCHAR(100) NOT NULL,
    WineType ENUM('Merlot', 'Cabernet', 'Chablis', 'Chardonnay') NOT NULL,
    ProductionQuantity INT CHECK (ProductionQuantity >= 0)
);

-- Create Supplier Table (Updated)
CREATE TABLE Supplier (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(255),
    ProductSupplied ENUM('Bottles & Corks', 'Labels & Boxes', 'Vats & Tubing') NOT NULL
);

-- Create Supply Order Table
CREATE TABLE SupplyOrder (
    SupplyOrderID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierID INT,
    WineID INT,
    QuantityOrdered INT CHECK (QuantityOrdered > 0),
    OrderDate DATE NOT NULL,
    ExpectedDeliveryDate DATE,
    ActualDeliveryDate DATE,
    OrderStatus ENUM('Pending', 'Delivered', 'Delayed') DEFAULT 'Pending',
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)
);

-- Create Inventory Table
CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    WineID INT NOT NULL,
    StockQuantity INT NOT NULL CHECK (StockQuantity >= 0),
    LastUpdated DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)
);

-- Create Distributor Table
CREATE TABLE Distributor (
    DistributorID INT AUTO_INCREMENT PRIMARY KEY,
    DistributorName VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(255)
);

-- Create Sales Transaction Table
CREATE TABLE SalesTransaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    DistributorID INT,
    WineID INT,
    QuantitySold INT CHECK (QuantitySold > 0),
    SalePrice DECIMAL(10,2),
    SaleDate DATE NOT NULL,
    PaymentStatus ENUM('Paid', 'Pending', 'Refunded') DEFAULT 'Pending',
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID),
    FOREIGN KEY (WineID) REFERENCES Wine(WineID)
);

-- Create Wine Distributor Table (Associative Table)
CREATE TABLE WineDistributor (
    WineDistributorID INT AUTO_INCREMENT PRIMARY KEY,
    WineID INT,
    DistributorID INT,
    FOREIGN KEY (WineID) REFERENCES Wine(WineID),
    FOREIGN KEY (DistributorID) REFERENCES Distributor(DistributorID)
);

-- Insert Sample Data

-- Departments
INSERT INTO Department (DepartmentName) VALUES 
('Finance'), ('Marketing'), ('Production'), ('Distribution');

-- Employees
INSERT INTO Employee (Name, Role, DepartmentID) VALUES 
('Janet Collins', 'Finance Manager', 1),
('Roz Murphy', 'Marketing Head', 2),
('Bob Ulrich', 'Marketing Assistant', 2),
('Henry Doyle', 'Production Manager', 3),
('Maria Costanza', 'Distribution Manager', 4),
('Stan Bacchus', 'Owner', NULL);

-- Work Hours
INSERT INTO WorkHours (EmployeeID, WorkDate, HoursWorked) VALUES 
(1, '2024-06-01', 8),
(2, '2024-06-02', 9),
(3, '2024-06-03', 7),
(4, '2024-06-04', 10),
(5, '2024-06-05', 8),
(6, '2024-06-06', 12);

-- Suppliers (Updated)
INSERT INTO Supplier (SupplierName, ContactInfo, ProductSupplied) VALUES 
('Glass Bottles Inc.', 'bottles@supplier.com', 'Bottles & Corks'),
('Label Masters', 'labels@supplier.com', 'Labels & Boxes'),
('Vats & More Co.', 'vats@supplier.com', 'Vats & Tubing');

-- Wine (Updated)
INSERT INTO Wine (WineName, WineType, ProductionQuantity) VALUES 
('Merlot', 'Merlot', 500),
('Cabernet Sauvignon', 'Cabernet', 700),
('Chablis Classic', 'Chablis', 400),
('Chardonnay Reserve', 'Chardonnay', 600);

-- Inventory
INSERT INTO Inventory (WineID, StockQuantity) VALUES 
(1, 500),
(2, 700),
(3, 400),
(4, 600);

-- Distributors
INSERT INTO Distributor (DistributorName, ContactInfo) VALUES 
('Elite Wines', 'elite@distributor.com'),
('Fine Wines Co.', 'fine@distributor.com'),
('Vineyard Distributors', 'vineyard@distributor.com');

-- Sales Transactions
INSERT INTO SalesTransaction (DistributorID, WineID, QuantitySold, SalePrice, SaleDate, PaymentStatus) VALUES 
(1, 1, 50, 12.99, '2024-06-07', 'Paid'),
(2, 2, 30, 15.99, '2024-06-08', 'Pending'),
(3, 3, 40, 10.99, '2024-06-09', 'Paid'),
(1, 4, 20, 13.99, '2024-06-10', 'Paid');

-- Wine Distributor Relations
INSERT INTO WineDistributor (WineID, DistributorID) VALUES 
(1, 1), 
(2, 2), 
(3, 3), 
(4, 1);