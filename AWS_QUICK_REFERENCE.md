# AWS Quick Reference Card

## RDS MySQL Connection String

```
mysql+pymysql://admin:password@endpoint.rds.amazonaws.com:3306/image_gallery
```

## Environment Variables Needed for AWS

```env
# RDS Configuration
RDS_ENDPOINT=your-rds.region.rds.amazonaws.com
RDS_USER=admin
RDS_PASSWORD=your-secure-password
RDS_DATABASE=image_gallery
RDS_PORT=3306

# S3 Configuration  
S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1

# App Settings
SECRET_KEY=your-secret-key
DEBUG=False
FLASK_ENV=production
```

## AWS CLI Quick Commands

### RDS
```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier image-gallery-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password YourPassword

# Get RDS endpoint
aws rds describe-db-instances --db-instance-identifier image-gallery-db \
  --query 'DBInstances[0].Endpoint.Address' --output text

# Delete RDS instance
aws rds delete-db-instance \
  --db-instance-identifier image-gallery-db \
  --skip-final-snapshot
```

### S3
```bash
# Create bucket
aws s3 mb s3://image-gallery-bucket --region us-east-1

# List buckets
aws s3 ls

# Upload file
aws s3 cp image.jpg s3://image-gallery-bucket/

# Delete bucket (must be empty)
aws s3 rb s3://image-gallery-bucket
```

### EC2
```bash
# Launch instance with IAM role
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t2.micro \
  --iam-instance-profile Name=ImageGalleryAppProfile

# Get instances
aws ec2 describe-instances --query 'Reservations[0].Instances[0].[InstanceId,PublicIpAddress]'

# Terminate instance
aws ec2 terminate-instances --instance-ids i-xxxxx
```

### IAM
```bash
# Create role
aws iam create-role \
  --role-name ImageGalleryAppRole \
  --assume-role-policy-document file://trust-policy.json

# Attach S3 policy
aws iam put-role-policy \
  --role-name ImageGalleryAppRole \
  --policy-name S3Access \
  --policy-document file://s3-policy.json

# Create instance profile
aws iam create-instance-profile \
  --instance-profile-name ImageGalleryAppProfile

# Add role to profile
aws iam add-role-to-instance-profile \
  --instance-profile-name ImageGalleryAppProfile \
  --role-name ImageGalleryAppRole
```

## EC2 Setup Steps

```bash
# 1. SSH into instance
ssh -i key.pem ec2-user@instance-ip

# 2. Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git -y

# 3. Clone and setup
git clone https://github.com/your-repo/image_gallery.git
cd image_gallery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 4. Configure
cp .env.aws .env
nano .env  # Edit with RDS and S3 details

# 5. Test
python3 run.py
# Visit http://instance-ip:5000

# 6. Production (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Systemd Service Setup

```bash
# Create service file
sudo nano /etc/systemd/system/image-gallery.service

# Add this content:
[Unit]
Description=Image Gallery
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/image_gallery
EnvironmentFile=/home/ec2-user/image_gallery/.env
ExecStart=/home/ec2-user/image_gallery/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable image-gallery
sudo systemctl start image-gallery
```

## Nginx Setup

```bash
# Install
sudo yum install nginx -y

# Edit config
sudo nano /etc/nginx/conf.d/image-gallery.conf

# Add this:
server {
    listen 80;
    server_name _;
    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable and restart
sudo systemctl enable nginx
sudo systemctl restart nginx
```

## HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is automatic
```

## Testing & Troubleshooting

```bash
# Test RDS connection
mysql -h endpoint -u admin -p -e "SELECT 1"

# Test S3 access
aws s3 ls s3://bucket-name/

# Check application logs
sudo journalctl -u image-gallery -f

# Check app status
sudo systemctl status image-gallery

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor resources
htop
```

## Cost Estimation (Monthly)

| Service | Type | Cost |
|---------|------|------|
| EC2 | t2.micro | ~$9 (Free tier: $0) |
| RDS | t3.micro | ~$16 (Free tier: $0) |
| S3 | 10GB | ~$0.24 |
| Data Transfer | Out | ~$1-5 |
| **Total** | | **~$25-30** |

## Security Checklist

- [ ] RDS security group allows only EC2 access
- [ ] EC2 security group allows SSH only from your IP
- [ ] S3 bucket is NOT public
- [ ] IAM role attached to EC2 (no access keys!)
- [ ] HTTPS enabled with valid certificate
- [ ] Firewall rules in place
- [ ] Backups enabled
- [ ] Monitoring/CloudWatch alerts configured

## Important AWS Best Practices

1. **Never use AWS access keys** - Use IAM roles instead
2. **Enable MFA** on AWS account
3. **Use strong passwords** - 16+ chars, special characters
4. **Enable backup** for RDS (automatic is fine)
5. **Monitor costs** with CloudWatch budgets
6. **Use security groups** properly (principle of least privilege)
7. **Enable HTTPS** - Never use HTTP for production
8. **Rotate credentials** regularly if needed
9. **Enable CloudTrail** for audit logging
10. **Document everything** - Keep runbooks updated

## Useful Resources

- [AWS RDS Console](https://console.aws.amazon.com/rds/)
- [AWS S3 Console](https://console.aws.amazon.com/s3/)
- [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
- [AWS IAM Console](https://console.aws.amazon.com/iam/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Boto3 S3 Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

## Emergency Commands

```bash
# Restore from RDS snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier new-instance \
  --db-snapshot-identifier snapshot-id

# Stop RDS (cheaper than deleting, keeps data)
aws rds stop-db-instance --db-instance-identifier image-gallery-db

# Reboot RDS
aws rds reboot-db-instance --db-instance-identifier image-gallery-db

# Reboot EC2
aws ec2 reboot-instances --instance-ids i-xxxxx
```

## Notes

- RDS takes 5-10 minutes to create
- S3 bucket names must be globally unique
- IAM role changes take 1-2 minutes to propagate
- Always test migrations before production
- Keep .env file secure - never commit to git
- Use git-crypt or AWS Secrets Manager for sensitive data
