from flask_restplus import Api
from flask import Blueprint

from .main.user.apis.user import api as user_ns
from .main.auth.apis.auth import api as auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='iCT Gamming Zone - API Specification',
          version='1.0',
          description='API specification using Swagger'
          )

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')