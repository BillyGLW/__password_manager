# heroku: 
https://password-manager-django.herokuapp.com/web_manager
# description: 
password manager that gives user an "bucket" for his passwords stored in secure way (django crypto), by using get request it is possible to share selected by user password as in temporary link, so that the others can see it and edit.

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`users` | GET | READ | Get all passwords
`user/:id` | GET | READ | Get a single password
`user`| POST | CREATE | Create a new password
`user/:id` | PUT | UPDATE | Update a password
`user/:id` | DELETE | DELETE | Delete a password

# set-up: 
Install Dependencies

pip install -r requirements.txt

Set Database (Make Sure you are in directory same as manage.py)

python manage.py makemigrations python manage.py migrate

Create SuperUser

python manage.py createsuperuser

After all these steps , you can start testing and developing this project. That's it! Happy Coding!

# Docker
- docker-compose:
 --building a new container with simultaneously running
### docker-compose down && docker-compose up
 - migrations, by executing "makemigrations" inside docker container
### docker-compose exec web python manage.py makemigrations --noinput
