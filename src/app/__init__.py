from flask import Flask

def create_app():
    app = Flask(__name__)
    #app.config.from_object(os.environ['APP_SETTINGS'])
    from . import index
    app.register_blueprint(index.bp)

    return app

