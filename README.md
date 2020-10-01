# Shoes shop

Shoes shop + REST API using Django +  Django REST.

## Setup

For python 3.6+

1. Install `pipenv`: `pip install pipenv`
1. Clone the repo, cd inside it and create and/or activate a venv: `pipenv shell`
1. Install dependencies: `pipenv install --dev`
1. Apply migrations: `python manage.py migrate`
1. Create admin user: `python manage.py createsuperuser`
1. Start the app: `python manage.py runserver 0.0.0.0:8080`


## Usage

1. Login in the admin site with your admin user credentials: `http://localhost:8080/admin`
1. Create a Token for Users you want to give access to the API
1. Check the API documentation here: `http://localhost:8080/swagger/`
1. Make API requests with the following header: `Authorization: Token {YOUR_USER_TOKEN}`


## Development

- Run the tests: `pytest .`
- Tests + coverage report: `pytest --cov=. --cov-report term:skip-covered --cov-report html`