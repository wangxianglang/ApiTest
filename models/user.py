import sys
from werkzeug.security import generate_password_hash, check_password_hash
sys.path.append("..")
from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 将password设置为私有属性，并且重命名
    _password = db.Column('password', db.String(128))

    # 定义一个属性，默认是读取的操作，这里报错，意思是不可读
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    # 定义上面那个password属性的可写属性，这里默认换算成哈希值，然后保存下来
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    # 校验传入的密码和哈希值是否是一对儿
    def verify_password(self, password):
        return check_password_hash(self._password, password)


    def __repr__(self):
        return "<User {}>".format(self.username)