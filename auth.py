import json
# from jose import jwt
from flask import request
from functools import wraps


class AuthError(Exception):
  def __init__(self, error, status_code):
    self.error = error
    self.status_code = status_code

## Auth Header

def get_token_check_auth_header():
  '''
  Check if request has the appropiate header
    raise an AuthError if
    - 'Authorization' not present in header
    - a malformed token present under 'Authorization'

    it split bearer and the token, and
    return the token part of the header
  '''
  # check for Auth in header

  if 'Authorization' not in request.headers:
    raise AuthError({
      'code': 'authorization_header_missing',
      'description': 'Authorication header is expected'
    }, 401)

  # check for bearer token header

  auth_header = request.headers['Authorization']
  header_parts = auth_header.split(' ')
  
  if len(header_parts) != 2:
    raise AuthError({
      'code':'invalid_authorization_header',
      'description': 'Expecting bearer token.'
    }, 401)
  elif header_parts[0].lower() != 'bearer':
    raise AuthError({
      'code':'invalid_authorization_header',
      'description': 'Authorization header must start with "Bearer".'
    }, 401)

  # return token
  return header_parts[1]


def requires_auth(permissions=''):
	'''
	Get permission and pass it to wraper for
		verifying header
		validate jwt
		check permission
	'''
	def requires_auth_decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			token = get_token_check_auth_header()

			return f(token, *args, **kwargs)
		
		return wrapper
	return requires_auth_decorator