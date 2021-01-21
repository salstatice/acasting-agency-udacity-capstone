import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def welcome():
    return 'Welcome to the empty main page!'

  '''
  Decorators for Actors
  '''

  @app.route('/actors', methods = ['GET'])
  def get_actors():
    return jsonify({
      'success': True,
      'action': 'get all actors',
    })

  @app.route('/actors', methods = ['POST'])
  def add_actor():
    return jsonify({
      'success': True,
      'action': 'add a new actor',
    })

  @app.route('/actors/<int:id>', methods = ['GET'])
  def get_actor_detail(id):
    return jsonify({
      'success': True,
      'action': 'get a actor',
    })

  @app.route('/actors/<int:id>', methods = ['DELETE'])
  def delete_actor(id):
    return jsonify({
      'success': True,
      'action': 'delete an existing actor',
    })
  
  @app.route('/actors/<int:id>', methods = ['PATCH'])
  def edit_actor(id):
    return jsonify({
      'success': True,
      'action': 'edit an existing actor'
    })

  

  '''
  Decorators for Movies
  '''
  @app.route('/movies', methods = ['GET'])
  def get_movies():
    return jsonify({
      'success': True,
      'action': 'get all movies',
    })

  @app.route('/movies', methods = ['POST'])
  def add_movie():
    return jsonify({
      'success': True,
      'action': 'add a new movie',
    })

  @app.route('/movies/<int:id>', methods = ['GET'])
  def get_movie_detail(id):
    return jsonify({
      'success': True,
      'action': 'get a movie',
    })

  @app.route('/movies/<int:id>', methods = ['DELETE'])
  def delete_movie(id):
    return jsonify({
      'success': True,
      'action': 'delete an existing movie',
    })
  
  @app.route('/movies/<int:id>', methods = ['PATCH'])
  def edit_movie(id):
    return jsonify({
      'success': True,
      'action': 'edit an existing movie'
    })


  '''
  Decorators for Roles
  '''
  @app.route('/castings', methods = ['GET'])
  def get_roles():
    return jsonify({
      'success': True,
      'action': 'get all roles',
    })

  @app.route('/castings', methods = ['POST'])
  def add_role():
    return jsonify({
      'success': True,
      'action': 'add a new role',
    })

  @app.route('/castings/<int:id>', methods = ['DELETE'])
  def delete_role(id):
    return jsonify({
      'success': True,
      'action': 'delete an role',
    })

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)