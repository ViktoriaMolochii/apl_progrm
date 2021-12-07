from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from marshmallow import Schema, fields
from flask_bcrypt import check_password_hash
import utils
from constants import *
from models import *
import jwt
import bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:vika29@localhost:3306/inetshop'

    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)
    ma = Marshmallow(app)
    class UserSchema(Schema):
        class Meta:
            model = User
            fields = ('Id', 'userName', 'firstName', 'lastName', 'email', 'login', 'password', 'phone', 'userStatus')

    class CustomSchema(Schema):
        class Meta:
            model = Custom
            fields = ('id', 'shipDate', 'statusCustomid', 'userid', 'productionid')
    class ProductionSchema(Schema):
        class Meta:
            model = Production
            fields = ('id', 'name', 'number')


    @app.route(BASE_PATH+ "/hello-world-6")
    def hello_world():
        return "<p>Hello World 6</p>"

#USER

    @app.route(BASE_PATH + USER_PATH + '/<int:Id>', methods=['GET'])
    @jwt_required()
    def get_user_by_id(Id):
        current_login = get_jwt_identity()

        session = Session()
        try:
            user = session.query(User).filter_by(Id=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        #false-user
        #true-admin
        user2 = session.query(User).filter_by(login=current_login).one()
        if current_login == user.login or user2.userStatus == True:
            return jsonify(UserSchema().dump(user)), 200

        return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + USER_PATH, methods=['GET'])
    @jwt_required()
    def get_all_users():
        current_login = get_jwt_identity()
        session = Session()
        try:
            users = session.query(User).all()
        except:
            users = []

        users_obj = UserSchema(many=True)
        user2 = session.query(User).filter_by(login=current_login).one()
        if user2.userStatus == True:
            return jsonify(users_obj.dump(users)), 200

        return jsonify('Access is denied'), 403

    @app.route(BASE_PATH + USER_PATH, methods=['POST'])
    def create_user():
        session = Session()
        try:
            user_info = UserSchema().load(request.json)
            try:
                if session.query(User).filter_by(Id=user_info.get('Id')).one():
                    return jsonify(USER_ALREADY_EXISTS), 409
            except:
                pass
            passUser = user_info.get('password')
            hashed_password = bcrypt.hashpw((bytes(passUser, 'utf-8')), bcrypt.gensalt())
            user_info['password'] = hashed_password

            user = User(**user_info)
            session.add(user)
            session.commit()
            return jsonify(USER_CREATED), 201
        except:
            return jsonify(SOMETHING_WENT_WRONG), 400

    @app.route(BASE_PATH + USER_PATH + '/login', methods=['POST'])
    def login():
        # creates dictionary of form data
        auth = request.form

        if not auth or not auth.get('login') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )
        session = Session()
        try:
            user = session.query(User).filter_by(login=auth.get('login')).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )
        if check_password_hash(user.password, auth.get('password')):
            access_token = create_access_token(identity=user.login)
            return access_token

        # returns 403 if password is wrong
        return make_response(
            'Wrong password',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )

    @app.route(BASE_PATH + USER_PATH + '/<int:Id>', methods=['PUT'])
    @jwt_required()
    def update_user(Id):
        current_login = get_jwt_identity()
        session = Session()
        try:
            user = session.query(User).filter_by(Id=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        if current_login == user.login:
            try:
                user_info = UserSchema().load(request.json, partial=True)
                if user_info.get('Id'):
                    return jsonify(CANT_CHANGE_ID), 400
            except:
                pass
            try:
                try:
                    user = session.query(User).filter_by(Id=Id).one()
                except:
                    return jsonify(USER_NOT_FOUND), 404
                if user_info.get('password'):
                    passwd = user_info.get('password')
                    hashed_password = bcrypt.hashpw(bytes(passwd, 'utf-8'), bcrypt.gensalt())
                    user_info['password'] = hashed_password

                updated_user = utils.update(user, **user_info)
                if updated_user == None:
                    return jsonify(SOMETHING_WENT_WRONG), 400

                return jsonify(USER_UPDATED), 200
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400

        return jsonify('Access is denied'), 403


    @app.route(BASE_PATH + USER_PATH + '/<Id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(Id):
        current_login = get_jwt_identity()
        session = Session()
        try:
            user = session.query(User).filter_by(Id=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        user2 = session.query(User).filter_by(login=current_login).one()
        if current_login == user.login or user2.userStatus == True:
            numberOfUserUsage = session.query(Custom).filter_by(userid=Id).count()

            try:
                if numberOfUserUsage > 0:
                    return jsonify('Sorry, firstly delete all user`s customs'), 400
            except:pass

            session.query(User).filter_by(Id=Id).delete()
            session.commit()

            return jsonify(USER_DELETED), 200
        else:
            return jsonify('Access is denied'), 403

#PRODUCTION

    @app.route(BASE_PATH + PRODUCTION_PATH + '/' + '<int:id>', methods=['GET'])
    def get_product_by_id(id):
        session = Session()
        try:
            products = session.query(Production).filter_by(id=id).one()
        except:
            return jsonify(PRODUCTION_NOT_FOUND), 404

        return jsonify(ProductionSchema().dump(products)), 200

    @app.route(BASE_PATH + PRODUCTION_PATH, methods=['GET'])
    def get_all_production():
        session = Session()
        try:
            products = session.query(Production).all()
        except:
            products = []

        products_obj = ProductionSchema(many=True)

        return jsonify(products_obj.dump(products)), 200

    # only admin
    @app.route(BASE_PATH + PRODUCTION_PATH, methods=['POST'])
    @jwt_required()
    def create_production():
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        if user.userStatus == True:
            try:
                product_info = ProductionSchema().load(request.json)
                try:
                    if session.query(Production).filter_by(id=product_info.get('id')).one():
                        return jsonify(PRODUCTION_ALREADY_EXISTS), 409
                except:
                    pass

                product = Production(**product_info)
                session.add(product)
                session.commit()
                return jsonify(PRODUCTION_CREATED), 200
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403

    # only admin
    @app.route(BASE_PATH + PRODUCTION_PATH + '/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_product(id):
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        if user.userStatus == True:
            try:
                product_info = ProductionSchema().load(request.json, partial=True)

                if not product_info:
                    return jsonify(EMPTY_DATA), 400

                if product_info.get('id'):
                    return jsonify(CANT_CHANGE_ID), 400
            except:
                pass
            try:
                if product_info.get('number'):
                    try:
                        numOfProductsBought = session.query(Custom).filter_by(productionid=id).count()
                        try:
                            if numOfProductsBought > product_info.get('number'):
                                return jsonify('You can`t now change number to lower value'), 400
                        except:
                            pass
                    except:
                        pass
                try:
                    products = session.query(Production).filter_by(id=id).one()
                except:
                    return jsonify(PRODUCTION_NOT_FOUND), 404

                utils.update(products, **product_info)

                return jsonify(PRODUCTION_UPDATED), 200
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403

    # only admin
    @app.route(BASE_PATH + PRODUCTION_PATH + '/<id>', methods=['DELETE'])
    @jwt_required()
    def delete_product(id):
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        if user.userStatus == True:
            try:
                session.query(Production).filter_by(id=id).one()
            except:
                return jsonify(PRODUCTION_NOT_FOUND), 404

            numberOfProdUsage = session.query(Custom).filter_by(productionid=id).count()

            try:
                if numberOfProdUsage > 0:
                    return jsonify('Sorry,you must delete custom with this product'), 400
            except:
                pass

            session.query(Production).filter_by(id=id).delete()
            session.commit()

            return jsonify(PRODUCTION_DELETED), 200
        else:
            return jsonify('Access is denied'), 403


#CUSTOM

    # only admin and user
    @app.route(BASE_PATH + CUSTOM_PATH + '/' + '<int:id>', methods=['GET'])
    @jwt_required()
    def get_custom_by_id(id):
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        try:
            customs = session.query(Custom).filter_by(id=id).one()
        except:
            return jsonify(CUSTOM_NOT_FOUND), 404
        if (user.userStatus == False and customs.userid == user.Id) or user.userStatus == True:
            return jsonify(CustomSchema().dump(customs)), 200
        else:
            return jsonify('Access is denied'), 403

    # only admin
    @app.route(BASE_PATH + CUSTOM_PATH, methods=['GET'])
    @jwt_required()
    def get_all_customs():
        current_login = get_jwt_identity()
        session = Session()
        try:
            customs = session.query(Custom).all()
        except:
            customs = []

        customs_obj = CustomSchema(many=True)
        user = session.query(User).filter_by(login=current_login).one()
        if user.userStatus == True:
            return jsonify(customs_obj.dump(customs)), 200
        else:
            return jsonify('Access is denied'), 403



    # only user
    @app.route(BASE_PATH + CUSTOM_PATH, methods=['POST'])
    @jwt_required()
    def create_custom():
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        custom_request = request.get_json()
        if user.userStatus == False and custom_request["userid"] == user.Id:
            try:
                custom_request = request.get_json()
                try:
                    if session.query(Custom).filter_by(id=custom_request['id']).one():
                        return jsonify(CUSTOM_ALREADY_EXISTS), 409
                except:
                    pass

                try:
                    session.query(User).filter_by(Id=custom_request['userid']).one()
                except:
                    return jsonify(USER_NOT_FOUND), 404
                try:
                    session.query(Production).filter_by(id=custom_request['productionid']).one()
                except:
                    return jsonify(PRODUCTION_NOT_FOUND), 404

                numOfProductsBought = session.query(Custom).filter_by(productionid=custom_request['productionid']).count()
                numOfProductsDefault = session.query(Production).filter_by(id=custom_request['productionid']).one().number
                if (numOfProductsBought < numOfProductsDefault):

                    custom_info = Custom(**custom_request)

                    session.add(custom_info)
                    session.commit()

                    return jsonify(CUSTOM_CREATED), 201
                else:
                    return jsonify('Product is totally sold!')

            except:
                return jsonify(SOMETHING_WENT_WRONG), 400
        else:
            return jsonify('Access is denied'), 403

    # only user and admin
    @app.route(BASE_PATH + CUSTOM_PATH + '/' + '<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_custom(id):
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        try:
            custom= session.query(Custom).filter_by(id=id).one()
        except:
            return jsonify(CUSTOM_NOT_FOUND), 404
        if (user.userStatus == False and custom.userid == user.Id) or user.userStatus == True:
            custom_delete = session.query(Custom).filter_by(id=id).one()

            session.delete(custom_delete)
            session.commit()

            return jsonify(CUSTOM_DELETED), 201
        else:
            return jsonify('Access is denied'), 403

    # only user
    @app.route(BASE_PATH + CUSTOM_PATH + '/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_custom(id):
        current_login = get_jwt_identity()
        session = Session()
        user = session.query(User).filter_by(login=current_login).one()
        if user.userStatus == False:
            try:
                custom_info = CustomSchema().load(request.json, partial=True)

                if not custom_info:
                    return jsonify(EMPTY_DATA), 400

                if custom_info.get('id'):
                    return jsonify(CANT_CHANGE_ID), 400

                if custom_info.get('userid'):
                    return jsonify(CANT_CHANGE_ID), 400

                if custom_info.get('productionid'):
                    return jsonify(CANT_CHANGE_ID), 400

                if custom_info.get('statusCustomid') > 2 or custom_info.get('statusCustomid') <= 0:
                    return jsonify('Such status not found!'), 404

            except:
                pass
            try:
                try:
                    custom = session.query(Custom).filter_by(id=id).one()
                except:
                    return jsonify(CUSTOM_NOT_FOUND), 404

                utils.update(custom, **custom_info)

                return jsonify(CUSTOM_UPDATED), 200
            except:
                return jsonify(SOMETHING_WENT_WRONG), 400

        else:
            return jsonify('Access is denied'), 403

    return app



# .venv\Scripts\activate
# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# /api/v1/hello-world-6
# /api/v1/hello-world

# curl -v -XGET http://localhost:5000/api/v1/hello-world-6

