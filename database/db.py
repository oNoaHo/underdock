#from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# db = MongoEngine()
db = SQLAlchemy()


def initialize_db(app):
    db.init_app(app)
