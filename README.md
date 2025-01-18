# Djosify API

Djosify is a user authentication and management system based on JWT (JSON Web Tokens) using Django and Django REST Framework. This API allows user creation, login, logout, and the management of access and refresh tokens.

This project is intended for the **Python Developer Internship** at **JL.ForEachPartners**.

## Description

Djosify provides an authentication solution for Django applications with capabilities to manage user register, login, and token refresh. It also offers profile management and a secure authentication flow with access and refresh tokens.

## Features

- 🔑 **JWT Authentication**: Obtain access and refresh tokens, with the ability to refresh them. The refresh token is stored server-side to manage session state.
- 👤 **User Management**: Registration, login, profile update, and logout functionality.
- 📄 **API Documentation**: Interactive API documentation available via Swagger and ReDoc.

## Requirements

- 🐍 Python 3.10.12
- 🖥️ Django 5.1.5
- 🔗 Django REST Framework
- 🔑 Djoser for user authentication 
- 🔄 djangorestframework-simplejwt for JWT token management
- 📑 drf-yasg for dynamic API documentation

## Installation

1. Clone this repository:

```bash
    git clone git@github.com:VladimirAzanza/djosify.git
```

2. Install the dependencies:

```bash
    cd djosify
    pip install -r requirements.txt
```

3. Configure the .env file with the necessary environment variables (SECRET_KEY, database, JWT, etc.).

4. Run the migrations:
```bash
    python manage.py migrate
```
5. Start the development server:
```bash
    python manage.py runserver
```

## Endpoints

The API is available at http://localhost:8000/api/. For interactive documentation, you can access the following links:

    📜 Swagger UI: http://localhost:8000/swagger/
    📚 ReDoc UI: http://localhost:8000/redoc/

## API Usage
User Registration

    POST /api/register/
    Register a new user by providing email and password.

Authentication

    POST /api/login/
    Obtain an access_token and refresh_token using the email and password.

    POST /api/refresh/
    Refresh the access token using the refresh_token.

Profile Management

    GET/PUT /api/me/
    Retrieve or update the profile of the logged-in user.

Logout

    POST /api/logout/
    Log out the user by deleting their refresh token.
