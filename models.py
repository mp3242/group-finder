from flask.ext.sqlalchemy import SQLAlchemy
import os.path

from app import db


association_table=db.Table("association",db.Model.metadata,db.Column('left_id',db.Integer,db.ForeignKey('left.id')),db.Column('right_id',db.Integer,db.ForeignKey('right.id')))

class User(db.Model):
    __tablename__="left"
    id=db.Column(db.Integer, primary_key=True,unique=True)
    name=db.Column(db.String(64))
    password=db.Column(db.String(32))
    email=db.Column(db.String(120),unique=True)
    courses=db.relationship("Course",secondary=association_table,back_populates="users")
    #created=db.Column(db.DateTime,default=datetime.datetime.utcnow)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __init__(self,name,password,email):
        self.name=name
        self.password=password
        self.email=email

    def __repr__(self):
        return '<User %r>' % (self.name)
#ex: how to make a post
#db.session.add(User(name='Hidy',password='iwonttellyou',email='yh2635@columbia.edu'));db.session.commit()






class Course(db.Model):
    __tablename__='right'
    id=db.Column(db.Integer, primary_key=True)
    classname=db.Column(db.String(64))
    users=db.relationship('User',secondary=association_table,back_populates="courses")
    
    def __init__(self,classname):
        self.classname=classname

    def __repr__(self):
        return '<Call number: %r Class: %r>' % (self.id,self.classname)
