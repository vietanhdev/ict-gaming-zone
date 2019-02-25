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

### NOTE FOR DEVELOPERS:

#### Create Multilang APIs using Flask-Babel:
- Please don't hardcode strings in this application.
- Use Flask-Babel to implement multilang APIs:
    + Import gettext, nggettext: `from flask_babel import gettext, ngettext`.
    + Use them in code: `gettext(u'User successfully created')`.
    + Use babel to update language files automatically: 
    ```Python
    pybabel extract -F babel.cfg -o messages.pot app
    pybabel update -i messages.pot -d app/main/translations
    ```
    + Edit language files in `app/main/translations/**/*.po` using text editors or POEdit tool: https://poedit.net/
    + Compile language file:
    ```Python
    pybabel compile -d  app/main/translations
    ```
- To specify language for API, set `Accept-Language` header of request to the language of response. Currently we support `en` (default) and `vi`.
    

### References
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563
