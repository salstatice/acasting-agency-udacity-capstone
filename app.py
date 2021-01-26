import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

from models import db, Actor, Movie, Role
from auth import AuthError, requires_auth

app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

trigger_deployment = "Attemp #2"
  
@app.route('/')
def welcome():
  return 'Welcome to the empty main page!'


#---------------------------------------
# Decorators for /actors
#---------------------------------------

@app.route('/actors', methods = ['GET'])
@requires_auth('get:actors')
def get_actors(payload):
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
@requires_auth('post:actors')
def add_actor(payload):
  try:
    body = request.get_json()
    if body is None:
      abort(400)

    req_name = body.get('name')
    req_age = body.get('age')
    req_gender = body.get('gender')

    if not isinstance(req_age,int):
      abort(400, {'message': 'age must be an integer'})

    actor = Actor(name=req_name, age=req_age, gender=req_gender)
    actor.insert()

    formatted_actor = [actor.format()]

    return jsonify({
      'success': True,
      'action': 'add a new actor',
      'actors': formatted_actor
    })
  except Exception as e:
    if e.code == 400:
      abort(400)
    else:
      abort(422)

@app.route('/actors/<int:id>', methods = ['GET'])
@requires_auth('get:actors')
def get_actor_detail(payload, id):
  try:
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
      abort(404)
    
    formatted_actor = [actor.format()]

    roles_list = [{
      'role_id': role.id, 
      'role_name': role.role_name,
      'movie_title': role.movie.title,
      'movie_id': role.movie.id
      } for role in actor.roles]
    
    formatted_actor[0]['roles'] = roles_list

    return jsonify({
      'success': True,
      'action': 'get a actor',
      'actors': formatted_actor,
    })
  except Exception as e:
    if e.code == 404:
      abort(404)
    else:
      abort(422)

@app.route('/actors/<int:id>', methods = ['PATCH'])
@requires_auth('patch:actors')
def edit_actor(payload, id):
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
      # verify age is integer
      if not isinstance(body.get('age'),int):
        abort(400)
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
    if e.code == 400:
      abort(400)
    elif e.code == 404:
      abort(404)
    else:
      abort(422)

@app.route('/actors/<int:id>', methods = ['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):
  try:
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
      abort(404)

    actor.delete()

    formatted_actor = [actor.format()]
  
    return jsonify({
      'success': True,
      'action': 'delete an existing actor',
      'deleted_actors': formatted_actor
    })
  except Exception as e:
    if e.code == 404:
      abort(404)
    else:
      abort(422)



#---------------------------------------
# Decorators for /movies
#---------------------------------------

@app.route('/movies', methods = ['GET'])
@requires_auth('get:movies')
def get_movies(payload):
  try:
    movies = Movie.query.all()

    formatted_movies = [movie.format() for movie in movies]

    return jsonify({
      'success': True,
      'action': 'get all movies',
      'movies': formatted_movies,
    })
  except Exception as e:
    abort(422)

@app.route('/movies', methods = ['POST'])
@requires_auth('post:movies')
def add_movie(payload):
  try:
    body = request.get_json()
    if body is None:
      abort(400)

    req_title = body.get('title')
    req_date = body.get('date')
    if req_date is None:
      abort(400)
    
    # This format string and sample is provided by dawg on 
    # https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
    fmts = ('%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y',
      '%Y-%m-%d', '%y-%m-%d', '%m-%d-%Y', '%m-%d-$y')
    is_datetime = False
    for fmt in fmts:
        try:
            t = datetime.strptime(req_date, fmt)
            is_datetime = True
            break
        except:
            pass
    if not is_datetime:
      abort(400)

    movie = Movie(title=req_title, date=req_date)
    movie.insert()

    formatted_movie = [movie.format()]

    return jsonify({
      'success': True,
      'action': 'add a new movie',
      'movies': formatted_movie,

    })
  except Exception as e:
    if e.code == 400:
      abort(400)
    else:
      abort(422)

@app.route('/movies/<int:id>', methods = ['GET'])
@requires_auth('get:movies')
def get_movie_detail(payload, id):
  try:
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
      abort(404)

    formatted_movie = [movie.format()]

    roles_list = [{
      'role_id': role.id, 
      'role_name': role.role_name,
      'actor_name': role.actor.name,
      'actor_id': role.actor.id
      } for role in movie.roles]

    formatted_movie[0]['roles'] = roles_list

    return jsonify({
      'success': True,
      'action': 'get a movie',
      'movies': formatted_movie,
    })
  except Exception as e:
    if e.code == 404:
      abort(404)
    else:
      abort(422)

@app.route('/movies/<int:id>', methods = ['PATCH'])
@requires_auth('patch:movies')
def edit_movie(payload, id):
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
      # This format string and sample is provided by dawg on 
      # https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
      fmts = ('%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y',
        '%Y-%m-%d', '%y-%m-%d', '%m-%d-%Y', '%m-%d-$y')
      is_datetime = False
      for fmt in fmts:
        try:
            t = datetime.strptime(body.get('date'), fmt)
            is_datetime = True
            movie.date = body.get('date')
            break
        except:
            pass
      if not is_datetime:
        abort(400)
    else:
      abort(400)

    movie.update()

    formatted_movie = [movie.format()]

    return jsonify({
      'success': True,
      'action': 'edit an existing movie',
      'movies': formatted_movie,
    })
  except Exception as e:
    if e.code == 400:
      abort(400)
    elif e.code == 404:
      abort(404)
    else:
      abort(422)

@app.route('/movies/<int:id>', methods = ['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):
  try:
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
      abort(404)
    
    movie.delete()

    formatted_movie = [movie.format()]

    return jsonify({
      'success': True,
      'action': 'delete an existing movie',
      'deleted_movies': formatted_movie,
    })
  except Exception as e:
    if e.code == 404:
      abort(404)
    else:
      abort(422)


#---------------------------------------
# Decorators for /castings
#---------------------------------------

@app.route('/castings', methods = ['GET'])
@requires_auth('get:castings')
def get_roles(payload):
  try:
    roles = Role.query.all()
    
    formatted_roles = [role.format() for role in roles]

    return jsonify({
      'success': True,
      'action': 'get all roles',
      'roles': formatted_roles
    })
  except:
    abort(422)

@app.route('/castings', methods = ['POST'])
@requires_auth('post:castings')
def add_role(payload):
  try:
    body = request.get_json()
    if body is None:
      abort(400)

    # actor_id and movie_id are required
    if not(body.get('actor_id') and body.get('movie_id')):
      abort(400)

    req_role_name = body.get('role_name')
    req_actor_id = body.get('actor_id')
    req_movie_id = body.get('movie_id')

    # actor and movie must exist in the database
    actor = Actor.query.filter(Actor.id == req_actor_id).one_or_none()
    movie = Movie.query.filter(Movie.id == req_movie_id).one_or_none()
    if not(actor and movie):
      abort(400)

    role = Role(role_name=req_role_name, actor_id=req_actor_id, movie_id=req_movie_id)
    role.insert()

    formatted_roles = [role.format()]

    return jsonify({
      'success': True,
      'action': 'add a new role',
      'roles': formatted_roles,
    })
  except Exception as e:
    if e.code == 400:
      abort(400)
    else:
      abort(422)

@app.route('/castings/<int:id>', methods = ['DELETE'])
@requires_auth('delete:castings')
def delete_role(payload, id):
  try:
    role = Role.query.filter(Role.id == id).one_or_none()
    if not role:
      abort(404)

    formatted_roles = [role.format()]

    role.delete()

    return jsonify({
      'success': True,
      'action': 'delete an role',
      'deleted_roles': formatted_roles,
    })
  except Exception as e:
    if e.code == 404:
      abort(404)
    else:
      abort(422)

#---------------------------------------
# Error Handling
#---------------------------------------
#   return 422, 400, 404, 405 and AuthError gracefully
#   Each error handler should return with error messages
#   EXAMPLE
#     jsonify({
#       "success": False, 
#       "error": 404,
#       "message": "resource not found"
#     }), 404
#
#   Authorization Errors are handlded differenrly by class AuthError
#   EXAMPLE
#     e.error = {
#       'code':'authorization_header_missing',
#       'description': 'Authriation header is expected'
#     }
#     e.status_code = 401
#       or
#     AuthError({
#       'code':'authorization_header_missing',
#       'description': 'Authriation header is expected'
#     }, 401)
#   return jsonify(e.error), e.status_code
#------------------------------------------

@app.errorhandler(422)
def unprocessable(error):
  '''
  Error handling for unprocessable entity
  '''
  return jsonify({
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }), 422

@app.errorhandler(400)
def bad_request(error):
  '''
  Error handling for bad request entity
  '''
  # if not hasattr(error, 'message'):
  #   error.message = 'bad request'
    
  return jsonify({
    'success': False,
    'error': 400,
    'message': 'bad request'
  }), 400

@app.errorhandler(404)
def resource_not_found(error):
  '''
  Error handling for resource not found entity
  '''
  return jsonify({
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }), 404

@app.errorhandler(405)
def method_not_found(error):
  '''
  Error handling for method not found entity
  '''
  return jsonify({
    "success": False, 
    "error": 405,
    "message": "method not found"
  }), 405

@app.errorhandler(AuthError)
def auth_error(e):
  '''
  Error handling for Auth Error
  '''
  return jsonify(e.error), e.status_code





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)