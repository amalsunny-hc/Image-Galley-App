# Image Gallery - Unified Environment Configuration Guide

## Overview

This guide explains how to use the **single unified `.env`** file for all deployment scenarios:
- **Local Development** (SQLite)
- **Docker Local** (MySQL in container)
- **AWS Production** (RDS + S3)

## The Unified `.env` File

One `.env` file, three scenarios. Just change the `DEPLOYMENT_MODE` variable!

### Quick Start

```bash
# 1. Copy template
cp .env.example .env

# 2. Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env

# 3. Choose deployment mode (uncomment one):
# DEPLOYMENT_MODE=local    # SQLite
# DEPLOYMENT_MODE=docker   # Docker MySQL
# DEPLOYMENT_MODE=aws      # AWS RDS

# 4. Configure as needed for your mode (see below)
```

---

## Scenario 1: Local Development (SQLite)

**Best for:** Quick testing, single developer, no database setup

### Configuration

```env
DEPLOYMENT_MODE=local
DEBUG=True
FLASK_ENV=development
SECRET_KEY=your-generated-secret-key
```

### That's it! No database configuration needed.

The app will automatically create and use `image_gallery.db` in the project root.

### Run

```bash
python3 run.py
# Visit http://localhost:5000
```

### Files Created

- `image_gallery.db` - SQLite database file (local, not committed to git)
- `app/static/uploads/` - Local image uploads

---

## Scenario 2: Docker Local Development (MySQL)

**Best for:** Testing Docker setup, local team development, closer to production

### Configuration

```env
DEPLOYMENT_MODE=docker
DEBUG=True
FLASK_ENV=development
SECRET_KEY=your-generated-secret-key

# MySQL Configuration
MYSQL_ROOT_PASSWORD=root-pass-123  # 12+ chars, mixed case
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user-pass-123       # 12+ chars, mixed case

# PHPMyAdmin Configuration
PMA_HOST=mysql
PMA_USER=gallery_user
PMA_PASSWORD=user-pass-123
PMA_ROOT_PASSWORD=root-pass-123
```

### Run

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f flask_app

# Stop all services
docker-compose down

# Access
# - App: http://localhost:5000
# - phpMyAdmin: http://localhost:8080 (user: gallery_user, password: user-pass-123)
```

### What Happens

1. **MySQL Container** starts with your configured database
2. **Flask App Container** connects to MySQL automatically
3. **phpMyAdmin Container** provides GUI for database management

### Important Notes

- `DEPLOYMENT_MODE=docker` tells the app to use Docker MySQL
- `MYSQL_*` variables are used by both Docker and the app
- Volumes persist data between container restarts
- `docker-compose down` removes containers but keeps data in volumes

---

## Scenario 3: AWS Production (RDS + S3)

**Best for:** Production deployment, team collaboration, cloud-native setup

### Prerequisites

1. **AWS RDS MySQL Instance** created
   - Get the endpoint (e.g., `mydb.c9akciq32.us-east-1.rds.amazonaws.com`)
   - Note the password you set

2. **AWS S3 Bucket** created
   - Get the bucket name (e.g., `image-gallery-bucket`)

3. **EC2 Instance** with IAM role for S3 access
   - Or use ECS/Elastic Beanstalk

### Configuration

```env
DEPLOYMENT_MODE=aws
DEBUG=False
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key

# AWS RDS Configuration
RDS_ENDPOINT=mydb.c9akciq32.us-east-1.rds.amazonaws.com
RDS_DATABASE=image_gallery
RDS_USER=admin
RDS_PASSWORD=your-secure-rds-password
RDS_PORT=3306

# AWS S3 Configuration
S3_BUCKET_NAME=image-gallery-bucket
AWS_REGION=us-east-1
```

### Run on EC2

```bash
# SSH into EC2
ssh -i key.pem ec2-user@instance-ip

# Clone and setup
git clone https://github.com/your-repo/image_gallery.git
cd image_gallery

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Copy .env and configure
cp .env.example .env
# Edit .env with RDS and S3 details (see above)
nano .env

# Run with Gunicorn (production WSGI server)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Run with Docker on EC2

```bash
# Same setup, but instead of gunicorn:
docker-compose -f docker-compose.aws.yml up -d

# Check logs
docker-compose -f docker-compose.aws.yml logs -f flask_app
```

### What Happens

1. App detects `DEPLOYMENT_MODE=aws`
2. Connects to AWS RDS using `RDS_*` credentials
3. Uses S3 for image storage via IAM role
4. No local database or uploads directory needed

---

## Environment Variable Reference

### All Scenarios

```env
# Application
FLASK_APP=run.py              # Entry point
FLASK_ENV=development|production
FLASK_PORT=5000              # Port to listen on
SECRET_KEY=...               # Generated secret (min 32 chars)
DEBUG=True|False              # Debug mode
MAX_FILE_SIZE=16777216        # Max upload size (bytes)
ALLOWED_EXTENSIONS=jpg,...    # Allowed image formats
UPLOAD_FOLDER=...             # Local upload directory
DEPLOYMENT_MODE=local|docker|aws
```

### Scenario 2: Docker Only

```env
MYSQL_ROOT_PASSWORD=...       # MySQL root password
MYSQL_DATABASE=image_gallery  # Database to create
MYSQL_USER=gallery_user       # App database user
MYSQL_PASSWORD=...            # App database password
PMA_HOST=mysql                # phpMyAdmin host
PMA_USER=gallery_user         # phpMyAdmin user
PMA_PASSWORD=...              # phpMyAdmin password
PMA_ROOT_PASSWORD=...         # phpMyAdmin root password
```

### Scenario 3: AWS Only

```env
RDS_ENDPOINT=...              # RDS endpoint
RDS_DATABASE=image_gallery    # Database name
RDS_USER=admin                # RDS master user
RDS_PASSWORD=...              # RDS master password
RDS_PORT=3306                 # RDS port (default 3306)
S3_BUCKET_NAME=...            # S3 bucket name
AWS_REGION=us-east-1          # AWS region
```

---

## How the App Detects Configuration

The app (in `app/__init__.py`) automatically detects your deployment mode:

```python
# 1. Check DEPLOYMENT_MODE variable
deployment_mode = os.getenv('DEPLOYMENT_MODE', 'local').lower()

# 2. Determine which database to use
if deployment_mode == 'aws' and RDS_ENDPOINT exists:
    # Use AWS RDS MySQL
    # Connect with: mysql+pymysql://user:pass@endpoint/db
    
elif deployment_mode == 'docker' and MYSQL_USER exists:
    # Use Docker MySQL
    # Connect with: mysql+pymysql://user:pass@mysql:3306/db
    
else:
    # Default to SQLite
    # Use: sqlite:///image_gallery.db
```

**You don't need to do anything!** The app figures it out from your `.env` file.

---

## Migration Path

```
Local Development (SQLite)
         ↓ (want MySQL)
Docker Local (MySQL)
         ↓ (deploying to cloud)
AWS Production (RDS + S3)
```

All three configurations use the same `.env` file with just `DEPLOYMENT_MODE` changed!

### Example: Migrating from Local to Docker

**Local setup:**
```env
DEPLOYMENT_MODE=local
SECRET_KEY=my-secret-key
DEBUG=True
```

**Docker setup (just add MySQL variables):**
```env
DEPLOYMENT_MODE=docker
SECRET_KEY=my-secret-key
DEBUG=True
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
MYSQL_DATABASE=image_gallery
```

Run `docker-compose up -d` and you're done!

### Example: Migrating from Docker to AWS

**Docker setup:**
```env
DEPLOYMENT_MODE=docker
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
```

**AWS setup (replace with RDS variables):**
```env
DEPLOYMENT_MODE=aws
DEBUG=False
FLASK_ENV=production
RDS_ENDPOINT=mydb.xxx.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=rds-password
S3_BUCKET_NAME=my-bucket
```

Upload `.env` to EC2 and you're done!

---

## Common Issues & Solutions

### Issue: App can't connect to MySQL in Docker

**Problem:** `DEPLOYMENT_MODE=docker` but app tries to use SQLite

**Solution:** Make sure `MYSQL_USER` and `MYSQL_PASSWORD` are set in `.env`

**Check:**
```bash
grep "MYSQL_USER\|MYSQL_PASSWORD" .env
```

---

### Issue: RDS connection fails on AWS

**Problem:** `DEPLOYMENT_MODE=aws` but can't reach RDS

**Solution:** 
1. Verify RDS endpoint is correct: `grep RDS_ENDPOINT .env`
2. Check security group allows MySQL (3306) from EC2
3. Test connection: `mysql -h RDS_ENDPOINT -u admin -p`

---

### Issue: S3 upload fails on AWS

**Problem:** App runs but images don't upload to S3

**Solution:**
1. EC2 must have IAM role with S3 permissions
2. Bucket name must exist: `aws s3 ls s3://BUCKET_NAME`
3. Check S3_BUCKET_NAME in `.env`

---

### Issue: Can't decide which mode to use

**Scenario:** I'm alone, testing locally  
→ Use `DEPLOYMENT_MODE=local` (SQLite)

**Scenario:** My team is testing together  
→ Use `DEPLOYMENT_MODE=docker` (MySQL)

**Scenario:** Ready to go live  
→ Use `DEPLOYMENT_MODE=aws` (RDS + S3)

---

## Password Security

### For Local Development
- Short passwords are fine: `password`, `test123`
- Used only in containers, not accessible from outside

### For Docker Local
- Slightly stronger: `MyApp@Pass123!` (12+ chars, mixed case, special char)
- Still local, but good habit

### For AWS Production
- **MUST be strong**: `D$9mK#xL2pQ!w8vN` (16+ chars, mixed case, numbers, special chars)
- Directly accessible from internet
- Generate with: `openssl rand -base64 32`

---

## Final Checklist

### Before Local Development
- [ ] `.env` created from `.env.example`
- [ ] `SECRET_KEY` generated and set
- [ ] `DEPLOYMENT_MODE=local`
- [ ] Run `python3 run.py`

### Before Docker Development
- [ ] All above ✓
- [ ] `DEPLOYMENT_MODE=docker`
- [ ] `MYSQL_*` variables configured
- [ ] Run `docker-compose up -d`
- [ ] Check `docker ps` shows 3 containers

### Before AWS Deployment
- [ ] All above ✓
- [ ] `DEPLOYMENT_MODE=aws`
- [ ] RDS instance created and endpoint available
- [ ] S3 bucket created
- [ ] EC2 instance launched with IAM role
- [ ] `.env` uploaded to EC2
- [ ] App running on EC2 (via Gunicorn or Docker)

---

## Pro Tips

**1. Different .env files for different machines**
```bash
cp .env.example .env.local
cp .env.example .env.docker
cp .env.example .env.aws

# Use the right one
mv .env.docker .env
docker-compose up -d
```

**2. Quick switch between modes**
```bash
# Function in .bashrc or .zshrc
switch_env() {
    cp ".env.example" ".env"
    echo "DEPLOYMENT_MODE=$1" >> ".env"
}

switch_env local
switch_env docker
switch_env aws
```

**3. Never commit .env to git**
```bash
# This is already in .gitignore, but verify
cat .gitignore | grep "^\.env"
# Should show: .env
```

**4. Document your setup**
```bash
# Add to README for your team
echo "DEPLOYMENT_MODE=docker" > .env.default
git add .env.default
# Team copies: cp .env.default .env and edits it
```

---

## Next Steps

1. **Copy template:** `cp .env.example .env`
2. **Choose mode:** Edit `DEPLOYMENT_MODE` in `.env`
3. **Generate secret:** `python3 -c "import secrets; print(secrets.token_hex(32))"`
4. **Configure as needed:** Add `MYSQL_*` for Docker, `RDS_*` for AWS
5. **Deploy:** Run `python3 run.py`, `docker-compose up`, or push to EC2

That's it! 🚀
