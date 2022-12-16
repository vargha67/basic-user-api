from flask import Flask
from config import Config
import database

from routes.user import user_routes


def create_app(config_type=Config):
    app = Flask(__name__)
    app.config.from_object(config_type)

    database.init_app(app)

    @app.errorhandler(Exception)
    def default_error_handler(err):
        print(f'Internal error {err}')
        return 'An internal error occurred while processing the request', 500

    app.register_blueprint(user_routes, url_prefix='/users')

    return app


if __name__ == "__main__":
    create_app().run()