# ACasting Agency - Capstone Project for Udacity Full Stack Nanodegree
Capstone Project for Udacity Full Stack Nanodegree



## API Reference
----------------------
### Getting Started
- Base URL: 
  - The app is hosted at https://acasting-agency.herokuapp.com/
  - When run locally, the backend app is hosted at the default `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

- API Keys /Authentication (if applicable):
 - This app use [Auth0](https://auth0.com/) for authentication. To gain access:
   - signup using [this link](https://acasting.us.auth0.com/authorize?audience=casting&response_type=token&client_id=btnPsM39RGK8lqycZQVRx6gwvTiakglc&redirect_uri=https://acasting-agency.herokuapp.com/), then email koutest1001@gmail.com for role permission, or
   -  (for Udacity reviewer) use jwt token provided in student notes

### Error Handling
Errors are returned as JSON objects in one of the two following format:

**Failed request**
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```
**Authorization error**
```
{
    "code": "unauthorized",
    "description": "Permission not found."
}
```
A list of expected response code:

- 200: successful request
- 400: bad request
- 401: unauthorized
- 404: resource not found
- 405: method not found
- 422: unprocessable

### Endpoint library

#### [Actors]

#### GET /actors

-  Get a list of all actors in JSON format
- Example:
```
   {
      "action": "get all actors",
      "actors": [
        {
          "age": 117,
          "gender": "Male",
          "id": 3,
          "name": "Link"
        }
      ],
      "success": true
   }
```

#### POST /actors

- Add an actor entity to database
 - actor has name, age, gender, and an unique id assigned by database
 - age must be an integer
  - return the new actor entity in JSON format
- Example:
```
    {
      "action": "add a new actor",
      "actors": [
        {
          "age": 117,
          "gender": "Male",
          "id": 3,
          "name": "Link"
        }
      ],
      "success": true
    }
```

#### GET /actors/{actor_id}

- Return actor's detail and related roles in JSON format
- Example:
```
  {
    "action": "get a actor",
    "actors": [
      {
        "age": 117,
        "gender": "Male",
        "id": 3,
        "name": "Link",
        "roles": [
          {
            "movie_id": 1,
            "movie_title": "The Legend of Zelda: Breath of the Wild",
            "role_id": 1,
            "role_name": "Hero who doesn't save the princess"
          }
        ]
      }
    ],
    "success": true
  }
```

#### PATCH /actors/{actor_id}

- Edit an existing actor entity
 - return the edited actor entity in JSON format
- Example:
```
    {
      "action": "edit an existing actor",
      "actors": [
        {
          "age": 117,
          "gender": "Male",
          "id": 3,
          "name": "Link"
        }
      ],
      "success": true
    }
```

#### DELETE /actors/{actor_id} 

- Delete an existing actor entity from database
 - return the deleted actor info in JSON format
- Example:
```
    {
      "action": "delete an existing actor",
      "deleted_actors": [
        {
          "age": 24,
          "gender": "Female",
          "id": 2,
          "name": "Amy"
        }
      ],
      "success": true
    }
```

#### [Movies]

#### GET /movies
- Get a list of movie entity in JSON format
- Example:
```
    {
      "action": "get all movies",
      "movies": [
        {
          "id": 1,
          "release_year": "2017",
          "title": "The Legend of Zelda: Breath of the Wild"
        }
      ],
      "success": true
    }
```

#### POST /movies

- Add a movie entity to database
 - Moive has title and date
 - date must be in an expected form
   - `'%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y',
      '%Y-%m-%d', '%y-%m-%d', '%m-%d-%Y', '%m-%d-$y'`
 - return new movie in JSON format
- Example:
```
    {
      "action": "add a new movie",
      "movies": [
        {
          "id": 1,
          "release_year": "2017",
          "title": "The Legend of Zelda: Breath of the Wild"
        }
      ],
      "success": true
    }
```

#### GET /movies/{movie_id}

- Return movie detail and related roles in JSON format
- Example:
```
    {
      "action": "get a movie",
      "movies": [
        {
          "id": 1,
          "release_year": "2017",
          "roles": [
            {
              "actor_id": 3,
              "actor_name": "Link",
              "role_id": 1,
              "role_name": "Hero who doesn't save the princess"
            }
          ],
          "title": "The Legend of Zelda: Breath of the Wild"
        }
      ],
      "success": true
    }
```

#### PATCH /movie/{movie_id}

- Edit an existing movie
 - date must be in an expected form
 - return edited movie in JSON format
- Example:
```
    {
      "action": "edit an existing movie",
      "movies": [
        {
          "id": 1,
          "release_year": "2017",
          "title": "The Legend of Zelda: Breath of the Wild"
        }
      ],
      "success": true
    }
```

#### DELETE /movie/{movie_id}

- Delete an existing actor entity from database
 - return the deleted actor info in JSON format
- Example:
```
    {
      "action": "delete an existing actor",
      "deleted_actors": [
        {
          "age": 24,
          "gender": "Female",
          "id": 2,
          "name": "Amy"
        }
      ],
      "success": true
    }
```

#### [Castings]

#### GET /castings

- Get a list of all roles in JSON format
- Example:
```
    {
      "action": "get all roles",
      "roles": [
        {
          "actor_id": 3,
          "actor_name": "Link",
          "id": 1,
          "movie_id": 1,
          "movie_name": "The Legend of Zelda: Breath of the Wild",
          "role_name": "Hero who doesn't save the princess"
        }
      ],
      "success": true
    }
```

#### POST /castings

- Add a role enitiy to database
 - role has role_name, actor_id and movie_id
 - actor_id and movie_id must be associated with an existing record
      from the database
 - return the new role in JSON format
- Example:
```
    {
      "action": "add a new role",
      "roles": [
        {
          "actor_id": 3,
          "actor_name": "Link",
          "id": 1,
          "movie_id": 1,
          "movie_name": "The Legend of Zelda: Breath of the Wild",
          "role_name": "Hero who doesn't save the princess"
        }
      ],
      "success": true
    }
```

#### DELETE /castings/{role_id}

- Delete an existing role from the database
 - return the delete role info in JSON format
- Example:
```
    {
      "action": "delete an role",
      "deleted_roles": [
        {
          "actor_id": 3,
          "actor_name": "Link",
          "id": 1,
          "movie_id": 1,
          "movie_name": "The Legend of Zelda: Breath of the Wild",
          "role_name": "Hero who doesn't save the princess"
        }
      ],
      "success": true
    }
```
