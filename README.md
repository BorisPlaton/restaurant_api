# Check generation API

My solution of [test task](https://github.com/smenateam/assignments/blob/master/backend/README.md) of creating an API service for generating checks.

## Configuration
## .env 
You have to create a `.env` file at the root of the project. You already have a `env.dist` file which has example values. You can use them in the `.env` file or create new ones.

## Project setup
Create a virtual environment and install all dependencies:
```
$ virtualenv venv --python 3.10
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## Application launch
### Docker-compose
Run the following command to run all necessary services:
```
$ docker-compose up
```
### RQ
The project uses [`django_rq`](https://github.com/rq/django-rq) for background tasks, so write next command in order to set up workers:
```
$ cd restaurant_api/
$ python manage.py rqworker wkhtmltopdf
```
### Run server
Now you can start a server. Type the following command:
```
$ python manage.py runserver
```



