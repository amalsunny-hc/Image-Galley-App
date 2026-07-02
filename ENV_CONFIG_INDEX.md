# Environment Configuration - Complete Documentation

## 🎯 Start Here

Choose your scenario and follow the link:

### 🏠 **Local Development** (just getting started)
→ Read: [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) (2-minute quick start)

### 🐳 **Docker Local Development** (team testing)
→ Read: [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) + [`UNIFIED_ENV_GUIDE.md`](UNIFIED_ENV_GUIDE.md#scenario-2-docker-local-development-mysql)

### ☁️ **AWS Production** (deploying to cloud)
→ Read: [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md) + [`AWS_QUICK_REFERENCE.md`](AWS_QUICK_REFERENCE.md)

---

## 📚 All Configuration Documents

### Quick Reference Guides
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) | One-page visual reference for all modes | 2 min |
| [`UNIFIED_ENV_SETUP.md`](UNIFIED_ENV_SETUP.md) | Overview of the unified .env approach | 5 min |
| [`AWS_QUICK_REFERENCE.md`](AWS_QUICK_REFERENCE.md) | AWS commands and quick lookup | 3 min |

### Comprehensive Guides
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [`UNIFIED_ENV_GUIDE.md`](UNIFIED_ENV_GUIDE.md) | Complete guide for all three scenarios | 15 min |
| [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md) | Step-by-step AWS setup instructions | 20 min |
| [`AWS_DEPLOYMENT_CHECKLIST.md`](AWS_DEPLOYMENT_CHECKLIST.md) | Interactive deployment checklist | 5 min |

### Configuration Files
| File | Purpose |
|------|---------|
| [`.env.example`](.env.example) | Template for all scenarios (fully commented) |
| `.env` | Your actual configuration (create from `.env.example`) |
| [`.env.aws`](.env.aws) | Deprecated (kept for reference) |

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Copy template
cp .env.example .env

# 2. Generate secret
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env

# 3. Choose ONE mode
DEPLOYMENT_MODE=local      # SQLite
# DEPLOYMENT_MODE=docker   # MySQL in Docker  
# DEPLOYMENT_MODE=aws      # AWS RDS + S3

# 4. For Docker: add MySQL variables
# For AWS: add RDS_* and S3_* variables

# 5. Run
python3 run.py             # local
# docker-compose up -d     # docker
# gunicorn ... run:app     # aws
```

---

## 🎓 Learn By Scenario

### Scenario 1: Local Development
- **What:** Single developer, testing, SQLite database
- **Setup Time:** < 1 minute
- **Cost:** Free
- **Best for:** Quick prototyping, learning

**Steps:**
1. `cp .env.example .env`
2. Generate and set `SECRET_KEY`
3. Set `DEPLOYMENT_MODE=local`
4. Run `python3 run.py`

**Key Files:**
- [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) - 🏠 LOCAL DEVELOPMENT section
- [`.env.example`](.env.example) - Scenario 1 example

---

### Scenario 2: Docker Local Development
- **What:** Team testing, MySQL database, Docker setup
- **Setup Time:** 5-10 minutes
- **Cost:** Free (uses Docker)
- **Best for:** Team collaboration, production-like testing

**Steps:**
1. `cp .env.example .env`
2. Generate and set `SECRET_KEY`
3. Set `DEPLOYMENT_MODE=docker`
4. Configure `MYSQL_*` variables (passwords)
5. Run `docker-compose up -d`

**Key Files:**
- [`UNIFIED_ENV_GUIDE.md`](UNIFIED_ENV_GUIDE.md#scenario-2-docker-local-development-mysql) - Complete Docker guide
- [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) - 🐳 DOCKER LOCAL section
- [`.env.example`](.env.example) - Scenario 2 example

---

### Scenario 3: AWS Production
- **What:** Cloud deployment, RDS MySQL, S3 storage, IAM auth
- **Setup Time:** 20-30 minutes
- **Cost:** $25-50/month (or free tier)
- **Best for:** Production, scaling, reliability

**Steps:**
1. Create AWS RDS instance
2. Create S3 bucket
3. Launch EC2 with IAM role
4. `cp .env.example .env`
5. Set `DEPLOYMENT_MODE=aws`
6. Configure `RDS_*` and `S3_*` variables
7. Deploy with Gunicorn or Docker

**Key Files:**
- [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md) - Step-by-step guide
- [`AWS_QUICK_REFERENCE.md`](AWS_QUICK_REFERENCE.md) - Commands and lookup
- [`AWS_DEPLOYMENT_CHECKLIST.md`](AWS_DEPLOYMENT_CHECKLIST.md) - Interactive checklist
- [`.env.example`](.env.example) - Scenario 3 example

---

## 🔄 Migration Path

### Local → Docker
```bash
# Current .env
DEPLOYMENT_MODE=local
SECRET_KEY=...

# Updated .env - just add MySQL variables
DEPLOYMENT_MODE=docker
SECRET_KEY=...
MYSQL_ROOT_PASSWORD=...
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DATABASE=image_gallery

# Then run
docker-compose up -d
```

### Docker → AWS
```bash
# Current .env
DEPLOYMENT_MODE=docker
MYSQL_*=...

# Updated .env - replace with RDS variables
DEPLOYMENT_MODE=aws
RDS_ENDPOINT=...
RDS_USER=...
RDS_PASSWORD=...
RDS_DATABASE=image_gallery
S3_BUCKET_NAME=...

# Then deploy to EC2
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Local → AWS (Skip Docker)
```bash
# Direct: Update .env and deploy
DEPLOYMENT_MODE=local → DEPLOYMENT_MODE=aws
Add RDS_* and S3_* variables
Deploy to EC2
```

---

## 🎯 How It Works

The app automatically detects your deployment mode:

```python
# From app/__init__.py
deployment_mode = os.getenv('DEPLOYMENT_MODE', 'local')

if deployment_mode == 'aws':
    # Use AWS RDS MySQL
    # Builds: mysql+pymysql://user:pass@endpoint:3306/db
    
elif deployment_mode == 'docker':
    # Use Docker MySQL
    # Builds: mysql+pymysql://user:pass@mysql:3306/db
    
else:
    # Use SQLite
    # Uses: sqlite:///image_gallery.db
```

**No code changes needed!** Just set `DEPLOYMENT_MODE` in `.env`.

---

## 🔐 Security Checklist

### For All Scenarios
- [ ] `.env` file created from `.env.example`
- [ ] `.env` added to `.gitignore` (already done)
- [ ] `.env` never committed to git
- [ ] `SECRET_KEY` is unique and strong (32+ chars)

### For Docker
- [ ] `MYSQL_ROOT_PASSWORD` is 12+ chars
- [ ] `MYSQL_PASSWORD` is 12+ chars
- [ ] Both have uppercase, lowercase, numbers

### For AWS
- [ ] `RDS_PASSWORD` is 16+ chars
- [ ] RDS password has uppercase, lowercase, numbers, special chars
- [ ] EC2 has IAM role with S3 permissions
- [ ] RDS security group allows access from EC2
- [ ] DEBUG=False in production

---

## 📋 Configuration Variables Reference

### Always Required
```
FLASK_APP=run.py
SECRET_KEY=generated-secret-key
DEPLOYMENT_MODE=local|docker|aws
```

### Always Available
```
FLASK_ENV=development|production
FLASK_PORT=5000
DEBUG=True|False
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
UPLOAD_FOLDER=app/static/uploads
```

### Docker Only
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

### AWS Only
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

## ❓ Troubleshooting

### "App won't start"
1. Check `.env` exists: `ls -la .env`
2. Check `DEPLOYMENT_MODE` is set: `grep DEPLOYMENT_MODE .env`
3. Check `SECRET_KEY` is set: `grep SECRET_KEY .env`

### "Can't connect to database"
- **Local:** No setup needed, SQLite is default
- **Docker:** Check `docker-compose up -d` ran successfully
- **AWS:** Check `RDS_ENDPOINT` and `RDS_PASSWORD` are correct

### "Docker containers won't start"
- Check Docker running: `docker --version`
- Check MySQL variables: `grep MYSQL .env`
- View logs: `docker-compose logs mysql`

### "S3 upload fails on AWS"
- Check EC2 has IAM role with S3 permissions
- Check bucket exists: `aws s3 ls s3://BUCKET_NAME`
- Check `S3_BUCKET_NAME` in `.env`

---

## 📞 Still Need Help?

| Question | Answer |
|----------|--------|
| What's the difference between the three modes? | See [`ENV_QUICK_REFERENCE.md`](ENV_QUICK_REFERENCE.md) |
| How do I set up Docker locally? | See [`UNIFIED_ENV_GUIDE.md`](UNIFIED_ENV_GUIDE.md#scenario-2-docker-local-development-mysql) |
| How do I deploy to AWS? | See [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md) |
| What AWS commands do I need? | See [`AWS_QUICK_REFERENCE.md`](AWS_QUICK_REFERENCE.md) |
| What goes in my `.env` file? | See [`.env.example`](.env.example) |
| How do I migrate from Docker to AWS? | See [`UNIFIED_ENV_GUIDE.md`](UNIFIED_ENV_GUIDE.md#migration-path) |

---

## 🎉 Summary

✅ **One unified `.env`** works for all three scenarios  
✅ **Smart auto-detection** in the app (`DEPLOYMENT_MODE`)  
✅ **Easy migration** from local → docker → AWS  
✅ **Clear documentation** for each scenario  
✅ **Secure by default** (passwords, no access keys)  

Just choose your scenario, set `DEPLOYMENT_MODE`, and go! 🚀

---

## Files at a Glance

```
image_gallery/
├── .env.example                      ← Copy this to .env
├── .env                             ← Your configuration (never commit)
├── app/__init__.py                  ← Has DEPLOYMENT_MODE detection
├── docker-compose.yml               ← For local Docker
├── docker-compose.aws.yml           ← For AWS Docker
│
├── ENV_QUICK_REFERENCE.md          ← 2-min quick start
├── UNIFIED_ENV_SETUP.md            ← 5-min overview
├── UNIFIED_ENV_GUIDE.md            ← 15-min complete guide
├── AWS_DEPLOYMENT_GUIDE.md         ← 20-min AWS setup
├── AWS_QUICK_REFERENCE.md          ← AWS commands
├── AWS_DEPLOYMENT_CHECKLIST.md     ← Interactive checklist
└── ENV_CONFIG_INDEX.md             ← This file
```

**Pick a scenario, pick a guide, and start! 🎯**
