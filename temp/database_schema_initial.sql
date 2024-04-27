CREATE DATABASE RoomDatabase;

USE RoomDatabase;

CREATE TABLE Rooms (
    RoomNumber INT,
    BuildingName VARCHAR(255),
    RoomLatitude DECIMAL(10, 7),
    RoomLongitude DECIMAL(10, 7),
    RoomSize INT,
    Beds INT,
    Individuals INT,
    ViewDescription VARCHAR(255)
);

