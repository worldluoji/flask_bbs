from flask import Flask
from apps.communal import bp as comm_bp
from apps.forum import bp as forum_bp
from apps.management import bp as manage_bp
import config
from externs import db

app = None

def create_app():
    app = Flask(__name__)

    #app should register blue print
    app.register_blueprint(comm_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(manage_bp)

    #read the config file
    app.config.from_object(config)
    db.init_app(app)

    return app

def get_app():
    if app is not None:
        return app
    return create_app()


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
