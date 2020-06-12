from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db, db
from flask_restful import Api
from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb://192.168.4.58/ddiadmin'
# }
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1qayxsw2@192.168.4.58:3306/test'

initialize_db(app)
initialize_routes(api)

with app.app_context():
    db.create_all()

app.run(port=3500, debug=True)
