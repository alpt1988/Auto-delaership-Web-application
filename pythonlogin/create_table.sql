
CREATE DATABASE test;
USE test;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Mafn2016@cu';

CREATE TABLE LoggedInUser (
  UserName varchar(16) NOT NULL,
  Password varchar(60) NOT NULL,
  FirstName varchar(100) NOT NULL,
  LastName varchar(100) NOT NULL,
  PRIMARY KEY (UserName)
);

CREATE TABLE InventoryClerk (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
      REFERENCES `LoggedInUser`(UserName) 
);

CREATE TABLE SalesPeople (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 

CREATE TABLE ServiceWriter (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 

CREATE TABLE Manager (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 

CREATE TABLE Owner (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 


-- Customer

CREATE TABLE Customer (
  CustomerID varchar(16)  NOT NULL,
  EmailAddress varchar(250) NULL,
  PhoneNumber varchar(250) NOT NULL,
  Address varchar(250) NOT NULL,
  City varchar(50) NOT NULL,
  State varchar(16) NOT NULL,
  PostalCode varchar(16) NOT NULL,
  PRIMARY KEY (CustomerID)
); 
  

CREATE TABLE Person (
  CustomerID varchar(16)  NOT NULL,
  DriverLicenseNumber varchar(250) NOT NULL,
  FirstName varchar(100) NOT NULL,
  LastName varchar(100) NOT NULL,
  PRIMARY KEY (DriverLicenseNumber),
  FOREIGN KEY (CustomerID)
    REFERENCES `Customer` (CustomerID) 
); 


CREATE TABLE Business (
  CustomerID varchar(16)  NOT NULL, 
  TaxIdentificationNumber varchar(250) NOT NULL,
  BusinessName varchar(100) NOT NULL,
  FirstName varchar(100) NOT NULL,
  LastName varchar(100) NOT NULL,
  Title varchar(100) NOT NULL,
  PRIMARY KEY (TaxIdentificationNumber),
  FOREIGN KEY (CustomerID)
    REFERENCES `Customer` (CustomerID) 
); 


-- Vehicle

CREATE TABLE Manufacturer (
  Name varchar(50) NOT NULL,
  PRIMARY KEY (Name)
); 


CREATE TABLE Truck (
  VIN char(17) NOT NULL,
  ModelName varchar(50) NOT NULL,
  ModelYear int NOT NULL,
  InvoicePrice double(10,2) NOT NULL,
  Description varchar(250) NULL,
  NumRearAxles int NOT NULL,
  CargoCoverType varchar(50) NULL,
  CargoCapacity float NOT NULL,
  ManufacturerName varchar(50) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (ManufacturerName) 
  	REFERENCES `Manufacturer` (Name)
); 


CREATE TABLE Convertible (
  VIN char(17) NOT NULL,
  ModelName varchar(50) NOT NULL,
  ModelYear int NOT NULL,
  InvoicePrice double(10,2) NOT NULL,
  Description varchar(250) NULL,
  RoofType varchar(50) NOT NULL,
  BackSeatCount int NOT NULL,
  ManufacturerName varchar(50) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (ManufacturerName) 
  	REFERENCES `Manufacturer` (Name)
); 


CREATE TABLE SUV (
  VIN char(17) NOT NULL,
  ModelName varchar(50) NOT NULL,
  ModelYear int NOT NULL,
  InvoicePrice double(10,2) NOT NULL,
  Description varchar(250) NULL,
  DriveTrainType varchar(50) NOT NULL,
  NumCupholders int NOT NULL,
  ManufacturerName varchar(50) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (ManufacturerName) 
  	REFERENCES `Manufacturer` (Name)
); 

  
CREATE TABLE Car (
  VIN char(17) NOT NULL,
  ModelName varchar(50) NOT NULL,
  ModelYear int NOT NULL,
  InvoicePrice double(10,2) NOT NULL,
  Description varchar(250) NULL,
  NumDoors int NOT NULL,
  ManufacturerName varchar(50) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (ManufacturerName) 
  	REFERENCES `Manufacturer` (Name)
); 


CREATE TABLE Van (
  VIN char(17) NOT NULL,
  ModelName varchar(50) NOT NULL,
  ModelYear int NOT NULL,
  InvoicePrice double(10,2) NOT NULL,
  Description varchar(250) NULL,
  HasDriverSideBackDoor boolean NOT NULL,
  ManufacturerName varchar(50) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (ManufacturerName) 
  	REFERENCES `Manufacturer` (Name)
); 


CREATE TABLE VehicleColor (
  VIN char(17) NOT NULL,
  Color varchar(50) NOT NULL,
  PRIMARY KEY (VIN, Color)
); 


CREATE TABLE AddVehicle (
  UserName varchar(16) NOT NULL,
  VIN char(17) NOT NULL,
  AddDate date NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (UserName) 
  	REFERENCES `LoggedInUser` (UserName)
); 


CREATE TABLE Purchase (
  VIN char(17) NOT NULL,
  CustomerID varchar(16)  NOT NULL,
  PurchaseDate date NOT NULL,
  SoldPrice double(10,2) NOT NULL,
  SalespeopleUsername varchar(16) NOT NULL,
  PRIMARY KEY (VIN),
  FOREIGN KEY (CustomerID) 
  	REFERENCES `Customer` (CustomerID),
  FOREIGN KEY (SalespeopleUsername) 
  	REFERENCES `LoggedInUser` (UserName)
); 

-- Repair

CREATE TABLE Repair (
  VIN char(17) NOT NULL,
  StartDate date NOT NULL,
  DateCompleted date NULL,
  Odometer float NOT NULL,
  CustomerID varchar(16)  NOT NULL,
  LaborCharges double(10,2) NOT NULL,
  UserName varchar(16) NOT NULL,
  Description varchar(100) NOT NULL,
  PRIMARY KEY (VIN, StartDate),
  FOREIGN KEY (UserName)
  	REFERENCES `LoggedInUser` (UserName),
  FOREIGN KEY (CustomerID)
  	REFERENCES `Customer` (CustomerID)
);


CREATE TABLE Part (
  VIN char(17) NOT NULL,
  StartDate date NOT NULL,
  PartNumber varchar(100) NOT NULL,
  VendorName varchar(60) NOT NULL,
  Quantity int NOT NULL,
  Price float NOT NULL,
  PRIMARY KEY (VIN, StartDate, PartNumber)
);

