# KanMind Backend 

A RESTful backend service for the task management application KanMind.


## Django Project

The project is called 'backend_kanmind', but project files are stored in the 'core' folder. Please refer to 'core/settings.py' for further details.


## Django Apps

Apps include: 

+ auth_app - this is for signup and login logic that don't require a token or authenticated user.
+ kanban_app - this is for the data models of Boards, Tasks und Comments and the logic for creating, updating, viewing and deleting data with different permissions. Can only be accessed by authenticated users.


## Installation

On macOS and Linux:
```sh
$ python -m pip install backend_kanmind
```

On Windows:
```sh
PS> python -m pip install backend_kanmind
```

## Execution / Usage
To run backend_kanmind, fire up a terminal window and run the following command:
```sh
$ backend_kanmind
```

Here are a few examples of using the backend_kanmind library in your code:

```python
from backend_kanmind.models import Board
...
```

## Technologies

backend_kanmind uses the following technologies and tools: 

![Python](	https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)  | ![Django]([https://img.shields.io/pypi/frameworkversions/django/5.2.4](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)) | ![DjangoREST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) | ![SQLite]([https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white))


## Database

The SQLite3 database used sits in the Django project root folder (alongside this README file). It is not included within the Git repo, so must instead be requested from the system admin. 


## Settings

There is 1 settings related file:

+ `settings.py` (for general project settings, regardless of environment and containing publicly accessible information)


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

  
