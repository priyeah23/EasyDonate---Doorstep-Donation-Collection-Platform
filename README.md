# EasyDonate

**Give • Collect • Change Lives**

## Project Overview

EasyDonate is a donation management system designed to connect donors with NGOs and volunteer collection teams. It supports donation request submission, doorstep pickup coordination, and donation status tracking.

## Features

- User registration and login
- Donation request submission
- Doorstep pickup coordination
- NGO needs and donation categories
- Donation tracking and receipt generation
- Volunteer collection team coordination

## Key Modules

- **User Management Module:** Handles user registration and login authentication.
- **Donation Management Module:** Allows donors to submit and manage donation requests.
- **Pickup Coordination Module:** Supports organizing doorstep donation collection.
- **Donation Tracking Module:** Maintains donation status information and receipt details.
- **NGO and Volunteer Coordination Module:** Supports coordination between donors, NGOs, and collection teams.
- **Database Management Module:** Stores user details, donation records, and contact messages using MySQL.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** MySQL
- **Database Connectivity:** MySQL Connector for Python
- **Security:** Password hashing and session-based authentication

## Project Structure

- `app.py` – Flask backend and application routes
- `schema.sql` – MySQL database and table definitions
- `requirements.txt` – Required Python packages
- `templates/index.html` – Website frontend
- `.env.example` – Example environment configuration

## Future Enhancements

- Real-time location tracking for collection teams
- Automated NGO and donor matching
- Online donation impact reports
- Email or SMS notifications
- Dynamic dashboard statistics

## How to Run

1. Install Python and MySQL.
2. Create the database by executing `schema.sql` in MySQL.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database credentials and Flask secret key using environment variables.
5. Start the application:

   ```bash
   python app.py
   ```

6. Open the local address displayed in the terminal in your web browser.

## Efficiency and Benefits

EasyDonate makes donation collection more convenient and efficient by allowing donors to submit requests online and helping organize donation records in one place. It reduces manual paperwork, saves time, supports doorstep pickup coordination, and improves communication between donors, NGOs, and volunteer collection teams. This helps make the donation process more organized, accessible, and transparent.

## Project Goal

The goal of EasyDonate is to make donation collection more organized and convenient by connecting donors, NGOs, and volunteer collection teams through a single platform.

---


