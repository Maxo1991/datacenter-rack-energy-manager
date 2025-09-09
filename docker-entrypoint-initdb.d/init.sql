CREATE TABLE IF NOT EXISTS racks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    serial_number VARCHAR(100),
    capacity_units INT,
    max_power INT
);

CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    serial_number VARCHAR(100),
    units INT,
    power INT,
    rack_id INT NULL,
    CONSTRAINT fk_rack FOREIGN KEY (rack_id) REFERENCES racks(id) ON DELETE CASCADE  
);