from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
#from .forms import LoginForm
#from .models import User

from flask.ext.openid import OpenID
from config import basedir
import requests
from os.path import abspath, dirname, join
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app
app.config.from_object('config')
db=SQLAlchemy(app)

import models

##for login
lm=LoginManager()
lm.init_app(app)
oid=OpenID(app,join(basedir,'tmp'))
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    #if g.user is not None and g.user.is_authenticated:
    #    return redirect(url_for('index'))
    #form=LoginForm()
    #if form.validate_on_submit():
    #    session['remember me']=form.remember_me.data/
    #    return oid.try_login(form.openid.data, ask_for=['email','password'])
    return render_template('login.html')

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email =="":
        flash("Invalid login. Please try again.")
        return redirect(url_for('login'))
    user=User.query.filter_by(email=resp.email, password=resp.password).first()
    if user is None:
        email=resp.email
        name=resp.email.split('@')[0]
        
        user=User(name=name,password=resp.password,email=email)
        db.session.add(user)
        db.session.commit()
    remember_me=False
    if 'remember_me' in session:
        remember_me=session['remember me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next')or url_for('index'))

@app.route('/') #decorator= @app.route blablabla
def index():
    return render_template("index.html")

# @app.route("/search", methods=["POST", "GET"])
# def search():
#     if request.method == "POST":
#         url = "https://www.googleapis.com/books/v1/volumes?q=" + request.form["user_search"]
#         response_dict = requests.get(url).json()
#         return render_template("result_get.html", api_data=response_dict)
#     else: # request.method == "GET"
#         return render_template("search.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/searchClasses",methods = ['POST'])
def searchClasses():
    if request.method == 'POST':
        try:
            #capitalized
            user_search = request.form['user_search']
            sections=models.Course.query.filter(models.Course.classname==user_search).all()
            res=[]
            for i in range(len(sections)):
                res+=sections[i].find_classmates().all()
            #with sqlite3.connect("app.db") as con:
            #    cur = con.cursor()
                #Capitalized Coursename
            #    cur.execute('SELECT * FROM right WHERE classname=?',(user_search,))
            #    all_rows = c.fetchall()
            print(res, file=sys.stderr)
            msg = "search successful"
        except:
            msg = "error in search operation"
        finally:
            return render_template("results.html", search_results=res)
        #    con.close()

@app.route("/results")
def results():
    return render_template("results.html")

@app.route('/signup')
def new_student():
    return render_template('signup.html')

@app.route('/addrec',methods = ['POST'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']

            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO left (name,password,email) VALUES (?,?,?)",(name,password,email))
            
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            return render_template("result_add.html",msg = msg)
            con.close()

@app.route('/user_profile') #decorator= @app.route blablabla
def user_profile():
    return render_template("user_profile.html")

#error
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, this page was not found.", 404


if __name__ == '__main__':
    app.run() #host="0.0.0.0" implied
