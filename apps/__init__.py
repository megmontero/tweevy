import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'root'
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

#from apps import oauth

from apps import views
