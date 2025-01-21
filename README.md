# Goodspeed
This repository holds code and tutorials for setting up cameras for Goodspeed parking.

## Key Components

### Database: SQLite
SQLite is a lightweight, file-based database system.

Note: The SQLite database file (`db.sqlite3`) is automatically excluded from version control by listing it in `.gitignore`.

### Backend: Django
Django is used to handle server-side logic, manage the database, and serve APIs, and host images for cameras. Key features include:

- APIs providing CRUD functionality for buildings, cameras, and parking spots.
- API for image upload for a specific camera

### Frontend: React
The project uses React with Typescript and Mantine components to provide an interactive user interface. Key features include:

- Snapshots of camera feeds based on building and camera number
- Parking spot polygons are overlayed on camera image, which are editable via draggable vertices
- Spot numbers are displayed as a label at the centroid of polygons which can be updated via double-click
- Can right-click parking spot polygons to bring up a context menu with a delete button

### Docker
Docker is used to containerize the application. Right now, there are containers for the frontend and backend. The `docker-compose` configuration defines these services.

## Example `.env` Configuration

```env
DEBUG='True'
ENV='development'
BACKEND_URL='http://localhost:8000'
FRONTEND_URL='http://localhost:5173'
ALLOWED_HOSTS='localhost'
SECRET_KEY= < a SHA256 key you would like to use for encryption. >
DJANGO_SETTINGS='config.settings'
LOCATION1 = 'halleyRise'
LOCATION2 = 'vertex1'
```

## Starting the Project

1. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

2. Once the containers are running, apply database migrations:
   ```bash
   docker exec -it <backend container id> python manage.py makemigrations
   docker exec -it <backend container id> python manage.py migrate
   ```

   Note: the backend container ID can be found using ```docker ps``` once the containers are running.

3. (Optional) Create a superuser for accessing the Django admin interface:
   ```bash
   docker exec -it backend python manage.py createsuperuser
   ```

4. Once the containers are running, the frontend is accessible at [http://localhost:5173](http://localhost:5173) and the backend is accessible at [http://localhost:8000](http://localhost:8000)

## Accessing Deployment Server: 

The server is deployed as an Amazon EC2 instance.

To access it, run the following command with a valid ```goodspeedparking.pem``` file:

```
ssh -i "goodspeedparking.pem" ec2-user@ec2-3-145-155-182.us-east-2.compute.amazonaws.com
```
