# Quick Reference Card - Unified .env

## One File. Three Ways to Deploy.

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│                    UNIFIED .env FILE                          │
│                 (Works for all scenarios!)                    │
│                                                               │
│  1. Copy: cp .env.example .env                              │
│  2. Edit: DEPLOYMENT_MODE=??? (see below)                   │
│  3. Configure: Add variables for your mode                  │
│  4. Deploy: Run app/docker/gunicorn                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Choose Your Deployment

### 🏠 LOCAL DEVELOPMENT (SQLite)

```env
DEPLOYMENT_MODE=local
DEBUG=True
SECRET_KEY=your-generated-key
```

**Setup:** Just copy `.env` and set `SECRET_KEY`  
**Database:** SQLite (file: `image_gallery.db`)  
**Run:** `python3 run.py`  
**Access:** `http://localhost:5000`  
**Best for:** Single developer testing

---

### 🐳 DOCKER LOCAL (MySQL)

```env
DEPLOYMENT_MODE=docker
DEBUG=True
SECRET_KEY=your-generated-key

MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123

PMA_HOST=mysql
PMA_USER=gallery_user
PMA_PASSWORD=user123
PMA_ROOT_PASSWORD=root123
```

**Setup:** Configure MySQL variables  
**Database:** MySQL in Docker container  
**Run:** `docker-compose up -d`  
**Access:** 
- App: `http://localhost:5000`
- phpMyAdmin: `http://localhost:8080`  
**Best for:** Team development, testing production-like setup

---

### ☁️ AWS PRODUCTION (RDS + S3)

```env
DEPLOYMENT_MODE=aws
DEBUG=False
FLASK_ENV=production
SECRET_KEY=your-generated-key

RDS_ENDPOINT=mydb.c9akciq32.us-east-1.rds.amazonaws.com
RDS_DATABASE=image_gallery
RDS_USER=admin
RDS_PASSWORD=rds-secure-password
RDS_PORT=3306

S3_BUCKET_NAME=image-gallery-bucket
AWS_REGION=us-east-1
```

**Setup:** Create RDS instance, S3 bucket, EC2 with IAM role  
**Database:** AWS RDS MySQL  
**Storage:** AWS S3  
**Run:** `gunicorn -w 4 -b 0.0.0.0:5000 run:app`  
**Access:** `http://your-domain.com`  
**Best for:** Production deployment, scaling, reliability

---

## Environment Variables Summary

### Required (All Scenarios)
```
FLASK_APP=run.py
SECRET_KEY=generated-secret-key-here
DEPLOYMENT_MODE=local|docker|aws
DEBUG=True|False
```

### Optional (All Scenarios)
```
FLASK_ENV=development|production
FLASK_PORT=5000
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
```

### Docker Only (When DEPLOYMENT_MODE=docker)
```
MYSQL_ROOT_PASSWORD=...
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=...
PMA_HOST=mysql
PMA_USER=gallery_user
PMA_PASSWORD=...
PMA_ROOT_PASSWORD=...
```

### AWS Only (When DEPLOYMENT_MODE=aws)
```
RDS_ENDPOINT=...
RDS_DATABASE=image_gallery
RDS_USER=admin
RDS_PASSWORD=...
RDS_PORT=3306
S3_BUCKET_NAME=...
AWS_REGION=us-east-1
```

---

## Setup Flowchart

```
Start
  ↓
Copy .env.example → .env
  ↓
Generate SECRET_KEY
  ↓
Choose Deployment Mode:
  ├─ Local? → Set DEPLOYMENT_MODE=local → Run python3 run.py
  ├─ Docker? → Add MYSQL_* → Set DEPLOYMENT_MODE=docker → docker-compose up -d
  └─ AWS? → Add RDS_*,S3_* → Set DEPLOYMENT_MODE=aws → Deploy to EC2
  ↓
Done! 🚀
```

---

## Database Connection Strings

### SQLite (Local)
```
sqlite:///image_gallery.db
```

### MySQL Docker
```
mysql+pymysql://gallery_user:password@mysql:3306/image_gallery
```

### AWS RDS
```
mysql+pymysql://admin:password@endpoint.rds.amazonaws.com:3306/image_gallery
```

*App builds these automatically - no manual configuration needed!*

---

## Common Commands

### Local
```bash
python3 run.py                          # Start dev server
```

### Docker
```bash
docker-compose up -d                    # Start all containers
docker-compose ps                       # Check status
docker-compose logs -f flask_app        # View logs
docker-compose down                     # Stop all containers
docker-compose down -v                  # Stop and remove volumes
```

### AWS (on EC2)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app  # Start with Gunicorn
# Or with Docker:
docker-compose -f docker-compose.aws.yml up -d
```

---

## Password Requirements

| Deployment | Min Length | Requirements |
|---|---|---|
| Local Dev | Any | No requirements |
| Docker Dev | 8+ | Should have uppercase & numbers |
| AWS Prod | 16+ | Uppercase, lowercase, numbers, special chars |

**Generate strong password:**
```bash
openssl rand -base64 32
```

---

## Migration Path

```
LOCAL (SQLite)
    ↓ want MySQL?
DOCKER (MySQL)
    ↓ deploying to cloud?
AWS (RDS + S3)
```

**Just change ONE line:** `DEPLOYMENT_MODE=???`

---

## Files Involved

### Configuration
- `.env.example` - Template (copy this to .env)
- `.env` - Your configuration (never commit!)

### Code
- `app/__init__.py` - Auto-detects DEPLOYMENT_MODE

### Docker
- `docker-compose.yml` - Local Docker setup
- `docker-compose.aws.yml` - AWS Docker setup

### Documentation
- `UNIFIED_ENV_SETUP.md` - Overview
- `UNIFIED_ENV_GUIDE.md` - Complete guide
- `.env.example` - Inline documentation

---

## Checklist

### Before Local Dev
- [ ] `.env` created
- [ ] `SECRET_KEY` set
- [ ] `DEPLOYMENT_MODE=local`

### Before Docker Dev
- [ ] All above ✓
- [ ] `DEPLOYMENT_MODE=docker`
- [ ] `MYSQL_*` configured
- [ ] `docker-compose up -d` successful

### Before AWS Deploy
- [ ] All above ✓
- [ ] `DEPLOYMENT_MODE=aws`
- [ ] RDS endpoint ready
- [ ] S3 bucket created
- [ ] EC2 with IAM role launched

---

## Key Points

✅ **One `.env` file** for all deployments  
✅ **Smart auto-detection** based on `DEPLOYMENT_MODE`  
✅ **No code changes** needed to switch deployments  
✅ **Easy migration** from local → docker → AWS  
✅ **Secure** (passwords in .env, never committed)  
✅ **Flexible** (all three modes supported equally)

---

## Need Help?

- **Setup Steps:** See `UNIFIED_ENV_GUIDE.md`
- **AWS Details:** See `AWS_DEPLOYMENT_GUIDE.md`
- **Quick Answers:** See `AWS_QUICK_REFERENCE.md`
- **All Options:** See `.env.example` (fully commented)

---

## TL;DR

```bash
# 1. Copy template
cp .env.example .env

# 2. Generate secret
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env

# 3. Choose mode (edit one line)
DEPLOYMENT_MODE=local     # or docker or aws

# 4. Add mode-specific vars
# For docker: add MYSQL_*
# For aws: add RDS_* and S3_*

# 5. Run!
python3 run.py            # local
# or
docker-compose up -d      # docker
# or
gunicorn ... run:app      # aws
```

**That's it! 🎉**
