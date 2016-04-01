from flask.ext.sqlalchemy import SQLAlchemy
import os.path

from app import db

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64))
    password=db.Column(db.String)
    email=db.Column(db.String)
    #created=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    def __init__(self,id,name,password,email):
        self.id=id
        self.name=name
        self.password=password
        self.email=email

    def __repr__(self):
        return '<User %r>' % (self.name)
#ex: how to make a post
#db.session.add(User(name='Hidy',password='iwonttellyou',email='yh2635@columbia.edu'));db.session.commit()
