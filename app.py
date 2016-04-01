from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User

from flask.ext.openid import OpenID
from config import basedir
import requests
from os.path import abspath, dirname, join

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app
app.config.from_object('config')
db=SQLAlchemy(app)

import models

##for login
lm=LoginManager()
lm.init_app(app)
oid=OpenID(app,os.path.join(basedir,'tmp'))
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        session['remember me']=form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['name','email'])
    return render_template('login.html',title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])

#homepage

#May need to change requirements.txt!
#remember you gotta type localhost:5000 !!!!

#app.config.from_object(os.environ['APP_SETTINGS'])


#homepage
@app.route('/') #decorator= @app.route blablabla
def hello():
    return render_template("hello.html")

#website
@app.route("/website")
def name():
  return "https://github.com/ADI-Labs/group-finder"

#search query
@app.route("/supersearch/<search_query>")
def supersearch(search_query):
  return search_query

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/add/<x>/<y>")
def add(x, y):
    return str(int(x) + int(y))

@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, this page was not found.", 404


if __name__ == '__main__':
    app.run() #host="0.0.0.0" implied
