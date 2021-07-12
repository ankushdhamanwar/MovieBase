from flask import Flask

from .extensions import mongo

def create_app(config_object = 'movieapp.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    mongo.init_app(app)

    from .main.routes import main
    app.register_blueprint(main)
    
    return app