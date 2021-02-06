from flask import Flask

from settings import DevelopConfig
from extensions import db
from blueprints import api_bp

def register_blueprints(_app):
    _app.register_blueprint(api_bp)


def register_extensions(_app):
    db.init_app(_app)
    init_db(_app)


def init_db(_app: Flask):
    _app.app_context().push()
    db.drop_all()
    db.create_all()
    db.session.commit()


def _create_app():
    _app = Flask(__name__)
    _app.config.from_object(DevelopConfig)

    register_blueprints(_app)
    register_extensions(_app)

    return _app


app = _create_app()

# if __name__ == '__main__':
#     app.run()
