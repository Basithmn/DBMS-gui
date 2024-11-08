create database bus;
use bus;
CREATE TABLE Employee1 (
    employee_name VARCHAR(20),
    E_id INT PRIMARY KEY,
    salary INT,
    date_of_joining DATE
);

CREATE TABLE Employee21 (
    E_id INT,
    phone BIGINT,
    PRIMARY KEY (E_id, phone),
    FOREIGN KEY (E_id) REFERENCES Employee1(E_id) ON DELETE CASCADE
);

CREATE TABLE E221 (
    E_id INT PRIMARY KEY,
    House_name VARCHAR(20),
    PinCode INT,
    Landmark VARCHAR(20),
    FOREIGN KEY (E_id) REFERENCES Employee1(E_id) ON DELETE CASCADE
);

CREATE TABLE E222 (
    PinCode INT PRIMARY KEY,
    City VARCHAR(20),
    District VARCHAR(20)
);

CREATE TABLE Depot1 (
    Depot_ID INT PRIMARY KEY,
    Capacity INT
);

CREATE TABLE Depot2 (
    Depot_ID INT PRIMARY KEY,
    place VARCHAR(20),
    pincode INT,
    district VARCHAR(20),
    FOREIGN KEY (Depot_ID) REFERENCES Depot1(Depot_ID) ON DELETE CASCADE
);

CREATE TABLE Route12 (
    Duration INT PRIMARY KEY,
    RefreshmentTime INT
);

CREATE TABLE Route11 (
    RouteID INT PRIMARY KEY,
    Destination VARCHAR(20),
    Distance INT,
    TypeOfService VARCHAR(20),
    Duration INT
);

CREATE TABLE Route2 (
    RouteID INT,
    Mainstops VARCHAR(20),
    PRIMARY KEY (RouteID, Mainstops),
    FOREIGN KEY (RouteID) REFERENCES Route11(RouteID) ON DELETE CASCADE
);

CREATE TABLE Bus (
    Bonnet_No VARCHAR(20) PRIMARY KEY,
    Registeration_No VARCHAR(20),
    depot_id int,
    Capacity INT,
    Status VARCHAR(20),
    Type VARCHAR(20) check (Type in ('Ordinary','Fast Passenger','Super Fast','Super Express','Super Deluxe','Garuda','Minnal','Low Floor'))
);


CREATE TABLE Works_for (
    employee_id INT,
    depot_id INT,
    PRIMARY KEY (employee_id, depot_id),
    FOREIGN KEY (employee_id) REFERENCES Employee1(E_id) ON DELETE CASCADE,
    FOREIGN KEY (depot_id) REFERENCES Depot1(Depot_ID) ON DELETE CASCADE
);

CREATE TABLE Works_In (
    E_ID INT,
    Bonnet_No VARCHAR(20),
    ShiftType VARCHAR(20) check (ShiftType in('General','Morning','Evening','Night')),
    Date DATE,
    PRIMARY KEY (E_ID, Bonnet_No, Date),
    FOREIGN KEY (E_ID) REFERENCES Employee1(E_id) ON DELETE CASCADE,
    FOREIGN KEY (Bonnet_No) REFERENCES Bus(Bonnet_No) ON DELETE CASCADE
);



CREATE TABLE GoesThrough (
    Bonnet_No VARCHAR(20),
    Route_ID INT,
    PRIMARY KEY (Bonnet_No, Route_ID),
    FOREIGN KEY (Bonnet_No) REFERENCES Bus(Bonnet_No) ON DELETE CASCADE,
    FOREIGN KEY (Route_ID) REFERENCES Route11(RouteID) ON DELETE CASCADE
);

CREATE TABLE StartsFrom1 (
    Route_ID INT PRIMARY KEY,
    Depot_ID INT,
    FOREIGN KEY (Depot_ID) REFERENCES Depot1(Depot_ID) ON DELETE CASCADE
);

CREATE TABLE StartsFrom2 (
    Route_ID INT,
    PortionNo INT,
    PRIMARY KEY (Route_ID, PortionNo),
    FOREIGN KEY (Route_ID) REFERENCES Route11(RouteID) ON DELETE CASCADE
);


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL,
    status ENUM('approved', 'pending', 'rejected') DEFAULT 'pending',
    name VARCHAR(100) NOT NULL,         -- Added name field
    email VARCHAR(100) NOT NULL UNIQUE  -- Added email field with unique constraint
);

insert into users values(1,'admin','admin123','admin','approved','Aparna','kovaparna@gmail.com');
select * from route11;
select * from bus;
use bus;
select * from depot1;
