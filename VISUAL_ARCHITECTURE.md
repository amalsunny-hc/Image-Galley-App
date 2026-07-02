# Environment Configuration Architecture - Visual Guide

## One File. Three Scenarios.

```
                        ┌──────────────────┐
                        │   .env.example   │
                        │  (unified file)  │
                        └────────┬─────────┘
                                 │
                    Copy to .env  │
                                 ▼
                        ┌──────────────────┐
                        │    .env file     │
                        │ (your copy, live)│
                        └────────┬─────────┘
                                 │
                 ┌────────────────┼────────────────┐
                 │                │                │
        Set ONE of these:
                 │                │                │
     DEPLOYMENT_MODE=local
                 │         DEPLOYMENT_MODE=docker DEPLOYMENT_MODE=aws
                 │                │                │
                 ▼                ▼                ▼
          ╔═══════════╗    ╔═════════════╗   ╔═══════════════╗
          ║  LOCAL    ║    ║   DOCKER    ║   ║      AWS      ║
          ║    DEV    ║    ║     DEV     ║   ║  PRODUCTION   ║
          ╚═════┬═════╝    ╚──────┬──────╝   ╚────────┬──────╝
                │                │                    │
                │                │                    │
                ▼                ▼                    ▼
         ┌─────────────┐  ┌──────────────┐   ┌────────────────┐
         │  SQLite DB  │  │ MySQL Docker │   │  AWS RDS MySQL │
         │(file-based) │  │ (container)  │   │  (managed svc) │
         └─────┬───────┘  └──────┬───────┘   └────────┬───────┘
               │                │                    │
               │                │                    │
               ▼                ▼                    ▼
         ┌─────────────┐  ┌──────────────┐   ┌────────────────┐
         │ Local Disk  │  │ Volume (local)           │     AWS S3 Bucket  │
         │            │  │            │   │ (managed svc) │
         │ Upload Dir  │  │ MySQL Data │   │               │
         └─────┬───────┘  └──────┬───────┘   │ Image Storage  │
               │                │            └────────┬───────┘
               │                │                     │
               └────────┬────────┴─────────┬──────────┘
                        │                 │
                        │   All use same  │
                        │  Flask app code │
                        │                 │
                        └────────┬────────┘
                                 │
                        ┌────────▼──────────┐
                        │   app/__init__.py │
                        │  (detects mode &  │
                        │ picks database)   │
                        └───────────────────┘
```

---

## Decision Tree

```
START HERE
    │
    └─ Copy .env.example to .env
         │
         ├─ Generate SECRET_KEY
         │   └─ python3 -c "import secrets; print(secrets.token_hex(32))"
         │
         └─ Choose DEPLOYMENT_MODE:
              │
              ├─ DEPLOYMENT_MODE=local
              │  │
              │  ├─ No additional setup
              │  ├─ Run: python3 run.py
              │  └─ Database: SQLite (image_gallery.db)
              │
              ├─ DEPLOYMENT_MODE=docker
              │  │
              │  ├─ Add MYSQL_* variables to .env
              │  │   ├─ MYSQL_ROOT_PASSWORD
              │  │   ├─ MYSQL_USER
              │  │   └─ MYSQL_PASSWORD
              │  ├─ Run: docker-compose up -d
              │  └─ Database: MySQL in Docker
              │
              └─ DEPLOYMENT_MODE=aws
                 │
                 ├─ Create AWS RDS instance
                 ├─ Create AWS S3 bucket
                 ├─ Launch EC2 with IAM role
                 ├─ Add RDS_* and S3_* variables
                 │   ├─ RDS_ENDPOINT
                 │   ├─ RDS_USER
                 │   ├─ RDS_PASSWORD
                 │   ├─ S3_BUCKET_NAME
                 │   └─ AWS_REGION
                 ├─ Run: gunicorn ... or docker-compose
                 └─ Database: AWS RDS, Storage: AWS S3
```

---

## File Dependencies

```
app/__init__.py
    │
    └─ reads from .env:
         │
         ├─ DEPLOYMENT_MODE (mandatory)
         │   │
         │   ├─ "local"   → uses SQLite
         │   ├─ "docker"  → looks for MYSQL_*
         │   └─ "aws"     → looks for RDS_*
         │
         ├─ RDS_* variables (if DEPLOYMENT_MODE=aws)
         │   ├─ RDS_ENDPOINT
         │   ├─ RDS_USER
         │   ├─ RDS_PASSWORD
         │   ├─ RDS_DATABASE
         │   └─ RDS_PORT
         │
         ├─ MYSQL_* variables (if DEPLOYMENT_MODE=docker)
         │   ├─ MYSQL_USER
         │   ├─ MYSQL_PASSWORD
         │   └─ MYSQL_DATABASE
         │
         └─ S3_* variables (if DEPLOYMENT_MODE=aws and DEBUG=False)
             ├─ S3_BUCKET_NAME
             └─ AWS_REGION
```

---

## Database Connection Logic

```
app/__init__.py startup
    │
    ├─ Read DEPLOYMENT_MODE from .env
    │
    ├─ if DEPLOYMENT_MODE == "aws" AND RDS_ENDPOINT exists:
    │   │
    │   ├─ Build connection string:
    │   │  mysql+pymysql://[RDS_USER]:[RDS_PASSWORD]@[RDS_ENDPOINT]:[RDS_PORT]/[RDS_DATABASE]
    │   │
    │   ├─ Log: "🔵 Connected to AWS RDS MySQL"
    │   │
    │   └─ Use AWS RDS
    │
    ├─ elif DEPLOYMENT_MODE == "docker" AND MYSQL_USER exists:
    │   │
    │   ├─ Build connection string:
    │   │  mysql+pymysql://[MYSQL_USER]:[MYSQL_PASSWORD]@mysql:3306/[MYSQL_DATABASE]
    │   │
    │   ├─ Log: "🐳 Connected to Docker MySQL"
    │   │
    │   └─ Use Docker MySQL
    │
    └─ else:
        │
        ├─ Build connection string:
        │  sqlite:///image_gallery.db
        │
        ├─ Log: "📁 Using SQLite local database"
        │
        └─ Use SQLite (default)
```

---

## Configuration File Content Map

```
.env.example layout:
│
├─ Header (what this file is)
│
├─ SECTION 1: Choose Your Scenario
│  ├─ DEPLOYMENT_MODE=local     (option 1)
│  ├─ DEPLOYMENT_MODE=docker    (option 2)
│  └─ DEPLOYMENT_MODE=aws       (option 3)
│
├─ SECTION 2: Application Settings
│  ├─ FLASK_APP, FLASK_ENV, etc
│  └─ DEBUG, SECRET_KEY, etc
│
├─ SECTION 3: Scenario 1 (Local)
│  └─ (no additional variables needed)
│
├─ SECTION 4: Scenario 2 (Docker)
│  ├─ MYSQL_ROOT_PASSWORD
│  ├─ MYSQL_DATABASE
│  ├─ MYSQL_USER
│  ├─ MYSQL_PASSWORD
│  ├─ PMA_HOST
│  ├─ PMA_USER
│  ├─ PMA_PASSWORD
│  └─ PMA_ROOT_PASSWORD
│
└─ SECTION 5: Scenario 3 (AWS)
   ├─ RDS_ENDPOINT
   ├─ RDS_DATABASE
   ├─ RDS_USER
   ├─ RDS_PASSWORD
   ├─ RDS_PORT
   ├─ S3_BUCKET_NAME
   └─ AWS_REGION
```

---

## Docker Compose File Selection

```
Choose which to run:

LOCAL DOCKER TESTING:
    docker-compose up -d
    └─ Uses: docker-compose.yml
       └─ Contains: MySQL + Flask
       └─ Reads: .env (DEPLOYMENT_MODE=docker)

AWS DOCKER DEPLOYMENT:
    docker-compose -f docker-compose.aws.yml up -d
    └─ Uses: docker-compose.aws.yml
       └─ Contains: Flask only
       └─ Reads: .env (DEPLOYMENT_MODE=aws)
       └─ Connects to: AWS RDS (external)
```

---

## Migration Flow

```
START: Local SQLite
│
│ Add MYSQL_* to .env
│ Change: DEPLOYMENT_MODE=local → docker
│ Run: docker-compose up -d
│
▼
MIGRATE TO: Docker MySQL
│
│ Replace MYSQL_* with RDS_* and S3_*
│ Change: DEPLOYMENT_MODE=docker → aws
│ Deploy: Push .env to EC2
│ Run: gunicorn ... run:app
│
▼
DEPLOY TO: AWS RDS + S3
│
│ Running on production! 🚀
│
▼
END: Production Ready
```

---

## Configuration Scope

```
Global (All scenarios)
├─ FLASK_APP
├─ FLASK_ENV
├─ FLASK_PORT
├─ SECRET_KEY          ✓ REQUIRED
├─ DEBUG
├─ MAX_FILE_SIZE
├─ ALLOWED_EXTENSIONS
├─ UPLOAD_FOLDER
└─ DEPLOYMENT_MODE    ✓ REQUIRED

Scenario: Local (SQLite)
└─ (no additional variables)

Scenario: Docker (MySQL)
├─ MYSQL_ROOT_PASSWORD    ✓ REQUIRED for docker
├─ MYSQL_DATABASE         ✓ REQUIRED for docker
├─ MYSQL_USER             ✓ REQUIRED for docker
├─ MYSQL_PASSWORD         ✓ REQUIRED for docker
├─ PMA_HOST
├─ PMA_USER
├─ PMA_PASSWORD
└─ PMA_ROOT_PASSWORD

Scenario: AWS (RDS + S3)
├─ RDS_ENDPOINT           ✓ REQUIRED for aws
├─ RDS_DATABASE           ✓ REQUIRED for aws
├─ RDS_USER               ✓ REQUIRED for aws
├─ RDS_PASSWORD           ✓ REQUIRED for aws
├─ RDS_PORT
├─ S3_BUCKET_NAME         ✓ REQUIRED for aws
└─ AWS_REGION
```

---

## Validation Checklist at Startup

```
When app starts:

1. Check DEPLOYMENT_MODE
   └─ Is it local, docker, or aws?

2. If DEPLOYMENT_MODE == "aws":
   ├─ Check RDS_ENDPOINT exists
   ├─ Check RDS_USER exists
   ├─ Check RDS_PASSWORD exists
   └─ Build RDS connection string

3. Elif DEPLOYMENT_MODE == "docker":
   ├─ Check MYSQL_USER exists
   ├─ Check MYSQL_PASSWORD exists
   └─ Build Docker MySQL connection string

4. Else (default "local"):
   └─ Use SQLite: sqlite:///image_gallery.db

5. Connect to database
   └─ Create tables if needed

6. Log result
   ├─ 📁 SQLite
   ├─ 🐳 Docker MySQL
   └─ 🔵 AWS RDS
```

---

## Network Diagram

```
LOCAL SCENARIO:
┌──────────────────────────────────┐
│  Your Computer                    │
│                                   │
│  ┌──────────────────────────┐    │
│  │  app/__init__.py         │    │
│  │  (Python/Flask)          │    │
│  └───────────┬──────────────┘    │
│              │ reads .env        │
│              │ DEPLOYMENT_MODE   │
│              ▼                    │
│  ┌──────────────────────────┐    │
│  │  image_gallery.db        │    │
│  │  (SQLite - local file)   │    │
│  └──────────────────────────┘    │
│                                   │
└──────────────────────────────────┘

DOCKER SCENARIO:
┌──────────────────────────────────────┐
│  Your Computer (Docker Host)          │
│                                        │
│  ┌────────────────┐  ┌──────────────┐│
│  │ Flask Container│  │ MySQL Docker ││
│  │ :5000          │  │ :3306        ││
│  │                │  │              ││
│  │ app/__init__.py│─→│ image_gallery││
│  └────────────────┘  │    database  ││
│                      └──────────────┘│
│                                        │
└──────────────────────────────────────┘

AWS SCENARIO:
┌──────────────────────────────────────────────────┐
│  EC2 Instance (AWS)                              │
│                                                   │
│  ┌────────────────┐  IAM Role (S3 access)       │
│  │ Flask App      │──────┬─────────────┐         │
│  │ :5000          │      │             │         │
│  │                │      │             │         │
│  │ app/__init__.py│      │             │         │
│  └────────┬───────┘      │             │         │
│           │              │             │         │
│           │              ▼             ▼         │
│           └─────────────────────────────────────→│
│                                                   │
└──────────┬─────────────────────────────────────┬─┘
           │                                     │
           │ DEPLOYMENT_MODE=aws                │
           │ RDS_ENDPOINT                       │ AWS_REGION
           │                                     │
           ▼                                     ▼
    ┌─────────────────┐            ┌──────────────────┐
    │  AWS RDS MySQL  │            │   AWS S3 Bucket  │
    │                 │            │                  │
    │  Database       │            │  Image Storage   │
    └─────────────────┘            └──────────────────┘
```

---

## Summary

```
KEY INSIGHT:

    One .env file
         ↓
    Set DEPLOYMENT_MODE
         ↓
    App auto-detects
         ↓
    Connects to correct database
         ↓
    Your code doesn't change!


BENEFIT:

    Local  → add MYSQL_*  → Docker  → replace with RDS_* → AWS
    (1 min)   (5-10 min)  (setup)   (20-30 min setup)   (prod)

    All with same .env format!
```

---

## File Reference

| File | Purpose | Editable |
|------|---------|----------|
| `.env.example` | Template (never edit in use) | No |
| `.env` | Your config (edit for each deployment) | Yes |
| `app/__init__.py` | Detects mode automatically | No |
| `docker-compose.yml` | Local Docker setup | No |
| `docker-compose.aws.yml` | AWS Docker setup | No |

---

Everything is interconnected through the `.env` file and `DEPLOYMENT_MODE` variable!
