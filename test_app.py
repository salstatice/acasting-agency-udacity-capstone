import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Actor, Movie, Role


### Set up database path and JWT token

database_path = os.environ['DATABASE_URL']
assistant_token = ''
director_token = ''
producer_token = ''



class ACastingTestCase(unittest.TestCase):
  ''' This class represents the ACasting test case'''
  @classmethod
  def setUpClass(cls):
    '''
		Define test variables and initialize app.
		'''
    cls.app = create_app()
    cls.client = cls.app.test_client
    cls.database_path = database_path
    setup_db(cls.app, cls.database_path)

    # binds the app to the current context(??)
    # not quite sure if I understand this part...
    #  
    # cls.app_context = cls.app.app_context():
    #   cls.db = SQLAlchemy()
    #   cls.db.init_app(cls.app)
    #   # create all tables
    #   cls.db.create_all()

    db.drop_all()

    # new actor use for testing
    cls.new_actor = {
      "name": "Amy",
      "age": 24,
      "gender": "Female"
    }

    # new movie use for testing
    cls.new_movie = {
      "title": "100 Days of Eraser",
      "date": "2056-01-31"
    }
  
  def setUp(self):
    '''Excutes before each test'''
    # create table
    db.create_all()
    
    # mock actor
    actor1 = Actor(name="First Actor", age=2, gender="Male")

    # mock movie
    movie1 = Movie(title="First Movie", date="2020-12-12")

    # mock role
    role1 = Role(role_name="First Role", actor_id=1, movie_id=1)
    db.session.add_all([actor1, movie1, role1])
    db.session.commit()

  def tearDown(self):
    '''Excutes after each test'''
  

  @classmethod
  def tearDownClass(cls):
    '''Excutes once at the end of all test case'''
    pass

  #----------------------------------------
  # Test success behavior for /actors
  #----------------------------------------
  def test_get_actor_list(self):
    res = self.client().get('/actors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['actors']))

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()