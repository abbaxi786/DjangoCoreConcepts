# Task Management System API


# Abstract

    In this project, I had used the django framework to make the company and project management system. I had used the default user of the django. The user creates the company and inherit the admin previlege, then add the projects and tasks in the project , then it also add the employees by adding email, name and password.
    The employees can't do the post, update and delete operation, that are in the domain of admin but can view projects and tasks.

# Markdown

- Python
- Django
- Django REST Framework
- SQLite
- JWT Authentication
- Threading (Email)

git clone <repository_url>

cd tasks

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

# Use the bearer token on every user on postman 