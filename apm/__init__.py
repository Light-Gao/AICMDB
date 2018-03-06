"""Initialize for whole application"""
from flask import Flask, redirect, url_for
from apm.controllers import servicemgr, usermgr
from apm.models import db
from apm.extensions import bcrypt
from apm.enums import globalenums

#create application function
def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    #will load SQLALCHEMY_DATABASE_URI from config.py to db object
    db.init_app(app)
    #init bcrypt object via app object
    bcrypt.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for(globalenums.DEFAULT_INDEX))

    #register Blueprint into app object
    app.register_blueprint(servicemgr.svc_blueprint)
    app.register_blueprint(usermgr.user_blueprint)

    return app
