# Library movies

API service for movie management written on DRF

👉 [Link to the deployed project on the server](https://library-movies.onrender.com/api/movie/) - `LIVE Demo`


### Installing using GitHub

1. Clone the source code:

```bash
git clone https://github.com/MykytaKuzmytskyi/library_movies.git
cd library_movies
```
2. Install modules and dependencies:

```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

3. `.env_sample` 
This is a sample .env file for use in local development.
Duplicate this file as .env in the root of the project
and update the environment variables to match your
desired config. You can use [djecrety.ir](https://djecrety.ir/)

4. Use the command to configure the database and tables:

```bash
python manage.py migrate
```

5. Start the app:

```bash
python manage.py runserver
```
### Getting access

- You can use following superuser:
- Follow to `/admin/`
    - Login: `admin@admin.com`
    - Password: `admin12345`


*REST API documentation*
----
  **Actors Service**

 - POST:      `api/movie/actors/<id>/` - add new 
 - GET:       `api/movie/actors/`      - get a list of actors
 - GET:       `api/movie/actors/<id>/` - get actor's detail info 
 - PUT/PATCH: `api/movie/actors/<id>/` - update actor 
 - DELETE:    `api/movie/actors/<id>/` - delete actor

  **Directors Service**

 - POST:      `api/movie/directors/<id>/` - add new 
 - GET:       `api/movie/directors/`      - get a list of directors
 - GET:       `api/movie/directors/<id>/` - get director's detail info 
 - PUT/PATCH: `api/movie/directors/<id>/` - update director 
 - DELETE:    `api/movie/directors/<id>/` - delete director

  **Movie Service**

 - POST:      `api/movie/movies/<id>/` - add new 
 - GET:       `api/movie/movies/`      - get a list of movies
 - GET:       `api/movie/movies/<id>/` - get movie's detail info 
 - PUT/PATCH: `api/movie/movies/<id>/` - update movie 
 - DELETE:    `api/movie/movies/<id>/` - delete movie