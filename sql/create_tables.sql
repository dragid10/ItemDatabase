-- Items table
CREATE TABLE Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Use INTEGER for primary key
    name VARCHAR(255) NOT NULL,
    barcode VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,            -- Use INTEGER for quantity
    type VARCHAR(35) NOT NULL
        CHECK (type IN ('Vinyl Record', 'Comic', 'Book', 'Other', 'Game', 'Technology')), -- Simulate ENUM with CHECK
    purchase_date DATE,
    warranty_link VARCHAR(255),
    INDEX(barcode)
);

-- Friends table
CREATE TABLE Friends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    INDEX(phone_number),
    INDEX(name)
);

-- Loans table
CREATE TABLE Loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (item_id) REFERENCES Items(id),
    FOREIGN KEY (friend_id) REFERENCES Friends(id),
    INDEX(item_id),
    INDEX(friend_id),
    INDEX(return_date)
);