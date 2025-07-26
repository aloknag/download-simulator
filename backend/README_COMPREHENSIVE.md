# Download Simulator Backend

Flask-based API server for simulating various download scenarios useful for testing download managers, browsers, and other HTTP clients.

## Features

- **Basic Downloads**: Configurable file size with optional abort simulation
- **No Content-Length**: Downloads without Content-Length header for testing chunked transfer
- **Redirect Simulation**: Downloads with configurable redirect chains
- **HTTP Error Simulation**: Generate various 4xx HTTP error responses
- **CORS Support**: Cross-origin requests enabled for frontend integration

## API Endpoints

### Health Check
```
GET /healthcheck
```
Returns JSON status for monitoring.

### Basic Download
```
GET /api/download?size=<mb>&abortAfter=<mb>
```
- `size`: File size in MB (default: 10)
- `abortAfter`: Abort download after this many MB (optional)

Generates random binary data with proper headers for download managers.

### Download Without Content-Length
```
GET /api/download-no-length?size=<mb>
```
- `size`: File size in MB (default: 10)

Streams data without Content-Length header to test chunked transfer handling.

### Redirect Download
```
GET /api/redirect-download?redirects=<count>&size=<mb>
```
- `redirects`: Number of redirects before serving file (default: 0)
- `size`: Final file size in MB (default: 10)

Tests redirect handling in download clients.

### HTTP Error Simulation
```
GET /api/download-4xx?code=<error_code>
```
- `code`: HTTP error code to return (400, 401, 403, 404, 410, 418)

Simulates various HTTP error conditions.

## Installation

### Using Poetry (Recommended)
```bash
poetry install
poetry run python main.py
```

### Using pip
```bash
pip install flask flask-cors
python main.py
```

## Development

The server runs on `http://localhost:5000` by default.

### Configuration
- Debug mode: Set via Flask environment variables
- Port: Configured in `main.py` or via Flask settings
- CORS: Currently allows all origins (configure for production)

### Adding New Endpoints
1. Define route function in `main.py`
2. Add appropriate CORS headers if needed
3. Follow existing patterns for response handling

## Docker Usage

This backend is designed to run in the provided Docker container with nginx reverse proxy. See root directory for Docker setup.

## Security Considerations

- Input validation on all parameters
- Rate limiting should be implemented for production
- CORS configuration should be restricted for production
- Consider authentication for production deployments

## Testing

### Manual Testing
```bash
# Basic download
curl -O "http://localhost:5000/api/download?size=5"

# With abort
curl -O "http://localhost:5000/api/download?size=10&abortAfter=3"

# No content length
curl -O "http://localhost:5000/api/download-no-length?size=2"

# With redirects
curl -L -O "http://localhost:5000/api/redirect-download?redirects=3&size=1"

# Error simulation
curl -v "http://localhost:5000/api/download-4xx?code=404"
```

### Integration with Frontend
The backend integrates with the Vue.js frontend via the nginx reverse proxy configuration. Frontend requests to `/api/*` are proxied to this Flask server.

## Performance Notes

- Uses `os.urandom()` for generating test data
- Includes artificial delays (`time.sleep(0.1)`) to simulate real download conditions
- Memory usage scales with concurrent requests and file sizes
- Consider implementing streaming for very large file simulation

## Troubleshooting

### Common Issues
- **Poetry not found**: Install poetry first: `pip install poetry`
- **Python version**: Requires Python 3.11+ (check `pyproject.toml`)
- **Port conflicts**: Default port 5000 may conflict with other services
- **CORS errors**: Check frontend URL configuration

### Logs
Application uses print statements for debugging (should be replaced with proper logging in production).

## Contributing

1. Follow existing code style
2. Add input validation for new endpoints
3. Update this README for new features
4. Test with the frontend integration