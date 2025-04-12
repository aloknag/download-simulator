## File Download Simulator
This project is a File Download Simulator that simulates various types of file download scenarios, useful for testing and debugging. It combines a Vue.js frontend with a Flask backend and includes a custom Nginx reverse proxy to serve both frontend and backend from a single container.

## Build locally.
```
docker build -t download:latest .
```

## Run locally
```
docker run -it  -p 8089:80 --name download download:latest
```
