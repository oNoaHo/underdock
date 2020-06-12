from .db import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_bcrypt import generate_password_hash, check_password_hash


class ApiUser(db.Model):
    __tablename__ = "apiuser"
    #id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), unique=True, primary_key=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, userid, password, email):
        self.userid = userid
        self.password = password
        self.email = email

    def __repr__(self):
        return '' % self.userid

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ApiUser
        sqla_session = db.session
    #id = fields.Number(dump_only=True)
    userid = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String()

# class users(db.Document):
#     userid = db.StringField(required=True, unique=True)
#     email = db.StringField()
#     department = db.StringField()
#     firstname = db.StringField()
#     lastname = db.StringField()
#     networks = db.ListField()
#     zones = db.ListField()
#     records = db.ListField()
#     groups = db.ListField()


# class groups(db.Document):
#     name = db.StringField(required=True, unique=True)
#     email = db.StringField()
#     comment = db.StringField()
#     networks = db.ListField()
#     zones = db.ListField()
#     records = db.ListField()


# class apiuser(db.Document):
#     # email = db.EmailField(required=True, unique=True)
#     name = db.StringField(required=True, unique=True)
#     password = db.StringField(required=True, min_length=6)

#     def hash_password(self):
#         self.password = generate_password_hash(self.password).decode('utf8')

#     def check_password(self, password):
#         return check_password_hash(self.password, password)
