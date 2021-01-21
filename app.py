import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, Role

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
    try:
      actors = Actor.query.all()

      formatted_actors = [actor.format() for actor in actors]

      return jsonify({
        'success': True,
        'action': 'get all actors',
        'actors': formatted_actors,
      })
    except:
      abort(422)

  @app.route('/actors', methods = ['POST'])
  def add_actor():
    try:
      body = request.get_json()
      if body is None:
        abort(400)
      
      # only allow assgin id for testing purpose 
      req_id = body.get('id')
      checkActor = Actor.query.filter(Actor.id == req_id).one_or_none()
      if checkActor:
        abort(400)

      req_name = body.get('name')
      req_age = body.get('age')
      req_gender = body.get('gender')

      actor = Actor(id=req_id, name=req_name, age=req_age, gender=req_gender)
      actor.insert()

      return jsonify({
        'success': True,
        'action': 'add a new actor',
      })
    # except TypeError:
    #   abort(400)
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/actors/<int:id>', methods = ['GET'])
  def get_actor_detail(id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if not actor:
        abort(404)
      
      formatted_actor = [actor.format()]

      return jsonify({
        'success': True,
        'action': 'get a actor',
        'actors': formatted_actor,
      })
    except:
      abort(422)

  @app.route('/actors/<int:id>', methods = ['PATCH'])
  def edit_actor(id):
    try:
      body = request.get_json()
      if body is None:
        abort(400)

      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if not actor:
        abort(404)
      
      if body.get('name'):
        actor.name = body.get('name')
      elif body.get('age'):
        actor.age = body.get('age')
      elif body.get('gender'):
        actor.gender = body.get('gender')
      else:
        abort(400)

      actor.update()

      formatted_actor = [actor.format()]

      return jsonify({
        'success': True,
        'action': 'edit an existing actor',
        'actors': formatted_actor,
      })
    except Exception as e:
      abort(422)

  @app.route('/actors/<int:id>', methods = ['DELETE'])
  def delete_actor(id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if not actor:
        abort(404)

      actor.delete()
    
      return jsonify({
        'success': True,
        'action': 'delete an existing actor',
      })
    except:
      abort(422)
  



  '''
  Decorators for Movies
  '''
  @app.route('/movies', methods = ['GET'])
  def get_movies():
    try:
      movies = Movie.query.all()

      formatted_movies = [movie.format() for movie in movies]

      return jsonify({
        'success': True,
        'action': 'get all movies',
        'movies': formatted_movies,
      })
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/movies', methods = ['POST'])
  def add_movie():
    try:
      body = request.get_json()
      if body is None:
        abort(400)

      # only allow assgin id for testing purpose 
      req_id = body.get('id')
      checkMovie = Movie.query.filter(Movie.id == req_id).one_or_none()
      if checkMovie:
        abort(400)

      req_title = body.get('title')
      req_date = body.get('date')

      movie = Movie(id=req_id, title=req_title, date=req_date)
      movie.insert()

      return jsonify({
        'success': True,
        'action': 'add a new movie',
      })
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/movies/<int:id>', methods = ['GET'])
  def get_movie_detail(id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if not movie:
        abort(404)

      formatted_movie = [movie.format()]

      return jsonify({
        'success': True,
        'action': 'get a movie',
        'movies': formatted_movie,
      })
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/movies/<int:id>', methods = ['PATCH'])
  def edit_movie(id):
    try:
      body = request.get_json()
      if body is None:
        abort(400)
      
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if not movie:
        abort(404)
      
      if body.get('title'):
        movie.title = body.get('title')
      elif body.get('date'):
        movie.date = body.get('date')
      else:
        abort(400)

      movie.update()

      formatted_movie = [movie.format()]

      return jsonify({
        'success': True,
        'action': 'edit an existing movie',
        'movies': formatted_movie,
      })
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods = ['DELETE'])
  def delete_movie(id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if not movie:
        abort(404)
      
      movie.delete()

      return jsonify({
        'success': True,
        'action': 'delete an existing movie',
      })
    except:
      abort(422)
  


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