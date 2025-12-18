# Library Management – Backend API

A Django REST Framework–based backend application for managing books and borrowing operations.

---

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT (Authentication)

---

## Features

- Book listing with search
- User registration
- Borrow and return books
- JWT-based authentication
- Unit and integration tests

---

## Setup Instructions

### Clone the repository
```bash
git clone <repository-url>
cd library_project


### 1 Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


### 2 Install dependencies
```bash
pip install -r requirements.txt

### 3 Apply Migration
```bash
python manage.py migrate

### 4 Creating a superser(admin)
```bash
python manage.py createsuperuser

### 5 Run development server
```bash
python manage.py runserver

### 6 Running Tests
```bash
python manage.py test

*** Run with Docker ***

(you can run those commands from project directory )
```bash
docker-compose up --build

### Apply database migrations with docker
docker-compose exec web python manage.py migrate

### creating superuser
docker-compose exec web python manage.py createsuperuser

### Run the tests from the Docker
```bash
docker-compose exec web python manage.py test


### Authentication

This project uses JWT authentication include the token in request headers

Example: Authorization: Bearer <access_token>


API Endpoints:
Register User
http://127.0.0.1:8000/api/auth/register

Login User
http://127.0.0.1:8000/api/auth/login

Browse Books (search optional)
http://127.0.0.1:8000/api/books/?search=robert

Borrow Book (Authenticated)
http://127.0.0.1:8000/api/loans/borrow 

Return Book (Authenticated) 
http://127.0.0.1:8000/api/loans/return

Swagger API Docs
http://127.0.0.1:8000/swagger

Admin Panel 
http://127.0.0.1:8000/admin

