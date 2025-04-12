FROM node:jod-slim@sha256:1c18d9ab3af4585870b92e4dbc5cac5a0dc77dd13df1a5905cea89fc720eb05b AS frontend

WORKDIR /frontend

# Copy frontend package and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend files
COPY frontend/ /frontend/

# Build the frontend application
RUN npm run build

# Use official Python and Node images
FROM python:3.13-bookworm@sha256:07bf1bd38e191e3ed18b5f3eb0006d5ab260cb8c967f49d3bf947e5c2e44d8a9

# Install nginx and supervisord
RUN apt-get update && apt-get install -y nginx
RUN apt-get install -y supervisor


# Set up the backend (Flask app)
WORKDIR /app

# Install dependencies for the backend using Poetry
COPY ./backend/pyproject.toml ./backend/poetry.lock ./
COPY ./backend/README.md ./
RUN pip install poetry

# Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN poetry install 
#--no-root

# # Activate env
# RUN poetry env activate

# Copy the main.py
COPY ./backend/main.py ./main.py

# Copy the compiled frontend build into the nginx directory
COPY --from=frontend /frontend/dist /usr/share/nginx/html

# Copy custom Nginx config file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Nginx (80)
# EXPOSE 5000??
EXPOSE 80

# Start supervisor to manage both Flask and Nginx
CMD ["/usr/bin/supervisord"]
