# EduTrack Administration Portal

This is a Django-based student enrollment and payment management portal.

## Why GitHub Pages did not work

GitHub Pages only hosts static files like `index.html`, CSS, and JavaScript.
This project is a Django application, so it needs:

- Python runtime
- Installed dependencies
- A database
- Django request handling on the server

Because of that, the full application must be deployed to a Python hosting platform such as Render or PythonAnywhere.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables:

```bash
cp .env.example .env
```

4. Set your real values in `.env`.
5. Run migrations:

```bash
python manage.py migrate
```

6. Start the server:

```bash
python manage.py runserver
```

## Render deployment

This repository includes:

- `build.sh`
- `render.yaml`
- environment-based Django settings

### Required environment variables

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `DB_SSL_REQUIRE=True` when your hosted database requires SSL

### Start command

```bash
gunicorn student_enrollment.wsgi:application
```

## Create the first admin login

This project uses its own `users` table, not Django's built-in admin user model.

On Render free instances, Shell access is not available, so the first admin user can be created automatically during deployment.
Add these environment variables in your Render web service:

- `ADMIN_NAME`
- `ADMIN_EMAIL`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

During the build, `build.sh` will automatically run the custom management command and create or update that login user.

Then log in from:

```text
/admin_login/
```

## Important note about the database

This project was originally connected to a local MySQL database.
For deployment, database credentials should come from environment variables instead of being hardcoded in `settings.py`.
