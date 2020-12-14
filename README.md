<!-- @format -->

## Two ways to run this project:

- Without Docker
- With Docker

---

## With Docker (make sure docker and docker compose is installed:

### To start application:

`docker-compose up --build `

### To stop application:

`docker-compose down`

## Without Docker:

### Install Dependencies

`pip install -r requirements.txt`

### Set Database (Make Sure you are in directory same as manage.py)

```
python manage.py makemigrations
python manage.py migrate
```

After all these steps , you can start testing and developing this project.
That's it! Happy Coding!
