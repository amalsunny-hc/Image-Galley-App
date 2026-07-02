# Quick Start - Unified .env File

## Your Single Configuration File

📁 **`.env`** ← Use this ONE file for all scenarios

## 3 Steps to Deploy

### Step 1️⃣: Open `.env` and Choose Mode
```env
DEPLOYMENT_MODE=local    # ← uncomment one
# DEPLOYMENT_MODE=docker
# DEPLOYMENT_MODE=aws
```

### Step 2️⃣: Configure Your Mode

**Local? You're done!** Just set `DEPLOYMENT_MODE=local`

**Docker?** Uncomment and set:
```env
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
MYSQL_DATABASE=image_gallery
```

**AWS?** Uncomment and set:
```env
RDS_ENDPOINT=mydb.c9akciq32.us-east-1.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=secure-password
S3_BUCKET_NAME=my-bucket
```

### Step 3️⃣: Run
```bash
python3 run.py               # local
# docker-compose up -d       # docker
# gunicorn ... run:app      # aws
```

---

## Inside `.env` File

| Section | Purpose |
|---------|---------|
| **STEP 1** | Choose: local, docker, or aws |
| **APPLICATION SETTINGS** | Common variables (all modes) |
| **SCENARIO 1** | Local development section |
| **SCENARIO 2** | Docker section with MySQL vars |
| **SCENARIO 3** | AWS section with RDS & S3 vars |
| **EXAMPLES** | Real config examples for each mode |
| **HOW IT WORKS** | Explains app auto-detection |
| **GUIDES** | Password requirements, migration, security |

---

## What's in the File

```
.env (ONE unified file)
├── Header: What the file is
├── Section 1: Choose DEPLOYMENT_MODE
├── Section 2: Common settings (FLASK_APP, SECRET_KEY, etc)
├── Section 3: LOCAL example (commented)
├── Section 4: DOCKER example (with MYSQL_* variables)
├── Section 5: AWS example (with RDS_* and S3_* variables)
├── Section 6: Real-world examples
├── Section 7: How app auto-detects
├── Section 8: Setup guide
├── Section 9: Password requirements
├── Section 10: Security notes
└── Section 11: Migration path
```

---

## Local Development

```env
DEPLOYMENT_MODE=local
DEBUG=True
SECRET_KEY=any-key
# Done! SQLite created automatically
```

Run: `python3 run.py`

---

## Docker Development

```env
DEPLOYMENT_MODE=docker
DEBUG=True
SECRET_KEY=your-generated-key
MYSQL_ROOT_PASSWORD=root123
MYSQL_USER=gallery_user
MYSQL_PASSWORD=user123
MYSQL_DATABASE=image_gallery
PMA_HOST=mysql
PMA_USER=gallery_user
PMA_PASSWORD=user123
PMA_ROOT_PASSWORD=root123
```

Run: `docker-compose up -d`

---

## AWS Production

```env
DEPLOYMENT_MODE=aws
DEBUG=False
SECRET_KEY=your-generated-key
RDS_ENDPOINT=mydb.xxx.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=Secure@Pass123!
RDS_DATABASE=image_gallery
S3_BUCKET_NAME=my-bucket
AWS_REGION=us-east-1
```

Run: `gunicorn -w 4 -b 0.0.0.0:5000 run:app`

---

## Key Features

✅ **ONE file** - No `.env.example` vs `.env` confusion  
✅ **Self-documenting** - Every variable explained in comments  
✅ **Examples included** - See real configs for all modes  
✅ **Easy migration** - Change one line to switch modes  
✅ **App auto-detects** - No code changes needed  

---

## Generate Secret Key

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste into `SECRET_KEY=` in `.env`

---

## Check Your Mode

When you run the app, logs show which mode:

```
📁 Using SQLite local database        # local
🐳 Connected to Docker MySQL          # docker
🔵 Connected to AWS RDS MySQL         # aws
```

---

## Password Tips

**Local:** Any password or empty  
**Docker:** 12+ chars (MyPass123!)  
**AWS:** 16+ chars with special chars (D$9K#xL2!)  

---

## That's It!

Edit `.env` → Choose mode → Run app 🚀

All configurations in ONE place!
