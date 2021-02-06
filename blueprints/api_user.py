import time

from extensions import db
from flask_restful import Api, Resource, reqparse
from flask import jsonify, request
from . import api_bp
from models.user import User
from blueprints.api_auth import auth, generator_auth_token, verify_auth_token

api_user = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('token', type=str)


class UserApi(Resource):
    def post(self):
        print('UserAddApi.post.url = ' + str(request.url))
        # 如果传入进来的是json数据，那么需要转换成dict类型的数据
        # user_info = json.loads(request.get_json())
        user_info = parser.parse_args()
        print('user_info.type =', type(user_info))
        print('UserAddApi.post.user_info = ' + str(user_info))
        try:
            u = User(username=user_info.get('username'))
            u.password = user_info.get('password')
            db.session.add(u)
            db.session.commit()
        except:
            print("{} User add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            db.session.rollback()
            return False
        else:
            print("{} User add: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            return True
        finally:
            db.session.close()

    @auth.login_required
    def get(self):
        token = parser.parse_args().get('token')
        print(token)
        # 使用token换取用户信息
        # user_info = verify_auth_token(token)

        # return jsonify({'用户名': user_info.username})
        return jsonify({'用户名': ".", 'token':token})

class UserVerifyApi(Resource):

    def post(self):
        print('UserVerifyApi.post.url = ' + str(request.url))
        # user_info = json.loads(request.get_json())
        user_info = parser.parse_args()
        try:
            u = User.query.filter_by(username=user_info.get('username')).first()
            if u is None or u.verify_password(user_info.get('password')) is False:
                print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
                return False
        except:
            print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            return False
        else:
            print("{} User query: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            return True
        finally:
            db.session.close()

#
# class UserTokenApi(Resource):
#     # @auth.login_required
#     def get(self):
#         print('UserTokenApi.get.url = ' + str(request.url))
#         token = generator_auth_token(expiration=600)
#         return jsonify({'token': token.decode('ascii')})


class UserLoginApi(Resource):
    def post(self):
        print('UserLoginApi.post.url = ' + str(request.url))
        user_info = parser.parse_args()
        u = User.query.filter_by(username=user_info.get('username')).first()
        try:
            if u is None or u.verify_password(user_info.get('password')) is False:
                print("{} User query: {} login failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
                return False
        except:
            print("{} User query: {} login failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            return False
        else:
            print("{} User query: {} login success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_info['username']))
            token = generator_auth_token(u.id)
            return jsonify({'token': token})
        finally:
            db.session.close()

api_user.add_resource(UserApi, '/user')
api_user.add_resource(UserVerifyApi, '/userverify', endpoint='userverify')
# api_user.add_resource(UserTokenApi, '/usertoken', endpoint='usertoken')
api_user.add_resource(UserLoginApi, '/login')