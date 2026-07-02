# AWS Deployment Checklist

## Pre-Deployment Setup

### AWS Account & Permissions
- [ ] AWS account created
- [ ] IAM user with AdministratorAccess or necessary permissions
- [ ] AWS CLI installed and configured: `aws configure`
- [ ] Valid AWS credentials set up

### AWS Services Configuration

#### RDS MySQL Setup
- [ ] RDS instance created with MySQL 8.0+
- [ ] Instance endpoint noted (e.g., `mydb.c9akciq32.us-east-1.rds.amazonaws.com`)
- [ ] Master username created (recommended: `admin`)
- [ ] Strong master password set
- [ ] Database name created: `image_gallery`
- [ ] Multi-AZ disabled for development (or enabled for production)
- [ ] Automatic backups enabled
- [ ] Backup retention set (7 days recommended)
- [ ] Security group allows inbound MySQL 3306 from EC2

#### S3 Bucket Setup
- [ ] S3 bucket created with descriptive name
- [ ] Bucket region same as RDS (for performance)
- [ ] Block public access enabled
- [ ] Versioning enabled
- [ ] Server-side encryption enabled
- [ ] Bucket policy configured if needed

#### EC2 Instance Setup
- [ ] Security group created with rules:
  - [ ] SSH (22) from your IP
  - [ ] HTTP (80) from anywhere
  - [ ] HTTPS (443) from anywhere
  - [ ] MySQL (3306) from RDS security group (for testing only)
- [ ] Key pair created and securely stored
- [ ] IAM role created with S3 permissions
- [ ] Instance profile attached to role
- [ ] EC2 instance launched with role attached
- [ ] Instance is in running state
- [ ] Elastic IP assigned (optional but recommended)

### Local Machine Setup
- [ ] Python 3.10+ installed
- [ ] Git installed
- [ ] SSH client available
- [ ] Key pair file has correct permissions (chmod 400 key.pem)
- [ ] AWS CLI configured
- [ ] Docker installed (optional, for Docker deployments)

## Deployment Steps

### Application Setup
- [ ] Repository cloned to EC2 instance
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Gunicorn installed: `pip install gunicorn`
- [ ] `.env.aws` copied to `.env`

### Environment Configuration
- [ ] `.env` file created with all RDS variables:
  - [ ] `RDS_ENDPOINT=your-endpoint.rds.amazonaws.com`
  - [ ] `RDS_USER=admin`
  - [ ] `RDS_PASSWORD=your-secure-password`
  - [ ] `RDS_DATABASE=image_gallery`
  - [ ] `RDS_PORT=3306`
- [ ] S3 bucket name configured:
  - [ ] `S3_BUCKET_NAME=your-bucket-name`
  - [ ] `AWS_REGION=us-east-1`
- [ ] Application settings configured:
  - [ ] `SECRET_KEY=generated-secret-key`
  - [ ] `DEBUG=False`
  - [ ] `FLASK_ENV=production`

### Testing & Validation
- [ ] RDS connectivity tested: `mysql -h endpoint -u admin -p`
- [ ] Database initialization script run
- [ ] Application started with Flask dev server: `python3 run.py`
- [ ] App accessible at `http://instance-ip:5000`
- [ ] Database tables created successfully
- [ ] S3 access verified with test upload
- [ ] All application features tested

### Production Deployment
- [ ] Systemd service file created: `/etc/systemd/system/image-gallery.service`
- [ ] Service enabled: `sudo systemctl enable image-gallery`
- [ ] Service started: `sudo systemctl start image-gallery`
- [ ] Service status verified: `sudo systemctl status image-gallery`
- [ ] Nginx installed and configured
- [ ] Nginx configuration updated with proxy settings
- [ ] Nginx restarted and enabled
- [ ] Application accessible via HTTP

### Security & HTTPS
- [ ] Domain name configured (if using custom domain)
- [ ] Certbot installed
- [ ] SSL certificate obtained: `sudo certbot --nginx -d domain.com`
- [ ] HTTPS redirect configured
- [ ] SSL certificate auto-renewal enabled
- [ ] Application accessible via HTTPS

### Monitoring & Maintenance
- [ ] CloudWatch monitoring enabled
- [ ] Application logs accessible: `sudo journalctl -u image-gallery`
- [ ] RDS backup schedule verified
- [ ] S3 bucket versioning confirmed
- [ ] CloudWatch alarms set up (optional)

## Verification Commands

```bash
# Check RDS connection
aws rds describe-db-instances --db-instance-identifier image-gallery-db

# Check S3 bucket
aws s3 ls s3://your-bucket-name

# Check EC2 instance
aws ec2 describe-instances --instance-ids i-xxxxx

# Check IAM role
aws iam get-role --role-name ImageGalleryAppRole

# Test connectivity from EC2
mysql -h RDS_ENDPOINT -u admin -p image_gallery

# Test S3 access
aws s3 ls s3://your-bucket-name
aws s3 cp test.txt s3://your-bucket-name/test.txt

# Check application logs
sudo journalctl -u image-gallery -n 100
tail -f /var/log/image-gallery.log
```

## Troubleshooting

### If RDS Connection Fails
- [ ] Verify RDS endpoint is correct
- [ ] Check RDS password is correct
- [ ] Verify RDS security group allows access from EC2
- [ ] Ensure RDS instance is running
- [ ] Check .env file has correct RDS_* variables

### If S3 Upload Fails
- [ ] Verify IAM role has S3 permissions
- [ ] Check S3 bucket name is correct
- [ ] Verify bucket exists in correct region
- [ ] Check IAM instance profile is attached to EC2
- [ ] Test with: `aws s3 cp file.txt s3://bucket-name/`

### If Application Won't Start
- [ ] Check application logs: `sudo journalctl -u image-gallery`
- [ ] Verify all environment variables are set
- [ ] Test database connection manually
- [ ] Check Gunicorn is installed
- [ ] Verify Python virtual environment is activated

### If Cannot SSH to EC2
- [ ] Verify key pair permissions: `chmod 400 key.pem`
- [ ] Check security group SSH rule (port 22)
- [ ] Verify public IP is correct
- [ ] Check your IP is allowed in security group

## Cleanup (If Needed)

```bash
# To remove AWS resources
aws rds delete-db-instance --db-instance-identifier image-gallery-db --skip-final-snapshot
aws s3 rm s3://your-bucket-name --recursive
aws s3 rb s3://your-bucket-name
aws ec2 terminate-instances --instance-ids i-xxxxx
aws iam delete-instance-profile --instance-profile-name ImageGalleryAppProfile
aws iam delete-role-policy --role-name ImageGalleryAppRole --policy-name S3Access
aws iam delete-role --role-name ImageGalleryAppRole
```

## Cost Monitoring

- [ ] CloudWatch billing alerts set up
- [ ] AWS Budgets configured
- [ ] Regular cost review scheduled
- [ ] Resources right-sized for workload

## Documentation

- [ ] AWS setup documented
- [ ] Custom configuration documented
- [ ] Deployment process documented
- [ ] Backup and recovery procedures documented
- [ ] Team access and permissions documented

## Post-Deployment

- [ ] Team members trained on deployment process
- [ ] Documentation shared with team
- [ ] Monitoring and alerting configured
- [ ] Backup and disaster recovery tested
- [ ] Performance baseline established
