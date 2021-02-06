from flask_script import Manager, Server, Shell

from extensions import db
from models.user import User
from ApiTest import _create_app


app = _create_app()

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('runserver', Server(host='127.0.0.1', port=5000, use_debugger=True, use_reloader=True))
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run(default_command='runserver')
