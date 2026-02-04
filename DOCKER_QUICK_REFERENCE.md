# Docker Quick Reference

## 🚀 Quick Start with Docker

### 1. Start Docker Services
```bash
docker-compose up -d
```

### 2. Access Application
```
📱 Gallery: http://localhost:5000
🗄️  phpMyAdmin: http://localhost:8080
```

### 3. Login
```
Username: admin
Password: admin123
```

## 📝 Configuration

All configuration comes from `.env` file:

```bash
# Edit environment variables
nano .env

# Restart services to apply changes
docker-compose restart
```

## 🔑 Key Environment Variables

```
# Flask Settings
FLASK_ENV=production          # Set to 'production' for Docker
DEBUG=False                   # Disable debug in production
FLASK_PORT=5000             # Application port
SECRET_KEY=your-secret-key   # Session encryption

# MySQL Settings
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_PASSWORD=gallery_password
MYSQL_USER=gallery_user
MYSQL_DATABASE=image_gallery

# Upload Settings
UPLOAD_FOLDER=app/static/uploads
MAX_FILE_SIZE=16777216
```

## 📊 Services

| Service | Port | URL |
|---------|------|-----|
| Flask App | 5000 | http://localhost:5000 |
| MySQL | 3306 | Internal only |
| phpMyAdmin | 8080 | http://localhost:8080 |

## 🎮 Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose stop

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f flask_app
docker-compose logs -f mysql

# Restart services
docker-compose restart

# Remove everything
docker-compose down -v

# Execute command in container
docker-compose exec flask_app python3 command.py
docker-compose exec mysql mysql -u gallery_user -p image_gallery
```

## 🔍 Check Status

```bash
# View running services
docker-compose ps

# View resource usage
docker stats

# View service health
docker-compose logs mysql | grep "healthy"
```

## 🗄️ Database

### Access MySQL CLI
```bash
docker-compose exec mysql mysql -u gallery_user -p image_gallery
# Password: gallery_password
```

### Backup Database
```bash
docker-compose exec mysql mysqldump -u gallery_user -p image_gallery > backup.sql
```

### Restore Database
```bash
docker-compose exec mysql mysql -u gallery_user -p image_gallery < backup.sql
```

## ⚠️ Troubleshooting

### Services Not Starting
```bash
# Check logs
docker-compose logs

# Verify .env file
cat .env

# Check ports are available
netstat -tuln | grep 5000
netstat -tuln | grep 3306
```

### MySQL Connection Error
```bash
# Wait for MySQL to start (30-60 seconds)
sleep 30

# Check MySQL health
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql
```

### Port Already in Use
Edit `.env`:
```
FLASK_PORT=8000
MYSQL_PORT=3307
PHPMYADMIN_PORT=8081
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

## 🔐 Security

### For Production:

1. **Change Passwords in .env**
   ```
   MYSQL_ROOT_PASSWORD=StrongPass123!
   MYSQL_PASSWORD=SecurePass456!
   SECRET_KEY=GeneratedSecureKey
   ```

2. **Set Production Mode**
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

3. **Backup .env**
   ```bash
   cp .env .env.backup
   ```

4. **Never Commit .env**
   - Already in .gitignore
   - Keep production .env separately

## 📂 File Structure

```
app/
├── static/uploads/          # Image storage (volume)
├── templates/               # HTML templates
├── models/                  # Database models
└── routes/                  # API routes

docker-compose.yml          # Container configuration
.env                        # Environment variables
Dockerfile                  # Flask app image
init.sql                    # Database initialization
```

## 🔄 Workflow

### Development to Docker

1. **Develop locally:**
   ```bash
   FLASK_ENV=development
   DATABASE_URL=sqlite:///image_gallery.db
   python3 run.py
   ```

2. **Test with Docker:**
   ```bash
   FLASK_ENV=production
   # No DATABASE_URL (uses MySQL)
   docker-compose up -d
   ```

3. **Deploy:**
   ```bash
   cp .env .env.production
   # Edit with secure values
   docker-compose --env-file .env.production up -d
   ```

## 📞 Support

- **Docker Guide:** See DOCKER_GUIDE.md
- **Env Configuration:** See ENV_GUIDE.md
- **Full Documentation:** See README.md

---

**Quick Commands Summary:**
```bash
docker-compose up -d        # Start
docker-compose stop         # Stop
docker-compose logs -f      # Logs
docker-compose down -v      # Remove all
```
