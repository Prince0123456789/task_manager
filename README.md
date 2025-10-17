# Task Manager API (Django + DRF)

## Features
- CRUD for tasks: `GET /api/tasks/`, `GET /api/tasks/{id}/`, `POST /api/tasks/`, `PUT /api/tasks/{id}/`, `DELETE /api/tasks/{id}/`
- JWT authentication (login/register)
- Swagger and ReDoc documentation
- Pagination and filtering (`?page=`, `?completed=true|false`, `?search=...`)
- Unit tests

## Quick start (local)

1. Create a virtualenv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate         

2.  pip install -r requirements.txt
3.  python manage.py migrate
4.  python manage.py createsuperuser
5.  python manage.py runserver

## For admin panel
http://localhost:8000/admin
## For Swagger View
http://localhost:8000/swagger

## Example requests
- Create a task (authenticated)
POST /api/tasks/
    Authorization: Bearer <access_token>
    Content-Type: application/json

    {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
    }
