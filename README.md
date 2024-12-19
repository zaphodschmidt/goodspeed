# Goodspeed
This repository holds code and tutorials for setting up cameras for Goodspeed parking.

## Key Components

### Django
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It is used here to handle server-side logic, manage the database, and serve APIs.

### SQLite
SQLite is a lightweight, file-based database system. It is ideal for development and small-scale projects due to its simplicity and ease of setup. The SQLite database file (`db.sqlite3`) is automatically excluded from version control by listing it in `.gitignore`.

### Docker
Docker is used to containerize the application, providing an isolated and consistent environment. The `docker-compose` configuration defines the services required to run the application.

## Environment Files

- `.env.dev`: Contains environment variables for development, such as local URLs and debug settings.
- `.env.prod`: Contains environment variables for production, including secure keys and production URLs.

These files allow you to easily switch between development and production configurations.

## Starting the Project

1. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

2. Once the containers are running, apply database migrations:
   ```bash
   docker exec -it backend python manage.py makemigrations
   docker exec -it backend python manage.py migrate
   ```

3. (Optional) Create a superuser for accessing the Django admin interface:
   ```bash
   docker exec -it backend python manage.py createsuperuser
   ```

## Notes

- The database file (`db.sqlite3`) is excluded from version control via `.gitignore`.
- Make sure to update `.env.dev` and `.env.prod` with the correct environment variables before running the project.
- Always use `.env.prod` for production to ensure security and proper configuration.

## Example `.env` Configuration

### `.env.dev`
```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SECRET_KEY=dev-secret-key
BACKEND_URL=http://localhost:8000
```

### `.env.prod`
```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-production-domain.com
DJANGO_SECRET_KEY=prod-secret-key
BACKEND_URL=https://your-production-domain.com
```
