#### PROJECT REPOSITORY FOR ICT GAMMING ZONE


### Installing neccessary packages

~~~
pip install -r requirements.txt
~~~

### Initialize database

~~~
python manage.py db upgrade
~~~


### Run the application

~~~
python manage.py run
~~~


### Using Postman ####

    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

### References
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563
