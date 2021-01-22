import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, Role


### Set up database path and JWT token

database_path = os.environ['DATABASE_URL']
assistant_token = ''
director_token = ''
producer_token = ''



class ACastingTestCase(unittest.TestCase):
  ''' This class represents the ACasting test case'''

  def setUp(self):
    '''
		Define test variables and initialize app.
		'''

    self.app = create_app()
    self.client = self.app.test_client
    self.database_path = database_path
    setup_db(self.app, self.database_path)

    # binds the app to the current context(??)
    # not quite sure if I understand this part...
    #  
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

    # new actor use for testing
    self.new_actor = {
      "name": "Amy",
      "age": 24,
      "gender": "Female"
    }

    # new movie use for testing
    self.new_movie = {
      "title": "100 Days of Eraser",
      "date": "2056-01-31"
    }
  
  def tearDown(self):
    '''Excutes after each test'''
    pass


  #----------------------------------------
  # Test success behavior for /actors
  #----------------------------------------
  def test_get_actor_list(self):
    res = self.client().get('/actors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.isinstance(data['actors'], list)

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()