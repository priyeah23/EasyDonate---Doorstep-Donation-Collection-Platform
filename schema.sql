CREATE DATABASE IF NOT EXISTS easydonate_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE easydonate_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    donor_name VARCHAR(120) NOT NULL,
    category ENUM('Clothes','Books','Furniture','Electronics','Food','Other') NOT NULL,
    description TEXT NOT NULL,
    quantity INT NOT NULL,
    pickup_date DATE NOT NULL,
    pickup_time TIME NOT NULL,
    address TEXT NOT NULL,
    status ENUM('Submitted','Scheduled','Collected','Delivered') NOT NULL DEFAULT 'Submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_donations_user FOREIGN KEY (user_id) REFERENCES users(id)
      ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(254) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
