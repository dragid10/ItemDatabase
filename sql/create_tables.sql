-- Create the Items table with an ENUM for item types
CREATE TABLE Items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    type ENUM('Vinyl Record', 'Comic', 'Book', 'Other') NOT NULL,
    purchase_date DATE,
    warranty_link VARCHAR(255)
);

-- Create the Friends table
CREATE TABLE Friends (
    friend_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255)
);

-- Create the Loans table
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    friend_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (item_id) REFERENCES Items(item_id),
    FOREIGN KEY (friend_id) REFERENCES Friends(friend_id)
);