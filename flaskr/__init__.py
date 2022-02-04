import os
import sys

from flask import Flask, render_template, g, abort
from flask_mail import Mail

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = 'dev',
            DATABASE = os.path.join(app.instance_path, 'flask.sqlite'),
            TEMPLATE_AUTO_RELOAD = True
                )


    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    app.config['mail'] = Mail(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
       pass 

    from . import auth
    from . import db
    from . import blog
    from . import equipments_data

    app.config['equipments_data'] = equipments_data.EQUIPMENTS_DATA

    @app.route('/')
    def main():
        data = equipments_data.EQUIPMENTS_DATA
        return render_template('index.html', equipments_data=data)

    db.init_app(app) 
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    return app

