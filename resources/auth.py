from flask import Response, request, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, jwt_refresh_token_required
from database.models import ApiUser, UserSchema
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
import pprint


class SignupApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            product_schema = UserSchema()
            if data.get('userid'):
                get_product = ApiUser.query.get(data['userid'])
                products = product_schema.dump(get_product)
                if products:
                    return make_response(jsonify({"status": "error", "message": "User already exists"}), 200)
            product = product_schema.load(data)
            product.hash_password()
            result = product_schema.dump(product.create())
            return make_response(jsonify({"product": result}), 200)
            # body = request.get_json()
            # apiusers = apiuser(**body)
            # apiusers.hash_password()
            # apiusers.save()
            # id = apiusers.id
            # return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            product_schema = UserSchema()
            if data.get('userid'):
                if data.get('password'):
                    get_product = ApiUser.query.get(data['userid'])
                    products = product_schema.dump(get_product)
                    product = product_schema.load(products)
                    pprint.pprint(product.password)
                    pprint.pprint(data['password'])
                    authorized = product.check_password(
                        data['password'])
                    if not authorized:
                        raise UnauthorizedError
                    expires = datetime.timedelta(minutes=5)
                    refreshexpires = datetime.timedelta(minutes=10)
                    access_token = create_access_token(
                        identity=str(product.userid), expires_delta=expires, fresh=True)
                    refresh_token = create_refresh_token(
                        identity=str(product.userid), expires_delta=refreshexpires)
                    return {'access_token': access_token, 'refresh_token': refresh_token}, 200
                else:
                    return make_response(jsonify({"status": "error", "message": "no password specified"}), 200)
            else:
                return make_response(jsonify({"status": "error", "message": "no userid specified"}), 200)
            # body = request.get_json()
            # apiusers = apiuser.objects.get(name=body.get('name'))
            # authorized = apiusers.check_password(body.get('password'))
            # if not authorized:
            #     raise UnauthorizedError

            # expires = datetime.timedelta(minutes=5)
            # refreshexpires = datetime.timedelta(minutes=10)
            # access_token = create_access_token(
            #     identity=str(apiusers.id), expires_delta=expires, fresh=True)
            # refresh_token = create_refresh_token(
            #     identity=str(apiusers.id), expires_delta=refreshexpires)
            # return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        expires = datetime.timedelta(minutes=5)
        refreshexpires = datetime.timedelta(minutes=10)
        new_token = create_access_token(
            identity=current_user, expires_delta=expires, fresh=False)
        refresh_token = create_refresh_token(
            identity=current_user, expires_delta=refreshexpires)
        return {'access_token': new_token, 'refresh_token': refresh_token}, 200
