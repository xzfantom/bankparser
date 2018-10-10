from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    #app.config.from_object(os.environ['APP_SETTINGS'])
    filepath = os.path.join(app.instance_path, "files")
    if not os.path.exists(filepath):
        os.makedirs(filepath)
        
    app.config['UPLOAD_FOLDER'] = filepath

    from . import index
    app.register_blueprint(index.bp)

    return app

