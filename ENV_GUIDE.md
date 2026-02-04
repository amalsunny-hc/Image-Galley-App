# Environment Variables Configuration for Docker

## Overview
The Image Gallery application uses a single `.env` file for both local development and Docker deployment. Environment variables are shared across all services.

## .env File Variables

### Flask Configuration
```
FLASK_APP=run.py                           # Flask application entry point
FLASK_ENV=development                      # development or production
FLASK_PORT=5000                            # Port for Flask app
SECRET_KEY=your-secret-key-...            # Session encryption key
DEBUG=True                                 # Debug mode
```

### Database Configuration
```
# SQLite (Local Development)
DATABASE_URL=sqlite:///image_gallery.db   # SQLite database path

# MySQL (Docker Deployment)
MYSQL_ROOT_PASSWORD=rootpassword          # MySQL root password
MYSQL_DATABASE=image_gallery              # Database name
MYSQL_USER=gallery_user                   # MySQL user
MYSQL_PASSWORD=gallery_password           # MySQL password
MYSQL_PORT=3306                           # MySQL port
```

### File Upload Configuration
```
UPLOAD_FOLDER=app/static/uploads          # Image storage directory
MAX_FILE_SIZE=16777216                    # Max upload size (16MB)
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp # Allowed image formats
```

### Service Ports
```
FLASK_PORT=5000                           # Flask application port
MYSQL_PORT=3306                           # MySQL server port
PHPMYADMIN_PORT=8080                      # phpMyAdmin port
```

## Using .env with Docker Compose

The `docker-compose.yml` reads from `.env` using:

```yaml
env_file: .env
```

This loads all variables into the service environment automatically.

## Local Development Setup

### 1. Use SQLite (Default)

Ensure `.env` has:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///image_gallery.db
DEBUG=True
```

### 2. Run without Docker

```bash
python3 run.py
```

## Docker Deployment Setup

### 1. Update .env for Docker

```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-very-secure-key-here
MYSQL_PASSWORD=strong-password
```

### 2. Build and Start Services

```bash
docker-compose up -d
```

Services automatically read from `.env`:
- MySQL container receives: `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- Flask app receives: All Flask and upload variables
- phpMyAdmin receives: MySQL credentials

## Environment Variable Examples

### Development (.env)
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=dev-key-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///image_gallery.db
UPLOAD_FOLDER=app/static/uploads
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=gallery_password
MYSQL_PORT=3306

PHPMYADMIN_PORT=8080
```

### Production (.env)
```
FLASK_APP=run.py
FLASK_ENV=production
FLASK_PORT=5000
SECRET_KEY=your-production-secret-key-min-32-chars
DEBUG=False
DATABASE_URL=sqlite:///image_gallery.db
UPLOAD_FOLDER=app/static/uploads
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

MYSQL_ROOT_PASSWORD=very-strong-root-password
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=very-strong-user-password
MYSQL_PORT=3306

PHPMYADMIN_PORT=8080
```

## How Docker Compose Uses .env

### Example: MySQL Service
```yaml
mysql:
  image: mysql:8.0
  env_file: .env          # Load all variables from .env
  environment:
    MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-default}
    MYSQL_DATABASE: ${MYSQL_DATABASE:-image_gallery}
    MYSQL_USER: ${MYSQL_USER:-gallery_user}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD:-gallery_password}
```

This means:
- Variables from `.env` are loaded first
- `${VAR_NAME:-default}` uses value from .env, or default if not set
- Port mapping: `"${MYSQL_PORT:-3306}:3306"` allows custom port from .env

## Changing Configuration

### 1. For Local Development
Edit `.env`:
```
FLASK_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///image_gallery.db
```

### 2. For Docker Deployment
Edit `.env`:
```
FLASK_ENV=production
DEBUG=False
MYSQL_PASSWORD=your-secure-password
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## Environment Variable Precedence

In `docker-compose.yml`:

1. **env_file: .env** - Loads all variables from .env
2. **environment:** block - Overrides or adds specific variables
3. **${VAR:-default}** - Uses value from .env or default

Example:
```yaml
environment:
  MYSQL_PASSWORD: ${MYSQL_PASSWORD:-gallery_password}
```

- If `MYSQL_PASSWORD=secure123` in .env → uses `secure123`
- If `MYSQL_PASSWORD` not in .env → uses default `gallery_password`

## Common Tasks

### Change MySQL Password
1. Edit `.env`:
   ```
   MYSQL_PASSWORD=new-secure-password
   ```
2. Restart services:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Change Flask Port
1. Edit `.env`:
   ```
   FLASK_PORT=8000
   ```
2. Restart services:
   ```bash
   docker-compose restart flask_app
   ```

### Change phpMyAdmin Port
1. Edit `.env`:
   ```
   PHPMYADMIN_PORT=8888
   ```
2. Restart services:
   ```bash
   docker-compose restart phpmyadmin
   ```

### Enable Debug Mode in Docker
1. Edit `.env`:
   ```
   DEBUG=True
   FLASK_ENV=development
   ```
2. Restart:
   ```bash
   docker-compose restart flask_app
   ```

## Security Considerations

### For Production:

1. **Change Default Passwords**
   ```
   MYSQL_ROOT_PASSWORD=SecureRootPass123!
   MYSQL_PASSWORD=SecureUserPass456!
   SECRET_KEY=generate-random-secure-key
   ```

2. **Use Strong Keys**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Disable Debug**
   ```
   DEBUG=False
   FLASK_ENV=production
   ```

4. **Restrict Ports**
   - Don't expose ports publicly
   - Use firewall rules
   - Use reverse proxy (nginx)

5. **Backup .env**
   - Keep backup of production .env
   - Never commit to git
   - Add to .gitignore

## .gitignore Configuration

Make sure `.env` is ignored:
```
# .gitignore
.env
.env.local
.env.*.local
image_gallery.db
```

## Environment File Variants

### .env (Development - Default)
Used for local development with SQLite

### .env.docker (Alternative)
Optional separate file for Docker:
```bash
docker-compose --env-file .env.docker up -d
```

### .env.production (Best Practice)
Create for production deployment:
```bash
cp .env .env.production
# Edit .env.production with secure values
docker-compose --env-file .env.production up -d
```

## Accessing Environment Variables in Application

The Flask app accesses variables from `.env`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default-key')
DATABASE_URL = os.getenv('DATABASE_URL')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')
```

## Docker Environment Variable Reference

| Variable | Service | Default | Example |
|----------|---------|---------|---------|
| `FLASK_APP` | Flask | run.py | run.py |
| `FLASK_ENV` | Flask | development | production |
| `FLASK_PORT` | Flask | 5000 | 8000 |
| `DEBUG` | Flask | True | False |
| `SECRET_KEY` | Flask | generated | your-secret-key |
| `MYSQL_ROOT_PASSWORD` | MySQL | rootpassword | strong-pass |
| `MYSQL_DATABASE` | MySQL | image_gallery | - |
| `MYSQL_USER` | MySQL | gallery_user | - |
| `MYSQL_PASSWORD` | MySQL | gallery_password | - |
| `MYSQL_PORT` | MySQL | 3306 | - |
| `PHPMYADMIN_PORT` | phpMyAdmin | 8080 | - |

## Troubleshooting

### Variables Not Loading
```bash
# Check if .env exists
ls -la .env

# Check env_file in docker-compose.yml
cat docker-compose.yml | grep env_file
```

### Service Using Wrong Value
```bash
# Check running environment
docker-compose exec flask_app env | grep VAR_NAME
```

### Port Conflict
```bash
# Change in .env
FLASK_PORT=8000

# Restart
docker-compose restart flask_app
```

## Best Practices

1. ✅ Use `.env` for ALL configuration
2. ✅ Never commit `.env` to git
3. ✅ Use strong secrets in production
4. ✅ Document all variables
5. ✅ Use env_file in docker-compose.yml
6. ✅ Create separate .env files for different environments
7. ✅ Rotate passwords regularly
8. ✅ Use environment variable validation
9. ✅ Log configuration on startup (without secrets)
10. ✅ Keep backups of production .env

## Example Workflow

### Development
```bash
# Edit .env for development
FLASK_ENV=development
DEBUG=True

# Run locally
python3 run.py
```

### Testing with Docker
```bash
# Edit .env for Docker
FLASK_ENV=production
DEBUG=False

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Production
```bash
# Create separate file
cp .env .env.production

# Edit with secure values
nano .env.production

# Deploy with specific env file
docker-compose --env-file .env.production up -d
```
