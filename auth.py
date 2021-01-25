import os
import json
from jose import jwt
from flask import request
from functools import wraps
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

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

## Verify and decode jwt
#
# This is provided by Udcaity FSND in reference to a boilerplate
# provided by Auth0

# '''
# @TODO implement verify_decode_jwt(token) method
#     @INPUTS
#         token: a json web token (string)

#     it should be an Auth0 token with key id (kid)
#     it should verify the token using Auth0 /.well-known/jwks.json
#     it should decode the payload from the token
#     it should validate the claims
#     return the decoded payload

#     !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
# '''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

# Check permission

def check_permissions(permission, payload):
    '''
    check if the permission is cluded in the decoded jwt payload
        raise an AuthError if
        - permission is not included in JWT
        - required permission is not included in the payload permission
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True

# Auth decorator wrapper

def requires_auth(permission=''):
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
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        
        return wrapper
    return requires_auth_decorator

