# Library movies

API service for movie management written on DRF

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
