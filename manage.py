import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_babel import Babel, refresh; refresh()
from flask import g, request
from app import blueprint
from app.main import create_app, db
from app.main.user.models import user
from app.main.auth.models import blacklist


app = create_app(os.getenv('ICTGAMMINGZONE_ENV') or 'dev')

babel = Babel(app)

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@babel.localeselector
def get_locale():
    print(request.accept_languages)
    refresh()
    translations = [str(translation) for translation in babel.list_translations()]
    print(translations)
    return 'vi'
    return request.accept_languages.best_match(['en', 'vi'])

@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
