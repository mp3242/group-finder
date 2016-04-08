from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import requests
from os.path import abspath, dirname, join
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app
app.config.from_object('config')
db=SQLAlchemy(app)

import models

#source venv/bin/activate

#homepage

#May need to change requirements.txt!
#remember you gotta type localhost:5000 !!!!

#app.config.from_object(os.environ['APP_SETTINGS'])

#homepage
@app.route('/') #decorator= @app.route blablabla
def hello():
    return render_template("index.html")

#search query
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        url = "https://www.googleapis.com/books/v1/volumes?q=" + request.form["user_search"]
        response_dict = requests.get(url).json()
        return render_template("result_get.html", api_data=response_dict)
    else: # request.method == "GET"
        return render_template("search.html")

@app.route('/signup')
def new_student():
    return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        msg = "hello world"
        try:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']

            with sqlite3.connect("app.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO User (name,password,email) VALUES (?,?,?)",(name,password,email))
            
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            return render_template("result_add.html",msg = msg)
            con.close()

#error
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry, this page was not found.", 404

#NOT used
@app.route("/website")
def name():
    return "https://github.com/ADI-Labs/group-finder"

#NOT used
@app.route("/supersearch/<search_query>")
def supersearch(search_query):
    return search_query

#NOT used
@app.route("/add/<x>/<y>")
def add(x, y):
    return str(int(x) + int(y))

if __name__ == '__main__':
    app.run() #host="0.0.0.0" implied
