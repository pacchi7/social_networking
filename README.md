# Social Networking API

This project is a social networking application built using Django and Django REST Framework (DRF). The API provides functionalities such as user authentication, friend requests management, accept the request, reject the request and user search.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Prerequisites](#Prerequisites)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)

## Features

- **JWT Authentication**: Secure user authentication using JSON Web Tokens.
- **User Search**: Search users by email or name with pagination.
- **Friend Requests**: Send, accept, reject, and list friend requests.
- **User Management**: Manage user profiles and friendships.

## Installation

### Prerequisites

- Python 3.12.4
- Django 5.1
- Django REST Framework 3.15.2
- PostgreSQL 
   
   Note - before goint to setup please create database in postgresql and add credentials in .env file
### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/social-networking-api.git
   cd social-networking-api
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

### api-endpoints

    ### signup
        url: http://127.0.0.1:8000/users/signup/
        method: POST
        body: {
            "email":"test1@gmail.com",
            "name":"test1",
            "password":"test1"
            }
        response: {
            "id": 3,
            "name": "test1",
            "email": "test1@gmail.com",
            "message": "User created successfully!"
            }
    
    ### login
        url: http://127.0.0.1:8000/users/login/
        method: POST
        body: {
            "email": "test@gmail.com",
            "password":"test"
            }
        response: {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMzgwMTI2MSwiaWF0IjoxNzIzNzE0ODYxLCJqdGkiOiIzNGU1ZWQ5YjRlM2Y0YmRjOGFkNzMxZDViM2M3YmM5NyIsInVzZXJfaWQiOjJ9.QHCE2C62sKnJ2u88Izocb1GutXKUBFB8y2XuewH34Co",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNzE1MTYxLCJpYXQiOjE3MjM3MTQ4NjEsImp0aSI6ImZmOGNjNjc1YjA3ZDQ2ZWViMWU0MWEzNTYzZDk1Y2ZkIiwidXNlcl9pZCI6Mn0.EphRjvhICJdt89a9P-EX8PWkPewHSadSutBvjF6Z80w",
            "user": {
                "id": 2,
                "name": "test",
                "email": "test@gmail.com"
                }
            }
    
    ### user_search
        url: http://localhost:8000/users/search/?q=test1@gmail.com
        method: POST
        Query Parameters: {
            key: q,
            value: test1@gmail.com
            }
        response: [
                {
                    "id": 3,
                    "first_name": "test1",
                    "last_name": "",
                    "email": "test1@gmail.com"
                }
            ]
    
    ### send_friend_request
        url: http://127.0.0.1:8000/users/send_friend_request/
        method: POST
        body: {
            "to_user_id":2
            }
        response: {
            "message": "Friend request sent"
        }
    Note - to_user_id means id of user which will be available in user table after creating using 

    ### accept_friend_request
        url: http://127.0.0.1:8000/users/accept_friend_request/
        method: POST
        body: {
            "request_id":1
            }
        response: {
            "message": "Friend request accepted"
            }
    Note - the request_id means freand request table id that you will find in the list_pending_requests for example as per this file its "4"
    
    ### list_pending_requests
        url: http://127.0.0.1:8000/users/list_pending_requests/
        method: GET
        response: [
            {
                "id": 4,
                "from_user": {
                "id": 1,
                "username": "prashant@gmail.com",
                "email": "prashant@gmail.com"
                }
            }
        ]
    
    ### reject_friend_request
        url: http://127.0.0.1:8000/users/reject_friend_request/
        method: POST
        body: {
            "request_id":4
            }
        response: {
            "message": "Friend request rejected"
            }
    Note - the request_id means freand request table id that you will find in the list_pending_requests for example as per this file its "4"

    ### list_friends
        url: http://127.0.0.1:8000/users/list_friends/
        method: GET
        response: [
            {
                "id": 1,
                "first_name": "Prashant",
                "last_name": "",
                "email": "prashant@gmail.com"
            }
        ]
    