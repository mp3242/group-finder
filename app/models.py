from app import app
import flask.ext.whooshalchemy as whooshalchemy
import os.path

if not os.path.exists('whoosh_index'):
        os.mkdir("whoosh_index");
#use default app.config['WHOOSH_BASE']

class User(db.Model):
    __tablename__='user'
    __searchable__=['name','id']

    id=app.db.Column(app.db.Integer, primary_key=True)
    name=app.db.Column(app.db.Text)
    password=app.db.Column(app.db.Text)
    email=app.db.Column(app.db.Text)
    created=db.Column(db.DateTime,default=datetime.datetime.utcnow)

    def __repr__(self):
        return '{0}(title={1})'.format(self.__class__.__name__, self.name)
    
whooshalchemy.whoosh_index(app,User)

#ex: how to make a post
#db.session.add(User(name='Hidy',password='iwonttellyou',email='yh2635@columbia.edu'));db.session.commit()
