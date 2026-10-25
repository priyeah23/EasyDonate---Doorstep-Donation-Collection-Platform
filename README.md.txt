# EasyDonate — Flask + MySQL

A donation-management web app using the existing EasyDonate frontend with a Python Flask backend and MySQL database.

## Implemented in this version
- Responsive HTML/CSS/JavaScript frontend
- Flask routes and JSON API
- User registration and login using Werkzeug password hashing
- Donation requests saved to MySQL
- Contact messages saved to MySQL
- Session-based login and per-user donation listing API (`GET /api/donations`)
- Donation receipt ID returned from the database

## Requirements
- Python 3.10+
- MySQL Server
- A web browser

## Setup

1. Create and activate a virtual environment:

   **Windows**
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bat
   pip install -r requirements.txt
   ```

3. In MySQL Workbench or the MySQL command line, run the contents of `schema.sql`.

4. Set database environment variables. For example, in Windows Command Prompt:

   ```bat
   set DB_HOST=localhost
   set DB_PORT=3306
   set DB_USER=root
   set DB_PASSWORD=YOUR_MYSQL_PASSWORD
   set DB_NAME=easydonate_db
   set FLASK_SECRET_KEY=replace-with-a-long-random-secret
   ```

   Replace `YOUR_MYSQL_PASSWORD` with your own MySQL password. Do not upload real credentials to GitHub.

5. Start the app:

   ```bat
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## API endpoints
- `GET /api/health` — checks MySQL connectivity
- `POST /api/register` — creates an account
- `POST /api/login` — verifies credentials
- `POST /api/logout` — clears the login session
- `POST /api/donations` — validates and stores a donation
- `GET /api/donations` — lists donations for the signed-in user
- `POST /api/messages` — stores a contact message

## Important notes
- The donation form can save a donation even if the donor has not logged in; such records have no linked user account. Registration/login is available from the top navigation.
- The page contains demo/sample dashboard counts, campaign progress, NGO need levels and volunteer assignment text. These are illustrative UI content and are not dynamically fetched from MySQL in this starter version.
- Donation status is initially saved as `Submitted`; live GPS tracking, automatic NGO matching, pickup-team assignment and status updates are not implemented.
- This is a local development starter. Before public deployment, configure a strong secret key, production server, CSRF protections, rate limiting, HTTPS, and privacy/security review.
