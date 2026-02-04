# AWS S3 Integration Setup Guide

## Overview

This Image Gallery application now supports AWS S3 for storing images. The integration uses **IAM role-based authentication**, meaning you don't need to store AWS access keys in your `.env` file - the application automatically uses credentials from the IAM role attached to your EC2 instance (or local AWS credentials file).

## Table of Contents

1. [Quick Start (EC2 with IAM Role)](#quick-start-ec2-with-iam-role)
2. [Local Development Setup](#local-development-setup)
3. [AWS IAM Policy](#aws-iam-policy)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start (EC2 with IAM Role)

### Step 1: Create S3 Bucket

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com)
2. Click **Create bucket**
3. **Bucket name**: `image-gallery-prod` (or your preferred name)
4. **Region**: Select your preferred region (e.g., `us-east-1`)
5. **Block Public Access settings**: Keep defaults (block all public access)
6. Click **Create bucket**

### Step 2: Create IAM Role for EC2

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Roles** → **Create role**
3. **Trusted entity type**: Select **AWS service**
4. **Service**: Select **EC2**
5. Click **Next**

### Step 3: Attach S3 Policy

You have two options:

#### Option A: Use Managed Policy (Simpler)
- Search for and select **AmazonS3FullAccess**
- Click **Next** and **Create role**

#### Option B: Create Custom Policy (Recommended)

1. Click **Create policy** in a new tab
2. Go to **JSON** tab
3. Paste the following policy (replacing `image-gallery-prod` with your bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3BucketAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::image-gallery-prod",
                "arn:aws:s3:::image-gallery-prod/*"
            ]
        }
    ]
}
```

4. Click **Next** → **Create policy**
5. Go back to role creation and attach this policy
6. Click **Create role**

### Step 4: Attach Role to EC2 Instance

1. Go to [EC2 Console](https://console.aws.amazon.com/ec2/)
2. Select your instance
3. Click **Instance state** → **Instance settings** → **Modify IAM instance profile**
4. Select the IAM role you created
5. Click **Update IAM instance profile**

### Step 5: Update Application Configuration

SSH into your EC2 instance and update `.env`:

```bash
cd /app
nano .env
```

Add/update these variables:

```env
S3_BUCKET_NAME=image-gallery-prod
AWS_REGION=us-east-1
```

No AWS access keys needed! The role credentials are automatically used.

### Step 6: Restart Application

```bash
# If using Docker
docker-compose restart

# If running locally
python3 run.py
```

---

## Local Development Setup

### Using AWS CLI Credentials

1. **Install AWS CLI**:
   ```bash
   pip install awscli
   ```

2. **Configure AWS credentials**:
   ```bash
   aws configure
   ```
   
   Enter your AWS credentials when prompted:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., us-east-1)

3. **Update `.env`**:
   ```env
   S3_BUCKET_NAME=your-test-bucket
   AWS_REGION=us-east-1
   ```

4. **Start application**:
   ```bash
   python3 run.py
   ```

The boto3 library will automatically pick up credentials from:
1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. `~/.aws/credentials` file
3. IAM role (if running on EC2)

### Using Environment Variables

Alternatively, set AWS credentials directly:

```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_REGION=us-east-1
```

Then set in `.env`:
```env
S3_BUCKET_NAME=your-test-bucket
AWS_REGION=us-east-1
```

---

## AWS IAM Policy

### Minimal Policy (Production Recommended)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListBucket",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::image-gallery-prod"
        },
        {
            "Sid": "GetPutDeleteObjects",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::image-gallery-prod/*"
        }
    ]
}
```

### Policy Explanation

- **ListBucket**: Allows listing objects (for debugging)
- **GetObject**: Read images for viewing
- **PutObject**: Upload new images
- **DeleteObject**: Delete images

---

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `S3_BUCKET_NAME` | S3 bucket name | `image-gallery-prod` |
| `AWS_REGION` | AWS region | `us-east-1` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| (None needed) | Credentials auto-detected | - |

### Application Configuration

The application automatically:
- Validates S3 bucket access on startup
- Generates signed URLs (valid for 1 hour)
- Optimizes images before uploading (max 2000x2000, quality 85)
- Encrypts objects using AES256

---

## Deployment

### On EC2 with Docker

1. **Pull/clone repository**
2. **Create `.env` file**:
   ```env
   S3_BUCKET_NAME=image-gallery-prod
   AWS_REGION=us-east-1
   FLASK_ENV=production
   SECRET_KEY=your-very-secure-key-here
   MYSQL_ROOT_PASSWORD=secure-password
   MYSQL_USER=gallery_user
   MYSQL_PASSWORD=secure-password
   ```

3. **Ensure IAM role is attached** to EC2 instance

4. **Start services**:
   ```bash
   docker-compose up -d
   ```

5. **Verify S3 connection**:
   ```bash
   docker-compose logs flask_app | grep -i "s3\|bucket"
   ```

### On EC2 with Local Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure IAM role is attached** to EC2 instance

3. **Configure `.env` with S3 settings**

4. **Run application**:
   ```bash
   python3 run.py
   ```

---

## Image Storage Structure

Images are stored in your S3 bucket with this structure:

```
s3://image-gallery-prod/
├── images/
│   ├── 2026/
│   │   ├── 02/
│   │   │   ├── 15/
│   │   │   │   ├── 20260215_143022_photo.jpg
│   │   │   │   ├── 20260215_150515_sunset.png
│   │   │   │   └── ...
```

Organization by year/month/day makes it easy to:
- Understand storage organization
- Implement retention policies
- Debug upload issues

---

## API Reference

### Uploading Images

The upload process automatically:
1. Validates file type (jpg, jpeg, png, gif, webp)
2. Resizes if larger than 2000x2000px
3. Compresses to quality 85
4. Uploads to S3 with encryption
5. Stores S3 key in database

### Accessing Images

Images are accessed via **signed URLs**:
- Valid for **1 hour** by default
- Automatically generated when viewing
- No direct S3 access needed

To change expiration time, edit `app/utils/s3.py`:
```python
def get_signed_url(s3_key, expiration=3600):  # Change 3600 (seconds)
```

### Deleting Images

When an image is deleted:
1. Image is removed from S3
2. Database record is deleted
3. Cascading deletes work for user deletion

---

## Troubleshooting

### Error: "Cannot access S3 bucket"

**Cause**: IAM role doesn't have S3 permissions

**Solution**:
1. Verify IAM role is attached to EC2 instance
2. Check IAM policy allows `s3:ListBucket` on bucket name
3. Check IAM policy allows `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject` on bucket/* 
4. Wait 1-2 minutes for IAM policy changes to propagate

### Error: "NoCredentialsError"

**Cause**: AWS credentials not found

**Local development**:
```bash
aws configure
```

**EC2**:
- Verify IAM role is attached
- Try: `aws sts get-caller-identity` to test

### Images Not Uploading

**Check**:
1. Verify bucket name in `.env`
2. Verify AWS region matches bucket region
3. Check application logs: `docker-compose logs flask_app`
4. Ensure IAM policy includes `s3:PutObject`

### Signed URLs Not Working

**Common issues**:
1. URL expired (generate a new one - they're valid 1 hour)
2. Bucket not accessible from user's network (unlikely unless private)
3. Image was deleted from S3

**Solution**: Images auto-generate new signed URLs on each page load

### Check S3 Bucket Access

From your EC2 instance:

```bash
# List objects in bucket
aws s3 ls s3://image-gallery-prod/

# Upload test file
echo "test" > test.txt
aws s3 cp test.txt s3://image-gallery-prod/test.txt

# Delete test file
aws s3 rm s3://image-gallery-prod/test.txt
```

---

## Security Best Practices

1. **Use IAM Roles** (not access keys) ✅
2. **Enable S3 encryption** (AES256) ✅ Enabled by default
3. **Block public access** ✅ Images accessed via signed URLs
4. **Use HTTPS** - Enable in production
5. **Set bucket lifecycle policies** - Delete old images after 90 days (optional)
6. **Enable S3 versioning** - For backup (optional)
7. **Use CloudFront** - For better performance (optional)

### Optional: Enable S3 Versioning

```bash
aws s3api put-bucket-versioning \
  --bucket image-gallery-prod \
  --versioning-configuration Status=Enabled
```

### Optional: Set Lifecycle Policy

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket image-gallery-prod \
  --lifecycle-configuration file://lifecycle.json
```

Example `lifecycle.json`:
```json
{
  "Rules": [
    {
      "Id": "DeleteOldImages",
      "Status": "Enabled",
      "Prefix": "images/",
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

---

## Cost Optimization

### Typical Costs

For 1000 images (average 2MB each):

- **S3 Storage**: ~$0.023/month
- **PUT requests**: ~$0.005
- **GET requests**: Minimal (free tier includes 1M requests)

### Reducing Costs

1. **Use S3 Intelligent-Tiering** - Automatically moves to cheaper tiers
2. **Enable CloudFront** - Cheaper for frequent reads
3. **Use S3 Glacier** - For archived images
4. **Set lifecycle policies** - Delete old images automatically

---

## Migration from Local Storage

To migrate existing images from local filesystem to S3:

1. **Keep database as-is** - Image records already exist
2. **Copy images to S3** manually:
   ```bash
   aws s3 sync ./app/static/uploads/ s3://image-gallery-prod/images/
   ```
3. **Update database** - Add S3 keys to existing image records

You'll need a migration script - contact support if needed.

---

## Support & Debugging

### Enable Debug Logging

In `app/__init__.py`, change:
```python
if not check_s3_bucket_access(s3_bucket):
    app.logger.warning(...)  # Change to ERROR for visibility
```

### View Application Logs

```bash
# Docker
docker-compose logs -f flask_app

# Local
tail -f debug.log
```

### Test S3 Connection

```bash
# SSH into EC2/container
aws sts get-caller-identity
aws s3 ls s3://image-gallery-prod/
```

---

## FAQ

**Q: Do I need AWS keys in my code?**
A: No! IAM roles handle authentication automatically.

**Q: Can I use S3 public URLs instead of signed URLs?**
A: Yes, but less secure. Update templates to use `s3://bucket/key` URLs instead.

**Q: How long are signed URLs valid?**
A: 1 hour by default. Change in `app/utils/s3.py`.

**Q: What happens if S3 goes down?**
A: Users won't be able to upload/view images. Application will log errors but continue running.

**Q: Can I use this without an IAM role?**
A: Yes - set environment variables or use AWS CLI credentials file locally.

---

## Version History

- **v2.0** - Added S3 IAM role support (current)
- **v1.0** - Local filesystem storage

---

For more information, see:
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
