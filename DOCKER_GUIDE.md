# Docker Setup Guide for Image Gallery

## Prerequisites
- Docker installed
- Docker Compose installed

## Services Included

1. **MySQL 8.0** - Database server
   - Port: 3306
   - Database: image_gallery
   - User: gallery_user
   - Password: gallery_password

2. **Flask Application** - Web application
   - Port: 5000
   - Automatically creates tables on startup

3. **phpMyAdmin** - MySQL management interface
   - Port: 8080
   - Access: http://localhost:8080

## How to Start

### 1. Build and Start Services
```bash
docker-compose up -d
```

This will:
- Build the Flask application image
- Start MySQL container with initialized database
- Start Flask application on port 5000
- Start phpMyAdmin on port 8080
- Create necessary volumes and networks

### 2. Access the Application
- **Image Gallery:** http://localhost:5000
- **phpMyAdmin:** http://localhost:8080

### 3. Login Credentials
```
Username: admin
Password: admin123
```

## Services Status

### Check if Services are Running
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f flask_app
docker-compose logs -f mysql
```

### Access MySQL CLI
```bash
docker-compose exec mysql mysql -u gallery_user -p image_gallery
# Enter password: gallery_password
```

### Access Flask Shell
```bash
docker-compose exec flask_app python3
```

## Volumes

- **mysql_data** - Persists MySQL database between container restarts

## Networks

All services connected via `gallery_network` bridge network for inter-service communication.

## Stop Services

### Stop Containers
```bash
docker-compose stop
```

### Remove Containers (Keep Volumes)
```bash
docker-compose down
```

### Remove Everything (Including Database)
```bash
docker-compose down -v
```

## Environment Variables

Edit `.env.docker` to customize:
- `SECRET_KEY` - Session encryption key
- `DATABASE_URL` - Database connection string
- `UPLOAD_FOLDER` - Image storage path
- `DEBUG` - Debug mode

## Troubleshooting

### MySQL Connection Refused
- Wait 30 seconds for MySQL to fully start
- Check logs: `docker-compose logs mysql`

### Port Already in Use
- Change ports in docker-compose.yml
- Or stop other services: `docker-compose down`

### Database Not Initialized
- Delete volume: `docker-compose down -v`
- Restart: `docker-compose up -d`

### Application Crashes
- Check logs: `docker-compose logs flask_app`
- Verify MySQL is healthy: `docker-compose ps`

## Database Backup

### Create Backup
```bash
docker-compose exec mysql mysqldump -u gallery_user -p image_gallery > backup.sql
```

### Restore Backup
```bash
docker-compose exec mysql mysql -u gallery_user -p image_gallery < backup.sql
```

## Performance Tips

1. Use production-grade secrets
2. Set DEBUG=False in production
3. Consider using reverse proxy (nginx)
4. Enable persistent volumes for data
5. Set up monitoring and logging
6. Use resource limits in docker-compose.yml

## Production Deployment

For production, also:

1. Change root password in docker-compose.yml
2. Use strong passwords for database user
3. Remove phpMyAdmin service
4. Add environment file: `--env-file .env.production`
5. Configure proper networking
6. Set up backups strategy
7. Use health checks
8. Enable logging
9. Add rate limiting
10. Use HTTPS with reverse proxy

## Docker Commands Reference

```bash
# Build images
docker-compose build

# Start services (detached)
docker-compose up -d

# Start services (foreground)
docker-compose up

# Stop services
docker-compose stop

# Remove services
docker-compose down

# Remove everything including data
docker-compose down -v

# View running services
docker-compose ps

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec <service> <command>

# View resource usage
docker stats
```

## Network Access

| Service | Host | Port | URL |
|---------|------|------|-----|
| Flask App | localhost | 5000 | http://localhost:5000 |
| MySQL | mysql | 3306 | N/A (internal) |
| phpMyAdmin | localhost | 8080 | http://localhost:8080 |

## File Structure in Container

```
/app/
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   │   └── uploads/    (Volume mount)
│   └── __init__.py
├── run.py
├── init_db.py
└── requirements.txt
```

## Health Checks

MySQL has built-in health check that:
- Tests connection every 10 seconds
- Requires 2 successful checks before healthy
- Times out after 20 seconds
- Max 10 retries

Flask app starts after MySQL is healthy.
