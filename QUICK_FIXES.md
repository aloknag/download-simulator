# Quick Fixes - Immediate Actions Required

This document provides step-by-step instructions to fix the most critical issues identified in the download-simulator repository.

## 🚨 Critical Fixes (Do These First)

### 1. Fix NPM Security Vulnerabilities

```bash
cd frontend
npm audit fix
npm update
```

Expected output should show vulnerabilities resolved.

### 2. Fix Dockerfile Typo

**File:** `Dockerfile`  
**Line 1:** Change `jod-slim` to `node-slim`

```dockerfile
# Before
FROM node:jod-slim@sha256:1c18d9ab3af4585870b92e4dbc5cac5a0dc77dd13df1a5905cea89fc720eb05b

# After  
FROM node:20-slim@sha256:1c18d9ab3af4585870b92e4dbc5cac5a0dc77dd13df1a5905cea89fc720eb05b
```

### 3. Fix Python Version Requirement

**File:** `backend/pyproject.toml`  
**Line 9:** Change Python version requirement

```toml
# Before
requires-python =  ">=3.13,<4.0"

# After
requires-python = ">=3.11,<4.0"
```

### 4. Remove Unused Dependencies

**File:** `backend/pyproject.toml`  
**Lines 10-15:** Remove FastAPI and Uvicorn (not used)

```toml
# Before
dependencies = [
    "flask (>=3.1.0,<4.0.0)",
    "flask-cors (>=5.0.1,<6.0.0)",
    "fastapi (>=0.115.12,<0.116.0)",
    "uvicorn (>=0.34.0,<0.35.0)"
]

# After
dependencies = [
    "flask (>=3.1.0,<4.0.0)",
    "flask-cors (>=5.0.1,<6.0.0)"
]
```

## 🔧 Code Quality Fixes

### 5. Replace Print Statements with Logging

**File:** `backend/main.py`  
Add logging import and replace print statement:

```python
# Add at top of file
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace line 65
# Before:
print(f"Redirects: {redirects}, Size: {size_mb} MB")

# After:
logger.info(f"Processing redirect request - Redirects: {redirects}, Size: {size_mb} MB")
```

### 6. Add Input Validation

**File:** `backend/main.py`  
Replace lines 16-17 with validated input:

```python
# Add validation function after imports
def validate_positive_int(value, param_name, default=10, max_value=1000):
    try:
        result = int(value) if value else default
        if result <= 0:
            abort(400, f"{param_name} must be positive")
        if result > max_value:
            abort(413, f"{param_name} exceeds maximum allowed ({max_value})")
        return result
    except (ValueError, TypeError):
        abort(400, f"Invalid {param_name} parameter")

# Replace lines 16-17
# Before:
size_mb = int(request.args.get("size", 10))
abort_after_mb = int(request.args.get("abortAfter", size_mb))

# After:
size_mb = validate_positive_int(request.args.get("size"), "size")
abort_after_mb = validate_positive_int(request.args.get("abortAfter", size_mb), "abortAfter", size_mb)
```

### 7. Add Rate Limiting

**File:** `backend/main.py`  
Add Flask-Limiter for rate limiting:

```python
# Add to requirements in pyproject.toml
dependencies = [
    "flask (>=3.1.0,<4.0.0)",
    "flask-cors (>=5.0.1,<6.0.0)",
    "flask-limiter (>=3.0.0,<4.0.0)"
]

# Add imports
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Add after CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Add rate limiting to download endpoints
@app.route("/api/download")
@limiter.limit("10 per minute")
def basic_download():
    # existing code...

@app.route('/api/download-no-length')
@limiter.limit("10 per minute") 
def download_no_content_length():
    # existing code...

@app.route('/api/redirect-download')
@limiter.limit("5 per minute")
def redirect_download():
    # existing code...
```

## 🛡️ Security Headers Fix

### 8. Enhanced Nginx Security Headers

**File:** `nginx.conf`  
Replace lines 29-33 with comprehensive security headers:

```nginx
# Replace existing security headers with:
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; font-src 'self'; img-src 'self' data:; connect-src 'self';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## 📁 Missing Files

### 9. Create Backend .gitignore

**File:** `backend/.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Poetry
poetry.lock
```

### 10. Create Basic Backend README

**File:** `backend/README.md`

```markdown
# Download Simulator Backend

Flask-based API server for simulating various download scenarios.

## Features

- Basic file downloads with configurable size
- Download interruption simulation
- Redirect-based downloads
- Downloads without Content-Length header
- HTTP error simulation

## API Endpoints

- `GET /healthcheck` - Health check endpoint
- `GET /api/download?size=<mb>&abortAfter=<mb>` - Download with optional abort
- `GET /api/download-no-length?size=<mb>` - Download without Content-Length
- `GET /api/redirect-download?redirects=<count>&size=<mb>` - Download with redirects
- `GET /api/download-4xx?code=<http_code>` - Simulate HTTP errors

## Development

```bash
poetry install
poetry run python main.py
```

## Production

Use with the provided Docker configuration.
```

## 🧪 Verification Steps

After applying these fixes:

1. **Test backend installation:**
```bash
cd backend
poetry install
poetry run python main.py
```

2. **Test frontend build:**
```bash
cd frontend
npm install
npm run build
```

3. **Test Docker build:**
```bash
docker build -t download-simulator .
```

4. **Verify security headers:**
```bash
curl -I http://localhost:8089/ | grep -E "(X-|Content-Security|Strict-Transport)"
```

5. **Test rate limiting:**
```bash
# Should work first few times, then get rate limited
for i in {1..15}; do curl "http://localhost:8089/api/download?size=1"; done
```

## 🚀 Deploy Priority

1. **Immediate (today):** Steps 1-4 (security and build fixes)
2. **This week:** Steps 5-7 (code quality)  
3. **Next week:** Steps 8-10 (security and documentation)

## ⚠️ Testing Required

- Test all API endpoints still work after validation changes
- Verify Docker container starts successfully
- Check that rate limiting doesn't block legitimate usage
- Ensure frontend can still communicate with backend