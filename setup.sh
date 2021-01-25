database_name="acasting"

# flask setup
export FLASK_APP=app.py
export FLASK_ENV=development

# database setup
export DATABASE_URL="***REMOVED***"

# Auth0 api jwt setup
export AUTH0_DOMAIN="acasting.us.auth0.com"
export ALGORITHMS=['RS256']
export API_AUDIENCE="casting"