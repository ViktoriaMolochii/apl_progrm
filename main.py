from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import utils
from constants import *
from models import *
import bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:vika29@localhost:3306/inetshop'

    ma = Marshmallow(app)
    class UserSchema(Schema):
        class Meta:
            model = User
            fields = ('Id', 'userName', 'firstName', 'lastName', 'email', 'password', 'phone', 'userStatus')

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
    def get_user_by_id(Id):
        session = Session()
        try:
            user = session.query(User).filter_by(Id=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        return jsonify(UserSchema().dump(user)), 200

    @app.route(BASE_PATH + USER_PATH, methods=['GET'])
    def get_all_users():
        session = Session()
        try:
            users = session.query(User).all()
        except:
            users = []

        users_obj = UserSchema(many=True)

        return jsonify(users_obj.dump(users)), 200

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

    @app.route(BASE_PATH + USER_PATH + '/<int:Id>', methods=['PUT'])
    def update_user(Id):
        session = Session()
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

    @app.route(BASE_PATH + USER_PATH + '/<Id>', methods=['DELETE'])
    def delete_user(Id):
        session = Session()
        try:
             session.query(User).filter_by(Id=Id).one()
        except:
            return jsonify(USER_NOT_FOUND), 404

        numberOfUserUsage = session.query(Custom).filter_by(userid=Id).count()

        try:
            if numberOfUserUsage > 0:
                return jsonify('Sorry, firstly delete all user`s customs'), 400
        except:pass

        session.query(User).filter_by(Id=Id).delete()
        session.commit()

        return jsonify(USER_DELETED), 200

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

    @app.route(BASE_PATH + PRODUCTION_PATH, methods=['POST'])
    def create_production():
        session = Session()
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

    @app.route(BASE_PATH + PRODUCTION_PATH + '/<int:id>', methods=['PUT'])
    def update_product(id):
        session = Session()
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

    @app.route(BASE_PATH + PRODUCTION_PATH + '/<id>', methods=['DELETE'])
    def delete_product(id):
        session = Session()
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


#CUSTOM

    @app.route(BASE_PATH + CUSTOM_PATH + '/' + '<int:id>', methods=['GET'])
    def get_custom_by_id(id):
        session = Session()
        try:
            customs = session.query(Custom).filter_by(id=id).one()
        except:
            return jsonify(CUSTOM_NOT_FOUND), 404

        return jsonify(CustomSchema().dump(customs)), 200

    @app.route(BASE_PATH + CUSTOM_PATH, methods=['GET'])
    def get_all_customs():
        session = Session()
        try:
            customs = session.query(Custom).all()
        except:
            customs = []

        customs_obj = CustomSchema(many=True)

        return jsonify(customs_obj.dump(customs)), 200


    @app.route(BASE_PATH + CUSTOM_PATH, methods=['POST'])
    def create_custom():
        session = Session()
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


    @app.route(BASE_PATH + CUSTOM_PATH + '/' + '<int:id>', methods=['DELETE'])
    def delete_custom(id):
        session = Session()
        try:
            session.query(Custom).filter_by(id=id).one()
        except:
            return jsonify(CUSTOM_NOT_FOUND), 404

        custom_delete = session.query(Custom).filter_by(id=id).one()

        session.delete(custom_delete)
        session.commit()

        return jsonify(CUSTOM_DELETED), 201

    @app.route(BASE_PATH + CUSTOM_PATH + '/<int:id>', methods=['PUT'])
    def update_custom(id):
        session = Session()
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




    return app




# .venv\Scripts\activate
# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# /api/v1/hello-world-6
# /api/v1/hello-world

# curl -v -XGET http://localhost:5000/api/v1/hello-world-6


# http://127.0.0.1:5000/api/v1/user/shcherbii_ostap
