# Unified Environment Setup - Complete

## What Changed?

You now have **ONE unified `.env` file** that works for all three deployment scenarios instead of multiple separate files.

### Before (Multiple Files)
```
.env.example      (template)
.env.aws          (AWS specific)
.env              (your copy)
```

### After (Unified Single File)
```
.env.example      (template for all scenarios)
.env              (your copy, works for all scenarios)
```

---

## How It Works

You control deployment with ONE variable: `DEPLOYMENT_MODE`

```env
# Choose ONE:
DEPLOYMENT_MODE=local      # SQLite, no setup needed
DEPLOYMENT_MODE=docker     # Docker MySQL, local dev
DEPLOYMENT_MODE=aws        # AWS RDS + S3, production
```

The app **automatically detects** which mode you're in and connects to the right database!

---

## Three Scenarios, One File

### Scenario 1: Local Development (SQLite)
```env
DEPLOYMENT_MODE=local
DEBUG=True
SECRET_KEY=your-key
```
✅ Just works! No additional setup.

### Scenario 2: Docker Local (MySQL)
```env
DEPLOYMENT_MODE=docker
DEBUG=True
SECRET_KEY=your-key
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
MYSQL_DATABASE=image_gallery
```
✅ Run: `docker-compose up -d`

### Scenario 3: AWS Production (RDS + S3)
```env
DEPLOYMENT_MODE=aws
DEBUG=False
SECRET_KEY=your-key
RDS_ENDPOINT=mydb.xxx.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=rds-pass
RDS_DATABASE=image_gallery
S3_BUCKET_NAME=my-bucket
AWS_REGION=us-east-1
```
✅ Deploy to EC2 with: `gunicorn -w 4 -b 0.0.0.0:5000 run:app`

---

## Files Modified

### Updated Files
1. **`.env.example`** - Now unified template for all scenarios
   - Clear sections for each deployment mode
   - Configuration examples
   - Setup instructions

2. **`app/__init__.py`** - Smarter database detection
   - Checks `DEPLOYMENT_MODE` variable
   - Automatically routes to correct database
   - Added helpful log messages

3. **`docker-compose.yml`** - Now references unified `.env`
   - Clearer comments about mode selection
   - Works with `DEPLOYMENT_MODE=docker`

4. **`docker-compose.aws.yml`** - Now references unified `.env`
   - Changed from `.env.aws` to `.env`
   - Works with `DEPLOYMENT_MODE=aws`

### New Files
1. **`UNIFIED_ENV_GUIDE.md`** - Complete guide with:
   - Quick start (3 steps)
   - Detailed scenario explanations
   - Environment variable reference
   - Migration path
   - Troubleshooting
   - Pro tips

### Deprecated Files
1. **`.env.aws`** - Still exists but marked as deprecated
   - Points to use `.env.example` instead
   - Can be deleted if you want

---

## Quick Start

### 1. Copy Template
```bash
cp .env.example .env
```

### 2. Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Copy output to `SECRET_KEY` in `.env`

### 3. Choose Mode
Uncomment ONE of these in `.env`:
```bash
DEPLOYMENT_MODE=local      # for local development
# OR
DEPLOYMENT_MODE=docker     # for docker local dev
# OR
DEPLOYMENT_MODE=aws        # for AWS production
```

### 4. Configure for Your Mode
- **Local**: No additional setup needed
- **Docker**: Add `MYSQL_*` variables
- **AWS**: Add `RDS_*` and `S3_*` variables

### 5. Run
- **Local**: `python3 run.py`
- **Docker**: `docker-compose up -d`
- **AWS**: `gunicorn -w 4 -b 0.0.0.0:5000 run:app`

---

## Database Auto-Detection

The app automatically picks the right database:

```
DEPLOYMENT_MODE=local
    ↓
app/__init__.py checks DEPLOYMENT_MODE
    ↓
Detects "local" → No other DB config
    ↓
Uses SQLite: sqlite:///image_gallery.db ✅

---

DEPLOYMENT_MODE=docker
    ↓
app/__init__.py checks DEPLOYMENT_MODE
    ↓
Detects "docker" + MYSQL_USER exists
    ↓
Uses Docker MySQL: mysql+pymysql://user:pass@mysql:3306/db ✅

---

DEPLOYMENT_MODE=aws
    ↓
app/__init__.py checks DEPLOYMENT_MODE
    ↓
Detects "aws" + RDS_ENDPOINT exists
    ↓
Uses AWS RDS: mysql+pymysql://user:pass@endpoint:3306/db ✅
```

---

## Configuration Examples

### Example 1: Local Dev Only
```env
DEPLOYMENT_MODE=local
DEBUG=True
FLASK_ENV=development
SECRET_KEY=abc123def456...
```

### Example 2: Docker Team Dev
```env
DEPLOYMENT_MODE=docker
DEBUG=True
FLASK_ENV=development
SECRET_KEY=abc123def456...
MYSQL_ROOT_PASSWORD=Root@Pass123!
MYSQL_DATABASE=image_gallery
MYSQL_USER=gallery_user
MYSQL_PASSWORD=User@Pass123!
PMA_HOST=mysql
PMA_USER=gallery_user
PMA_PASSWORD=User@Pass123!
PMA_ROOT_PASSWORD=Root@Pass123!
```

### Example 3: AWS Production
```env
DEPLOYMENT_MODE=aws
DEBUG=False
FLASK_ENV=production
SECRET_KEY=abc123def456...
RDS_ENDPOINT=mydb.c9akciq32.us-east-1.rds.amazonaws.com
RDS_DATABASE=image_gallery
RDS_USER=admin
RDS_PASSWORD=Secure@RDS@Pass123!
RDS_PORT=3306
S3_BUCKET_NAME=image-gallery-production
AWS_REGION=us-east-1
```

---

## Migration Examples

### From Local to Docker
```bash
# Step 1: Update .env
# Change:
DEPLOYMENT_MODE=local

# To:
DEPLOYMENT_MODE=docker
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
MYSQL_DATABASE=image_gallery

# Step 2: Start Docker
docker-compose up -d

# Step 3: Done! ✅
```

### From Docker to AWS
```bash
# Step 1: Update .env
# Change:
DEPLOYMENT_MODE=docker
MYSQL_*=...

# To:
DEPLOYMENT_MODE=aws
RDS_ENDPOINT=mydb.xxx.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=...
S3_BUCKET_NAME=my-bucket

# Step 2: Deploy to EC2
scp .env ec2-user@instance:/app/
# Run gunicorn or docker on EC2

# Step 3: Done! ✅
```

---

## Important Notes

✅ **One file for all modes** - No more `.env.aws`, `.env.docker` confusion

✅ **Smart detection** - App figures out which database to use automatically

✅ **Never commit .env** - Already in `.gitignore`, but never remove it

✅ **Secure passwords** - 12+ characters for Docker, 16+ for AWS production

✅ **Easy migration** - Switch from local → docker → AWS just by changing one line

✅ **Full documentation** - See `UNIFIED_ENV_GUIDE.md` for comprehensive guide

---

## Troubleshooting

### "Can't connect to database"
- **Local**: Check `.env` has `DEPLOYMENT_MODE=local`
- **Docker**: Check `MYSQL_*` variables and `docker-compose up` ran
- **AWS**: Check `RDS_*` variables and security group allows EC2→RDS

### "App uses wrong database"
- Check `DEPLOYMENT_MODE` is set correctly
- App logs will show: 📁 SQLite, 🐳 Docker MySQL, or 🔵 AWS RDS

### "S3 upload fails"
- AWS only: EC2 must have IAM role with S3 permissions
- Check `S3_BUCKET_NAME` matches actual bucket

---

## See Also

- **`UNIFIED_ENV_GUIDE.md`** - Complete step-by-step guide
- **`.env.example`** - Template with all configuration options
- **`AWS_DEPLOYMENT_GUIDE.md`** - Full AWS setup instructions
- **`AWS_QUICK_REFERENCE.md`** - AWS commands and quick reference

---

## Summary

✨ **One unified `.env` file** handles all three deployment scenarios:
- Local Development (SQLite)
- Docker Local (MySQL)  
- AWS Production (RDS + S3)

Just change `DEPLOYMENT_MODE` and the app does the rest! 🚀

Happy deploying! 🎉
