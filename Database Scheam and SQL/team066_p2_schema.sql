create database Project;
use Project;

CREATE TABLE LoggedInUser (
  UserName varchar(16) NOT NULL,
  Password varchar(60) NOT NULL,
  FirstName varchar(100) NOT NULL,
  LastName varchar(100) NOT NULL,
  PRIMARY KEY (UserName)
);
INSERT INTO `LoggedInUser` (`UserName`, `FirstName`, `LastName`,`Password`) VALUES
  ('InventoryClerk1', 'UserFName1', 'UserLName1','password1'),
  ('InventoryClerk2', 'UserFName2', 'UserLName2','password2'),
  ('InventoryClerk3', 'UserFName3', 'UserLName3','password3'),
  ('InventoryClerk4', 'UserFName4', 'UserLName4','password4'),
  ('InventoryClerk5', 'UserFName5', 'UserLName5','password5'),
  ('SalesPeople1', 'UserFName11', 'UserLName11','password1'),
  ('SalesPeople2', 'UserFName12', 'UserLName12','password2'),
  ('SalesPeople3', 'UserFName13', 'UserLName13','password3'),
  ('SalesPeople4', 'UserFName14', 'UserLName14','password4'),
  ('SalesPeople5', 'UserFName15', 'UserLName15','password5'),
  ('ServiceWriter1', 'UserFName16', 'UserLName16','password1'),
  ('ServiceWriter2', 'UserFName17', 'UserLName17','password2'),
  ('ServiceWriter3', 'UserFName18', 'UserLName18','password3'),
  ('ServiceWriter4', 'UserFName19', 'UserLName19','password4'),
  ('ServiceWriter5', 'UserFName20', 'UserLName20','password5'),
  ('Manager1', 'UserFName21', 'UserLName21','password1'),
  ('Manager2', 'UserFName22', 'UserLName22','password2'),
  ('Roland', 'Roland', 'Owner','password2');

CREATE TABLE InventoryClerk (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
      REFERENCES `LoggedInUser`(UserName) 
);
insert into `InventoryClerk` (`UserName`) values
('InventoryClerk1'),
('InventoryClerk2'),
('InventoryClerk3'),
('InventoryClerk4'),
('InventoryClerk5');

CREATE TABLE SalesPeople (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 
insert into `SalesPeople` (`UserName`) values
('SalesPeople1'),
('SalesPeople2'),
('SalesPeople3'),
('SalesPeople4'),
('SalesPeople5');

CREATE TABLE ServiceWriter (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 
insert into `ServiceWriter` (`UserName`) values
('ServiceWriter1'),
('ServiceWriter2'),
('ServiceWriter3'),
('ServiceWriter4'),
('ServiceWriter5');

CREATE TABLE Manager (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 
insert into `Manager` (`UserName`) values
('Manager1'),
('Manager2');

CREATE TABLE Owner (
  UserName varchar(16) NOT NULL,
  PRIMARY KEY (UserName),
  FOREIGN KEY (UserName)
    REFERENCES `LoggedInUser`(UserName) 
); 
insert into `Owner` (`UserName`) values
('Roland');
-- Customer

CREATE TABLE Customer (
  CustomerID varchar(16)  NOT NULL, # modify datatype from int(16) to varchar(16) (previously: CustomerID varchar(16) unsigned NOT NULL AUTO_INCREMENT,)
  EmailAddress varchar(250) NULL,
  PhoneNumber varchar(250) NOT NULL,
  Address varchar(250) NOT NULL,
  City varchar(16) NOT NULL,
  State varchar(16) NOT NULL,
  PostalCode varchar(16) NOT NULL,
  PRIMARY KEY (CustomerID)
); 
INSERT INTO `Customer` (`CustomerID`, `EmailAddress`, `PhoneNumber`,`Address`,`City`,`State`,`PostalCode`) VALUES
  ('customer01', 'customer01@gmail.com', '6462360001','340 1st street','Jersey City','NJ','07301'),
  ('customer02', 'customer02@gmail.com', '6462360002','340 2nd street','New York City','NY','10025'),
  ('customer03', 'customer03@gmail.com', '6462360003','340 3rd street','Jersey City','NJ','07303'),
  ('customer04', 'customer04@gmail.com', '6462360004','340 4th street','Jersey City','NJ','07310'),
  ('customer05', 'customer05@gmail.com', '6462360005','340 5th street','Jersey City','NJ','07305'),
  ('customer06', 'customer06@gmail.com', '6462360006','340 6th street','Jersey City','NJ','07306'),
  ('customer07', 'customer07@gmail.com', '6462360007','340 7th street','Jersey City','NJ','07307'),
  ('customer08', 'customer08@gmail.com', '6462360008','340 8th street','Jersey City','NJ','07308');
  

CREATE TABLE Person (
  CustomerID varchar(16)  NOT NULL, # modify datatype from int(16) to varchar(16) (previously: CustomerID varchar(16) unsigned NOT NULL AUTO_INCREMENT,)
  DriverLicenseNumber varchar(250) NOT NULL,
  FirstName varchar(100) NOT NULL,
  LastName varchar(100) NOT NULL,
  PRIMARY KEY (DriverLicenseNumber),
  FOREIGN KEY (CustomerID)
    REFERENCES `Customer` (CustomerID) 
); 
insert into `Person` (`CustomerID`,`DriverLicenseNumber`,`FirstName`,`LastName`) values
('customer01','L00000000001','cus_first_01','cus_last_01'),
('customer02','L00000000002','cus_first_02','cus_last_02'),
('customer03','L00000000003','cus_first_03','cus_last_03'),
('customer04','L00000000004','cus_first_04','cus_last_04'),
('customer05','L00000000005','cus_first_05','cus_last_05');


CREATE TABLE Business (
  CustomerID varchar(16)  NOT NULL, # modify datatype from int(16) to varchar(16) (previously: CustomerID varchar(16) unsigned NOT NULL AUTO_INCREMENT,)
  TaxIdentificationNumber varchar(250) NOT NULL,
  BusinessName varchar(100) NOT NULL,
  Name varchar(100) NOT NULL,
  Title varchar(100) NOT NULL,
  PRIMARY KEY (TaxIdentificationNumber),
  FOREIGN KEY (CustomerID)
    REFERENCES `Customer` (CustomerID) 
); 
insert into `Business` (`CustomerID`,`TaxIdentificationNumber`,`BusinessName`,`Name`,`Title`) values
('customer06','TIN006','BusinessCustomer06','Busi_name_06','Mr.'),
('customer07','TIN007','BusinessCustomer07','Busi_name_07','Ms.'),
('customer08','TIN008','BusinessCustomer08','Busi_name_08','Mrs.');
-- Vehicle

CREATE TABLE Manufacturer (
  Name varchar(50) NOT NULL,
  PRIMARY KEY (Name)
); 
INSERT INTO `Manufacturer` (`Name`) VALUES
  ('Honda'),
  ('Toyota'),
  ('Chevy'),
  ('Volvo'),
  ('BMW'),
  ('Benz'),
  ('Lexus'),
  ('VW'),
  ('Tesla');

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
INSERT INTO `Truck` (`VIN`, `ModelName`,`ModelYear`,`InvoicePrice`,`Description`,`NumRearAxles`,
					`CargoCoverType`,`CargoCapacity`,`ManufacturerName`) VALUES
  ('TruckVIN001', 'TruckModelName001', '2010','10000.20','Truck Description 001','1','CargoCoverType001','5.00','HONDA'),
  ('TruckVIN002', 'TruckModelName002', '2013','20000.55','Truck Description 002','2','CargoCoverType002','7.00','TOYOTA'),
  ('TruckVIN003', 'TruckModelName003', '2017','50000.45','Truck Description 003','1','CargoCoverType003','900','HONDA'),
  ('TruckVIN004', 'TruckModelName004', '2020','70000.45','Truck Description 004','4','CargoCoverType004','20','CHEVY'),
  ('TruckVIN005', 'TruckModelName005', '2021','80000.45','Truck Description 005','2','CargoCoverType005','100','Volvo');

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
INSERT INTO `Convertible` (`VIN`, `ModelName`,`ModelYear`,`InvoicePrice`,`Description`,`RoofType`,
					`BackSeatCount`,`ManufacturerName`) VALUES
  ('ConvertibleVIN001', 'ConvertibleModelName001', '2010','10000.20','Convertible Description 001','RoofType001','2','Benz'),
  ('ConvertibleVIN002', 'ConvertibleModelName002', '2013','20000.55','Convertible Description 002','RoofType002','2','BMW'),
  ('ConvertibleVIN003', 'ConvertibleModelName003', '2017','50000.45','Convertible Description 003','RoofType003','0','BMW'),
  ('ConvertibleVIN004', 'ConvertibleModelName004', '2020','70000.45','Convertible Description 004','RoofType001','1','CHEVY'),
  ('ConvertibleVIN005', 'ConvertibleModelName005', '2021','80000.45','Convertible Description 005','RoofType002','2','Volvo');

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
INSERT INTO `SUV` (`VIN`, `ModelName`,`ModelYear`,`InvoicePrice`,`Description`,`DriveTrainType`,
					`NumCupholders`,`ManufacturerName`) VALUES
  ('SUVVIN001', 'SUVModelName001', '2010','10000.20','SUV Description 001','DriveTrainType001','2','Benz'),
  ('SUVVIN002', 'SUVModelName002', '2013','20000.55','SUV Description 002','DriveTrainType002','2','BMW'),
  ('SUVVIN003', 'SUVModelName003', '2017','50000.45','SUV Description 003','DriveTrainType003','0','BMW'),
  ('SUVVIN004', 'SUVModelName004', '2020','70000.45','SUV Description 004','DriveTrainType001','1','CHEVY'),
  ('SUVVIN005', 'SUVModelName005', '2021','80000.45','SUV Description 005','DriveTrainType002','2','Volvo');
  
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
INSERT INTO `Car` (`VIN`, `ModelName`,`ModelYear`,`InvoicePrice`,`Description`,`NumDoors`,`ManufacturerName`) VALUES
  ('CarVIN001', 'CarModelName001', '2010','10000.20','Car Description 001','2','Benz'),
  ('CarVIN002', 'CarModelName002', '2013','20000.55','Car Description 002','2','BMW'),
  ('CarVIN003', 'CarModelName003', '2017','50000.45','Car Description 003','4','BMW'),
  ('CarVIN004', 'CarModelName004', '2020','70000.45','Car Description 004','4','CHEVY'),
  ('CarVIN005', 'CarModelName005', '2021','80000.45','Car Description 005','2','Volvo');

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
INSERT INTO `Van` (`VIN`, `ModelName`,`ModelYear`,`InvoicePrice`,`Description`,`HasDriverSideBackDoor`,`ManufacturerName`) VALUES
  ('VanVIN001', 'VanModelName001', '2010','10000.20','Van Description 001','1','Benz'),
  ('VanVIN002', 'VanModelName002', '2013','20000.55','Van Description 002','1','BMW'),
  ('VanVIN003', 'VanModelName003', '2017','50000.45','Van Description 003','0','BMW'),
  ('VanVIN004', 'VanModelName004', '2020','70000.45','Van Description 004','0','CHEVY'),
  ('VanVIN005', 'VanModelName005', '2021','80000.45','Van Description 005','1','Volvo');

CREATE TABLE VehicleColor (
  VIN char(17) NOT NULL,
  Color varchar(50) NOT NULL,
  PRIMARY KEY (VIN, Color)/*,
  FOREIGN KEY (VIN)
  	REFERENCES `Truck` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Convertible` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `SUV` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Van` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Car` (VIN)*/
); 
Insert into `VehicleColor` (`VIN`,`Color`) values
('VanVIN001','Aluminum'),
('VanVIN002','Beige'),
('VanVIN003','Black'),
('VanVIN004','Blue'),
('VanVIN005','Brown'),
('CarVIN001','Bronze'),
('CarVIN002','Claret'),
('CarVIN003','Copper'),
('CarVIN004','Cream'),
('CarVIN005','Gold'),
('SUVVIN001','Gray'),
('SUVVIN002','Green'),
('SUVVIN003','Maroon'),
('SUVVIN004','Metallic'),
('SUVVIN005','Navy'),
('ConvertibleVIN001','Orange'),
('ConvertibleVIN002','Pink'),
('ConvertibleVIN003','Purple'),
('ConvertibleVIN004','Red'),
('ConvertibleVIN005','Rose'),
('TruckVIN001','Rust'),
('TruckVIN002','Silver'),
('TruckVIN003','Tan'),
('TruckVIN004','Turquoise'),
('TruckVIN005','White');


CREATE TABLE AddVehicle (
  UserName varchar(16) NOT NULL,
  VIN char(17) NOT NULL,
  AddDate date NOT NULL,
  PRIMARY KEY (UserName, VIN)/*,
  FOREIGN KEY (VIN) 
  	REFERENCES `Truck` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Convertible` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `SUV` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Van` (VIN),
  FOREIGN KEY (VIN)
  	REFERENCES `Car` (VIN),
  FOREIGN KEY (UserName) 
  	REFERENCES `InventoryClerk` (UserName)*/
); 
Insert into `AddVehicle` (`UserName`,`VIN`,`AddDate`) values
('InventoryClerk1','VanVIN001','20140618'),
('InventoryClerk2','VanVIN002','20140619'),
('InventoryClerk2','VanVIN003','20150618'),
('InventoryClerk1','VanVIN004','20170618'),
('InventoryClerk3','VanVIN005','20140818'),
('InventoryClerk1','CarVIN001','20200618'),
('InventoryClerk2','CarVIN002','20140620'),
('InventoryClerk3','CarVIN003','20140619'),
('InventoryClerk2','CarVIN004','20150205'),
('InventoryClerk3','CarVIN005','20210618'),
('InventoryClerk2','SUVVIN001','20120810'),
('InventoryClerk1','SUVVIN002','20140910'),
('InventoryClerk4','SUVVIN003','20120918'),
('InventoryClerk4','SUVVIN004','20140630'),
('InventoryClerk1','SUVVIN005','20120918'),
('InventoryClerk2','ConvertibleVIN001','20120920'),
('InventoryClerk5','ConvertibleVIN002','20150918'),
('InventoryClerk2','ConvertibleVIN003','20210918'),
('InventoryClerk1','ConvertibleVIN004','20150918'),
('InventoryClerk2','ConvertibleVIN005','20160911'),
('InventoryClerk1','TruckVIN001','20170923'),
('InventoryClerk2','TruckVIN002','20180123'),
('InventoryClerk5','TruckVIN003','20190811'),
('InventoryClerk1','TruckVIN004','20201111'),
('InventoryClerk5','TruckVIN005','20211011');

CREATE TABLE Purchase (
  VIN char(17) NOT NULL,
  CustomerID varchar(16)  NOT NULL, # modify datatype from int(16) to varchar(16) (previously: CustomerID int(16) unsigned NOT NULL,)
  PurchaseDate date NOT NULL,
  SoldPrice double(10,2) NOT NULL,
  SalespeopleUsername varchar(16) NOT NULL,
  PRIMARY KEY (VIN, CustomerID),
  FOREIGN KEY (CustomerID) 
  	REFERENCES `Customer` (CustomerID),
  FOREIGN KEY (SalespeopleUsername) 
  	REFERENCES `SalesPeople` (UserName)
); 
insert into `Purchase` (`VIN`,`CustomerID`,`PurchaseDate`,`SoldPrice`,`SalespeopleUsername`) values
('SUVVIN001','customer01','20201011','30000','SalesPeople1'),
('CarVIN003','customer03','20210810','40000','SalesPeople3'),
('VanVIN003','customer07','20190810','20000','SalesPeople1'),
('ConvertibleVIN003','customer07','20190812','20000','SalesPeople4'),
('TruckVIN003','customer08','20120810','40000','SalesPeople5');
-- Repair

CREATE TABLE Repair (
  VIN char(17) NOT NULL,
  StartDate date NOT NULL,
  DateCompleted date NULL,
  Odometer double(10,2) NOT NULL,
  CustomerID varchar(16)  NOT NULL, # modify datatype from int(16) to varchar(16) (previously: CustomerID int(16) unsigned NOT NULL,)
  LaborCharges double(10,2) NOT NULL,
  UserName varchar(16) NOT NULL,
  Description varchar(100) NOT NULL/*,
  PRIMARY KEY (VIN, StartDate),
  FOREIGN KEY (UserName)
  	REFERENCES `ServiceWriter` (UserName),
  FOREIGN KEY (CustomerID)
  	REFERENCES `Customer` (CustomerID)*/
);
insert into `Repair` (`VIN`,`StartDate`,`DateCompleted`,`Odometer`,`CustomerID`,`LaborCharges`,`UserName`,`Description`) values
('TruckVIN003','20150214','20150526','100000.56','customer01','500','ServiceWriter1','Repair description 001'),
('CarVIN003','20180214','20180526','200000.56','customer03','234.56','ServiceWriter3','Repair description 002'),
('ConvertibleVIN003','20160214','20160526','300000.56','customer03','300','ServiceWriter1','Repair description 003'),
('VanVIN003','20170214','20170526','700000.56','customer05','700','ServiceWriter4','Repair description 004'),
('SUVVIN003','20200214','20200526','800000.56','customer02','200','ServiceWriter5','Repair description 005'),
('SUVVIN003','20180214','20180526','600000.56','customer07','200','ServiceWriter3','Repair description 006');

CREATE TABLE Part (
  PartID varchar(100) NOT NULL,
  Quantity int(10) NOT NULL,
  VendorName varchar(60) NOT NULL,
  PartNumber varchar(100) NOT NULL,
  Price DOUBLE(10,2) NOT NULL,
  PRIMARY KEY (PartID)
);
insert into `Part` (`PartID`,`Quantity`,`VendorName`,`PartNumber`,`Price`) values
('Part001','1','VendorName001','000001','100.00'),
('Part002','2','VendorName002','000002','1200.00'),
('Part003','3','VendorName003','000003','300.00'),
('Part004','4','VendorName004','000004','400.00'),
('Part005','15','VendorName005','000005','500.00');
CREATE TABLE Need (
  VIN char(17) NOT NULL,
  StartDate date NOT NULL,
  PartID varchar(100) NOT NULL,
  PRIMARY KEY (VIN, StartDate, PartID)/*,
  FOREIGN KEY (VIN)
  	REFERENCES `Repair` (VIN),
  FOREIGN KEY (PartID)
  	REFERENCES `Part` (PartID)*/
);
insert into `Need` (`VIN`,`StartDate`,`PartID`) values
('SUVVIN003','20180214','Part005'),
('VanVIN003','20170214','Part002');


select VIN, ModelName, ModelYear, InvoicePrice, Description, NumRearAxles, CargoCoverType,CargoCapacity,ManufacturerName from Truck where Modelyear = '2010';
select * from Convertible;
select * from SUV;
select * from Van;
select * from Car;
select * from Truck where VIN = 'TruckVIN001';
select * from Convertible where VIN='ConvertibleVIN001';
select * from SUV where VIN='SUVVIN001';
select * from Van where VIN='CarVIN001';
select * from Car where VIN='VanVIN001';