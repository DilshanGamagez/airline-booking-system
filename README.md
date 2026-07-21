# Airline Booking System

A secure flight booking web application built with Flask, demonstrating core web security practices including authentication, password hashing, and protected routes.

## Features
- User signup and login with hashed passwords (Werkzeug + Flask-Login)
- Browse available flights
- Book flights (only accessible to logged-in users)
- View personal booking history
- Session-based authentication with protected routes

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite with Flask-SQLAlchemy (ORM)
- **Auth:** Flask-Login, Werkzeug password hashing
- **Frontend:** HTML, Jinja2 templating

## Security Practices Implemented
- Passwords are never stored in plain text — hashed using Werkzeug's `generate_password_hash`
- Booking routes are protected with `@login_required`, preventing unauthorized access
- Session management handled securely via Flask-Login

## Project Status
In development — currently a local Flask app. Planned next steps:
- Containerize with Docker
- Deploy to AWS using Terraform
- Add AWS security layer: IAM least-privilege roles, Secrets Manager, WAF, GuardDuty, CloudTrail
- Set up CI/CD pipeline with GitHub Actions

## Running Locally
```bash
git clone https://github.com/DilshanGamagez/airline-booking-system.git
cd airline-booking-system
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy flask-login werkzeug
python3 app.py
```
Then visit `http://localhost:5000`

## Author
Dilshan Gamage — BSc (Hons) Computer Networks student, building toward cloud/Security roles.