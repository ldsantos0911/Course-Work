from flask import Flask

app = Flask(__name__)

from . import views

app.config.from_mapping(SECRET_KEY='dev')

# db.py, auth.py, login.html, register.html
# were copied and adapted from the flask tutorial at flask.pocoo.org
import db
db.init_app(app)

import auth
app.register_blueprint(auth.bp)

@app.route('/hello')
def hello():
    return 'Hello!'
