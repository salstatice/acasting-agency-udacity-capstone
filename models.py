import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
  '''
  setup_db(app)
    binds a flask application and a SQLAlchemy service.
  '''
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  migrate = Migrate(app, db)



class Actor(db.Model):
  '''
  Actor
  Have name, age and gender.
  '''  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  roles = db.relationship('Role', backref='actor', lazy=True)

  # adding assgined id for testing purpose

  # def __init__(self, id, name, age, gender=""):
  #   self.name = name
  #   self.age = age
  #   self.gender = gender

  def format(self):
    '''
    format()
      returns a json repsentation of the Actor model.
    '''
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
    }

  def insert(self):
    '''
    insert()
      inserts a new model into a database
      the model must have a unique id or null id
      EXAMPLE
        actor = Actor(name=req_name, age=req_age, gender=req_gender)
        actor.insert()
    '''
    db.session.add(self)
    db.session.commit()

  def update(self):
    '''
    update()
      updates a model in a database
      the model must exist in the database
      EXAMPLE
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        actor.age = 36
        actor.update()
    '''
    db.session.commit()

  def delete(self):
    '''
    delete()
      delets a model from a database
      the model must exist in the database
      EXAMPLE
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        actor.delete()
    '''
    db.session.delete(self)
    db.session.commit()

  def __repr__(self):
    return json.dumps(self.format())



class Movie(db.Model):
  '''
  Movie
  Have title and release date
  '''
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  date = Column(db.DateTime, nullable=False)
  roles = db.relationship('Role', backref='movie', lazy=True)

  # adding assgined id for testing purpose

  # def __init__(self, id, title, date):
  #   self.id = id
  #   self.title = title
  #   self.date = date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_year': self.date.strftime("%Y"),
    }
  
  def insert(self):
    '''
    insert()
      inserts a new model into a database
      the model must have a unique id or null id
      EXAMPLE
        movie = Movie(title=req_title, date=req_date)
        movie.insert()
    '''
    db.session.add(self)
    db.session.commit()

  def update(self):
    '''
    update()
      updates a model in a database
      the model must exist in the database
      EXAMPLE
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        movie.title = "New Movie"
        movie.update()
    '''
    db.session.commit()

  def delete(self):
    '''
    delete()
      delets a model from a database
      the model must exist in the database
      EXAMPLE
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        movie.delete()
    '''
    db.session.delete(self)
    db.session.commit()

  def __repr__(self):
    return json.dumps(self.format())



class Role(db.Model):
  '''
  Role
  Have role name, actor name and related movie
  '''
  __tablename__ = 'Role'

  id = Column(Integer, primary_key=True)
  role_name = Column(String)
  actor_id = Column(Integer, db.ForeignKey('Actor.id'))
  movie_id = Column(Integer, db.ForeignKey('Movie.id'))

  # adding assgined id for testing purpose

  # def __init__(self, id, role_name, actor_id, movie_id):
  #   self.id = id
  #   self.role_name = role_name
  #   self.actor_id = actor_id
  #   self.movie_id = movie_id

  def format(self):
    return {
      'id': self.id,
      'role_name': self.role_name,
      'actor_id': self.actor_id,
      'actor_name': self.actor.name,
      'movie_id': self.movie_id,
      'movie_name': self.movie.title,
    }
  
  def insert(self):
    '''
    insert()
      inserts a new model into a database
      the model must have a unique id or null id
      EXAMPLE
        role = Role(role_name=req_role_name, actor_id=req_actor_id, movie_id=req_movie_id)
        role.insert()
    '''
    db.session.add(self)
    db.session.commit()

  def delete(self):
    '''
    delete()
      delets a model from a database
      the model must exist in the database
      EXAMPLE
        role = Role.query.filter(Role.id == id).one_or_none()
        role.delete()
    '''
    db.session.delete(self)
    db.session.commit()

  def __repr__(self):
    return json.dumps(self.format())
