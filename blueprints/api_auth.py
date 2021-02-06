from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import jsonify, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from settings import DevelopConfig
from models.user import User

# auth = HTTPBasicAuth(scheme="JWT")
auth = HTTPTokenAuth()


@auth.error_handler
def unauthorized():
    error_info = '{}'.format('Invalid credentials')
    print('api.auth.unauthorized.error_info = ' + error_info)
    response = jsonify({'error': error_info})
    response.status_code = 403

    print('api.auth.unauthorized.response = ' + str(response))

    return response


# def verify_password_for_token(username, password):
#     """
#     验证输入的用户名和密码是否匹配
#     :param username: 用户名
#     :param password: 密码
#     :return: 匹配结果
#     """
#     user = User.query.filter_by(username=username).first()
#     # 注意一下，以后判断是否为空，还是写成 user is None 而不要写成 not user
#     # 这样写更容易理解一些
#     if user is None or not user.verify_password(password):
#         # 结果不匹配
#         return False
#
#     return True


# @auth.verify_password
# def verify_password(username_or_token, password):
#     user = verify_auth_token(username_or_token)
#     print("__________________")
#     print(username_or_token)
#     print(password)
#     print("__________________")
#     if user is None:
#         return verify_password_for_token(username_or_token, password)
#
#     return user


@auth.verify_token
def verify_token(token):
    # Config.SECRET_KEY:内部的私钥，这里写在配置信息里
    s = Serializer(DevelopConfig.SECRET_KEY)
    try:
        data = s.loads(token)
        print(data)
    except BadSignature:
        # AuthFailed 自定义的异常类型
        print("BadSignature..")
        return None
    except SignatureExpired:
        print("SignatureExpired..")
        return None
    # 校验通过返回True
    return True


def generator_auth_token(userid):
    s = Serializer(secret_key=DevelopConfig.SECRET_KEY, expires_in=DevelopConfig.TOKEN_EXPIRATION)
    token = s.dumps({'id': userid}).decode("ascii")
    return token


def verify_auth_token(token):
    s = Serializer(DevelopConfig.SECRET_KEY)

    try:
        data = s.loads(token)
    except SignatureExpired:
        print("SignatureExpired....")
        return None
    except BadSignature:
        print("BadSignature....")
        return None

    print(data)

    user = User.query.get(data.get('id'))

    return user