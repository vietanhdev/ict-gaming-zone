import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_babel import Babel, refresh; refresh()
from flask import g, request
from app import blueprint
from app.main import create_app, db

app = create_app(os.getenv('ICT_GAMING_ZONE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

babel = Babel(app)
@babel.localeselector
def get_locale():
    refresh()
    translations = [str(translation) for translation in babel.list_translations()]
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