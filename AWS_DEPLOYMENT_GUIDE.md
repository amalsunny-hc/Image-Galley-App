# AWS Deployment Guide - Image Gallery

## Overview
This guide walks you through deploying the Image Gallery application to AWS with:
- **Database**: AWS RDS MySQL
- **Storage**: AWS S3
- **Compute**: EC2 or ECS/Elastic Beanstalk
- **Authentication**: IAM roles (no access keys needed!)

## Prerequisites

### AWS Services to Create
1. **RDS MySQL Database** (if not already created)
   - Engine: MySQL 8.0+
   - Instance class: db.t3.micro (free tier eligible)
   - Storage: 20GB gp2
   - Multi-AZ: No (for development), Yes (for production)
   - Database name: `image_gallery`

2. **S3 Bucket**
   - Bucket name: `your-app-bucket-name`
   - Region: Same as RDS for best performance
   - Block public access: Yes (use CloudFront if needed)
   - Versioning: Optional
   - Encryption: Enabled (default)

3. **EC2 Instance or ECS Cluster**
   - AMI: Amazon Linux 2 or Ubuntu
   - Python 3.10+
   - IAM role with S3 permissions

## Step-by-Step Deployment

### 1. Create RDS MySQL Database

```bash
# Using AWS CLI
aws rds create-db-instance \
  --db-instance-identifier image-gallery-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --region us-east-1
```

Or use AWS Console:
1. RDS Dashboard → Create Database
2. Choose MySQL 8.0
3. Set Master username: `admin`
4. Set strong Master password
5. Note the endpoint (e.g., `mydb.c9akciq32.us-east-1.rds.amazonaws.com`)

**Security Group Setup**:
- Allow inbound MySQL (3306) from your EC2 instance security group

### 2. Create S3 Bucket

```bash
# Using AWS CLI
aws s3 mb s3://image-gallery-app-bucket --region us-east-1
aws s3api put-bucket-versioning \
  --bucket image-gallery-app-bucket \
  --versioning-configuration Status=Enabled
```

Or use AWS Console:
1. S3 Dashboard → Create Bucket
2. Bucket name: `image-gallery-app-bucket`
3. Region: `us-east-1`
4. Block all public access: Yes

### 3. Create IAM Role for EC2

**Policy Document** (`s3-policy.json`):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::image-gallery-app-bucket",
                "arn:aws:s3:::image-gallery-app-bucket/*"
            ]
        }
    ]
}
```

```bash
# Create IAM role
aws iam create-role \
  --role-name ImageGalleryAppRole \
  --assume-role-policy-document file://trust-policy.json

# Attach policy
aws iam put-role-policy \
  --role-name ImageGalleryAppRole \
  --policy-name S3Access \
  --policy-document file://s3-policy.json

# Create instance profile
aws iam create-instance-profile \
  --instance-profile-name ImageGalleryAppProfile

aws iam add-role-to-instance-profile \
  --instance-profile-name ImageGalleryAppProfile \
  --role-name ImageGalleryAppRole
```

### 4. Launch EC2 Instance

```bash
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t2.micro \
  --key-name your-key-pair \
  --iam-instance-profile Name=ImageGalleryAppProfile \
  --security-groups default \
  --region us-east-1
```

Or use AWS Console:
1. EC2 Dashboard → Launch Instance
2. Select Amazon Linux 2 or Ubuntu
3. Instance type: t2.micro (free tier)
4. IAM instance profile: `ImageGalleryAppProfile`
5. Add security group rules for HTTP (80), HTTPS (443), SSH (22)

### 5. SSH into EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
# or for Ubuntu:
ssh -i your-key.pem ubuntu@your-instance-ip
```

### 6. Set Up Application on EC2

```bash
# Update system
sudo yum update -y  # Amazon Linux
# or: sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Python and dependencies
sudo yum install python3 python3-pip git -y  # Amazon Linux
# or: sudo apt install python3 python3-pip python3-venv git -y  # Ubuntu

# Clone repository
git clone https://github.com/your-repo/image_gallery.git
cd image_gallery

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # For production WSGI server

# Create .env file from .env.aws template
cp .env.aws .env

# Edit .env with your AWS credentials
nano .env
```

**Update these in .env**:
```env
# Your RDS endpoint from AWS Console
RDS_ENDPOINT=mydb.c9akciq32.us-east-1.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=YourSecurePassword123!
RDS_DATABASE=image_gallery

# Your S3 bucket name
S3_BUCKET_NAME=image-gallery-app-bucket
AWS_REGION=us-east-1

# Generate a new SECRET_KEY
SECRET_KEY=your-generated-secret-key-here

DEBUG=False
```

### 7. Test the Application

```bash
# With Flask development server (testing only)
python3 run.py

# Access at: http://your-instance-ip:5000
```

### 8. Production Deployment with Gunicorn

```bash
# Create systemd service file
sudo nano /etc/systemd/system/image-gallery.service
```

**Content**:
```ini
[Unit]
Description=Image Gallery Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/image_gallery
EnvironmentFile=/home/ec2-user/image_gallery/.env
ExecStart=/home/ec2-user/image_gallery/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable image-gallery
sudo systemctl start image-gallery
sudo systemctl status image-gallery
```

### 9. Set Up Nginx Reverse Proxy (Optional but Recommended)

```bash
sudo yum install nginx -y  # Amazon Linux
# or: sudo apt install nginx -y  # Ubuntu

sudo systemctl start nginx
sudo systemctl enable nginx
```

**Edit Nginx config** (`/etc/nginx/sites-available/image-gallery` or `/etc/nginx/conf.d/image-gallery.conf`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo systemctl restart nginx
```

### 10. Enable HTTPS with Let's Encrypt (Recommended)

```bash
sudo yum install certbot python3-certbot-nginx -y  # Amazon Linux
# or: sudo apt install certbot python3-certbot-nginx -y  # Ubuntu

sudo certbot --nginx -d your-domain.com
sudo systemctl restart nginx
```

### 11. Docker Deployment Alternative

```bash
# On EC2 instance with Docker installed
docker-compose -f docker-compose.aws.yml -f docker-compose.aws.yml up -d
docker logs -f image_gallery_app

# Or with image from Docker Hub
docker run -e RDS_ENDPOINT=... -e RDS_PASSWORD=... \
  -e S3_BUCKET_NAME=... -p 5000:5000 your-docker-image:latest
```

### 12. Monitoring and Logging

```bash
# View application logs
sudo journalctl -u image-gallery -f

# Or with Docker
docker logs -f image_gallery_app

# Monitor system resources
top
# or: htop (install with: sudo yum install htop -y)
```

## Troubleshooting

### RDS Connection Issues
```bash
# Test RDS connectivity from EC2
mysql -h mydb.c9akciq32.us-east-1.rds.amazonaws.com -u admin -p

# Check security group allows EC2 to RDS
# RDS Security Group → Inbound Rules → MySQL 3306 from EC2 SG
```

### S3 Upload Issues
```bash
# Check IAM role attached to EC2 instance
# Verify S3 bucket policy allows access from the role
# Test S3 access: aws s3 ls s3://image-gallery-app-bucket
```

### Application Won't Start
```bash
# Check logs
sudo journalctl -u image-gallery -n 50
docker logs image_gallery_app

# Check environment variables
echo $RDS_ENDPOINT
echo $S3_BUCKET_NAME

# Test database connection
python3
>>> import pymysql
>>> pymysql.connect(host='endpoint', user='admin', password='pass')
```

## Cost Estimation

For small deployments:
- **EC2 t2.micro**: ~$9/month (free tier 1 year)
- **RDS t3.micro**: ~$16/month (free tier 750 hours)
- **S3**: ~$0.023 per GB stored + transfer costs
- **Total**: ~$25-50/month for basic setup

## Next Steps

1. Configure CloudFront CDN for S3 images
2. Set up AWS CloudWatch monitoring
3. Configure auto-scaling
4. Set up CI/CD pipeline with GitHub Actions
5. Add database backups and snapshots
6. Implement AWS WAF for security

## References
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
