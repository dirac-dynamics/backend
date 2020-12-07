# Backend

For prototyping, please refer to the [Jupyter folder](https://github.com/Dirac-Dynamics/backend/tree/main/jupyter).


## Flush and Migrate the DB

These commands are in the original `Dockerfile` in `/app` (commented out there).

```
$ docker-compose exec web python manage.py flush --no-input
$ docker-compose exec web python manage.py migrate
```

[Helpful link](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)


To be continued...