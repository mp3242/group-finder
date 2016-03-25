from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import os

#May need to change requirements.txt!
#remember you gotta type localhost:5000 !!!!

app = Flask(__name__)
app.config["DEBUG"] = True  # Only include this while you are testing your app
#app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

#from models import Result

#homepage
@app.route('/') #decorator= @app.route blablabla
def hello():
    #return "<h1>changed</h1>"
    #"Hello World!" #return HTML instead for webpages
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