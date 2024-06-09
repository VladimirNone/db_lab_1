CREATE DATABASE BankDB;
USE BankDB;

-- Table for Borrowers
CREATE TABLE Borrowers (
    borrower_id INT AUTO_INCREMENT PRIMARY KEY,
    tax_id VARCHAR(15),
    entity_type BOOLEAN,
    address VARCHAR(255),
    amount DECIMAL(15, 2),
    conditions TEXT,
    legal_notes TEXT,
    contract_list TEXT
);

-- Table for Individuals
CREATE TABLE Individuals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    middle_name VARCHAR(50),
    passport VARCHAR(20),
    tax_id VARCHAR(15),
    insurance_id VARCHAR(15),
    driver_license VARCHAR(20),
    additional_docs TEXT,
    note TEXT,
    borrower_id INT,
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);

-- Table for Loans
CREATE TABLE Loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    individual_id INT,
    amount DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    rate DECIMAL(5, 2),
    term INT,
    conditions TEXT,
    note TEXT,
    borrower_id INT,
    FOREIGN KEY (individual_id) REFERENCES Individuals(id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);

-- Table for BusinessLoans
CREATE TABLE BusinessLoans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT,
    individual_id INT,
    amount DECIMAL(15, 2),
    term INT,
    interest_rate DECIMAL(5, 2),
    conditions TEXT,
    note TEXT,
    borrower_id INT,
    FOREIGN KEY (individual_id) REFERENCES Individuals(id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);

-- Example entries for testing purposes
INSERT INTO Borrowers (tax_id, entity_type, address, amount, conditions, legal_notes, contract_list)
VALUES 
('123456789', TRUE, '123 Main St, Anytown, USA', 100000.00, 'Standard terms', 'No legal notes', 'Contract1, Contract2'),
('987654321', FALSE, '456 Elm St, Anytown, USA', 50000.00, 'Standard terms', 'No legal notes', 'Contract3, Contract4'),
('234567890', TRUE, '789 Oak St, Anytown, USA', 75000.00, 'Standard terms', 'No legal notes', 'Contract5, Contract6'),
('876543219', FALSE, '135 Pine St, Anytown, USA', 30000.00, 'Standard terms', 'No legal notes', 'Contract7, Contract8'),
('345678901', TRUE, '246 Birch St, Anytown, USA', 120000.00, 'Standard terms', 'No legal notes', 'Contract9, Contract10');

INSERT INTO Individuals (first_name, last_name, middle_name, passport, tax_id, insurance_id, driver_license, additional_docs, note, borrower_id)
VALUES 
('John', 'Doe', 'Michael', 'A1234567', '123456789', '987654321', 'D1234567', 'None', 'No remarks', 1),
('Jane', 'Smith', 'Anna', 'B1234567', '987654321', '123456789', 'E1234567', 'None', 'No remarks', 2),
('Alice', 'Brown', 'Marie', 'C1234567', '234567890', '876543210', 'F1234567', 'None', 'No remarks', 3),
('Bob', 'Johnson', 'David', 'D1234567', '876543219', '210987654', 'G1234567', 'None', 'No remarks', 4),
('Charlie', 'Williams', 'James', 'E1234567', '345678901', '345678912', 'H1234567', 'None', 'No remarks', 5);

INSERT INTO Loans (individual_id, amount, interest_rate, rate, term, conditions, note, borrower_id)
VALUES 
(1, 10000.00, 5.0, 3.5, 24, 'Standard terms', 'No remarks', 1),
(2, 20000.00, 6.0, 4.0, 36, 'Standard terms', 'No remarks', 2),
(3, 15000.00, 4.5, 3.0, 18, 'Standard terms', 'No remarks', 3),
(4, 25000.00, 5.5, 3.8, 48, 'Standard terms', 'No remarks', 4),
(5, 30000.00, 6.5, 4.2, 60, 'Standard terms', 'No remarks', 5);

INSERT INTO BusinessLoans (organization_id, individual_id, amount, term, interest_rate, conditions, note, borrower_id)
VALUES 
(1, 1, 50000.00, 48, 5.5, 'Business loan terms', 'No remarks', 1),
(2, 2, 75000.00, 60, 6.0, 'Business loan terms', 'No remarks', 2),
(3, 3, 80000.00, 36, 5.0, 'Business loan terms', 'No remarks', 3),
(4, 4, 90000.00, 72, 6.5, 'Business loan terms', 'No remarks', 4),
(5, 5, 100000.00, 84, 7.0, 'Business loan terms', 'No remarks', 5);
