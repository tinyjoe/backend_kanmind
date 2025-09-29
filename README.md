# KanMind Backend 

A RESTful backend service for the task management application KanMind.


## Django Project

The project is called 'backend_kanmind', but project files are stored in the 'core' folder. Please refer to 'core/settings.py' for further details.


## Requirements

+ Python 3.13
+ Django 5.2.4
+ SQLite 3


## Technologies

backend_kanmind uses the following technologies and tools: 

![Python](	https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)     ![Django](https://img.shields.io/badge/Django-5.2.4-green?style=for-the-badge&logo=django&logoColor=white)     ![DjangoREST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)     ![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite&logoColor=white)


## Django Apps

Apps include: 

+ auth_app - this is for signup and login logic that don't require a token or authenticated user.
+ kanban_app - this is for the data models of Boards, Tasks und Comments and the logic for creating, updating, viewing and deleting data with different permissions. Can only be accessed by authenticated users.


## Database

The SQLite3 database used sits in the Django project root folder. It is not included within the Git repo, so must instead be requested from the system admin. 


## Settings

There is 1 settings related file:

+ `settings.py` (for general project settings, regardless of environment and containing publicly accessible information)


## Installation

Clone the repostiory:
```sh
git clone https://github.com/tinyjoe/backend_kanmind.git
cd backend_kanmind
```

Create a virtual environment
```sh
python -m venv env
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install dependencies
```sh
pip install -r requirements.txt
```

## Database Migrations

Run the initial migrations
```sh
python manage.py migrate
```

When you make changes to models
```sh
python manage.py makemigrations
python manage.py migrate
```

## Start Development Server
```sh
python manage.py runserver
```





## API-Documentation
- [POST] - User Registration - Signup a new user
  ```
  /api/registration/
  ```

- [POST] - User Login - Login a registrated user
  ```
  /api/login/
  ```

- [GET] - Boards - Get an overview of the boards where the user is owner or member
  ```
  /api/boards/
  ```

- [POST] - Boards - Create a new board
  ```
  /api/boards/
  ```

- [GET] - Board Details - Get the details of a specific board where the user is owner or member
  ```
  /api/boards/{board_id}/
  ```

- [PATCH] - Board Details - Update the details of a specific board where the user is owner or member
  ```
  /api/boards/{board_id}/
  ```

- [DELETE] - Board Details - Delete a specific board where the user is owner
  ```
  /api/boards/{board_id}/
  ```

- [GET] - Email-Check - Checks if a user with the given email address exists
  ```
  /api/email-check/
  ```

- [GET] - Assigned Tasks - Get a list of tasks where the user is the assignee
  ```
  /api/tasks/assigned-to-me/
  ```

- [GET] - Reviewing Tasks - Get a list of tasks where the user is the reviewer
  ```
  /api/tasks/reviewing/
  ```

- [POST] - Task - Create a new tasks for a board where the user is a member
  ```
  /api/tasks/
  ```

- [PATCH] - Task - Update an existing task where the user is the creator or member of the board
  ```
  /api/tasks/{task_id}/
  ```

- [DELETE] - Task - Delete an existing task where the user is the creator
  ```
  /api/tasks/{task_id}/
  ```

- [GET] - Comments - Get a list of the comments of a task
  ```
  /api/tasks/{task_id}/comments/
  ```

- [POST] - Comment - Create a comment for a task where the user is member of the board
  ```
  /api/tasks/{task_id}/comments/
  ```

- [DELETE] - Comment - Delete a specific comment of a task where the user is the author or member of the board
  ```
  /api/tasks/{task_id}/comments/{comment_id}/
  ```

  
