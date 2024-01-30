
CREATE DATABASE db_hosts;
USE db_hosts;

CREATE TABLE end_device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(15) NOT NULL,
    mac_address VARCHAR(17) NOT NULL,
    longitude FLOAT,
    latitude FLOAT
);

CREATE TABLE iot_device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mac VARCHAR(255) NOT NULL,
    temp FLOAT,
    time TIMESTAMP
);

INSERT INTO end_device (name, ip_address, mac_address, longitude, latitude) VALUES
    ('Device1', '192.168.1.1', '00:11:22:33:44:55', NULL, NULL),
    ('Device2', '192.168.1.2', 'AA:BB:CC:DD:EE:FF', NULL, NULL),
    ('Device3', '192.168.1.3', '11:22:33:44:55:66', NULL, NULL);

INSERT INTO iot_device (mac, temp, time) VALUES
    ('00:11:22:33:44:55', 25.5, '2022-01-22 12:30:00'),
    ('AA:BB:CC:DD:EE:FF', 22.0, '2022-01-22 13:15:00'),
    ('11:22:33:44:55:66', 23.8, '2022-01-22 14:45:00');
