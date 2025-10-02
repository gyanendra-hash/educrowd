# 🚀 EduCrowd Deployment Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Local Development](#local-development)
4. [Staging Deployment](#staging-deployment)
5. [Production Deployment](#production-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Database Setup](#database-setup)
8. [SSL Configuration](#ssl-configuration)
9. [Monitoring & Logging](#monitoring--logging)
10. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 20GB free space
- **CPU**: 2+ cores recommended

### Software Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.8+ (for local development)
- **Node.js**: 16+ (for frontend builds)
- **Git**: Latest version

### External Services

- **PostgreSQL**: 13+ (or managed service)
- **Redis**: 6+ (or managed service)
- **Email Service**: SMTP server or service (SendGrid, AWS SES)
- **File Storage**: AWS S3, Google Cloud Storage, or local storage
- **Domain**: For production deployment

## 🌍 Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/educrowd.git
cd educrowd
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=educrowd
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Frontend URL
FRONTEND_URL=https://yourdomain.com

# Payment Gateways (for production)
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

# File Storage (AWS S3 example)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_S3_REGION_NAME=us-east-1
```

## 💻 Local Development

### Option 1: Docker Development (Recommended)

```bash
# Start all services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create test data
docker-compose exec web python manage.py create_test_data

# Access the application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### Option 2: Local Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run_dev.py
```

### Development Commands

```bash
# Run tests
python manage.py test

# Run linting
flake8 .

# Run type checking
mypy .

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create test data
python manage.py create_test_data
```

## 🧪 Staging Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Application Deployment

```bash
# Clone repository
git clone https://github.com/your-org/educrowd.git
cd educrowd

# Create staging environment file
cp .env.example .env.staging

# Configure staging environment
nano .env.staging
```

**Staging Environment Variables:**

```env
DEBUG=False
ALLOWED_HOSTS=staging.yourdomain.com
DATABASE_URL=postgres://user:pass@staging-db:5432/educrowd
REDIS_URL=redis://staging-redis:6379/0
FRONTEND_URL=https://staging.yourdomain.com
```

### 3. Deploy with Docker

```bash
# Build and start services
docker-compose -f docker-compose.staging.yml up --build -d

# Run migrations
docker-compose -f docker-compose.staging.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.staging.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.staging.yml exec web python manage.py collectstatic --noinput
```

### 4. Nginx Configuration

```nginx
# /etc/nginx/sites-available/educrowd-staging
server {
    listen 80;
    server_name staging.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/educrowd/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/educrowd/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

## 🏭 Production Deployment

### 1. Server Requirements

- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 100GB+ SSD
- **Network**: High bandwidth connection

### 2. Production Environment Setup

```bash
# Create production user
sudo adduser educrowd
sudo usermod -aG docker educrowd
sudo usermod -aG sudo educrowd

# Switch to production user
su - educrowd

# Clone repository
git clone https://github.com/your-org/educrowd.git
cd educrowd

# Create production environment
cp .env.example .env.production
nano .env.production
```

**Production Environment Variables:**

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgres://user:pass@prod-db:5432/educrowd
REDIS_URL=redis://prod-redis:6379/0
FRONTEND_URL=https://yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# File Storage
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
STATICFILES_STORAGE=storages.backends.s3boto3.S3StaticStorage
```

### 3. Database Setup

#### Option A: Managed Database (Recommended)

```bash
# Using AWS RDS
aws rds create-db-instance \
    --db-instance-identifier educrowd-prod \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --master-username educrowd \
    --master-user-password your-secure-password \
    --allocated-storage 100 \
    --vpc-security-group-ids sg-12345678
```

#### Option B: Self-Managed Database

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE educrowd;
CREATE USER educrowd WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE educrowd TO educrowd;
\q
```

### 4. Redis Setup

#### Option A: Managed Redis (Recommended)

```bash
# Using AWS ElastiCache
aws elasticache create-cache-cluster \
    --cache-cluster-id educrowd-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

#### Option B: Self-Managed Redis

```bash
# Install Redis
sudo apt install redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set: requirepass your-redis-password
# Set: bind 127.0.0.1

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis
```

### 5. Application Deployment

```bash
# Build production image
docker build -t educrowd:latest .

# Deploy with production compose
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 6. Nginx Configuration

```nginx
# /etc/nginx/sites-available/educrowd
upstream educrowd_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Static Files
    location /static/ {
        alias /var/www/educrowd/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/educrowd/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Application
    location / {
        proxy_pass http://educrowd_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 7. SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🐳 Docker Deployment

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    image: educrowd:latest
    restart: unless-stopped
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:pass@db:5432/educrowd
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_DB=educrowd
      - POSTGRES_USER=educrowd
      - POSTGRES_PASSWORD=your-secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass your-redis-password
    deploy:
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  celery:
    build: .
    image: educrowd:latest
    restart: unless-stopped
    command: celery -A educrowd worker -l info
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:pass@db:5432/educrowd
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  celery-beat:
    build: .
    image: educrowd:latest
    restart: unless-stopped
    command: celery -A educrowd beat -l info
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:pass@db:5432/educrowd
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## 📊 Monitoring & Logging

### 1. Application Monitoring

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/educrowd/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

### 2. Health Checks

```python
# health_check.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health_check(request):
    status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'services': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['services']['database'] = 'healthy'
    except Exception as e:
        status['services']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Redis check
    try:
        cache.get('health_check')
        status['services']['redis'] = 'healthy'
    except Exception as e:
        status['services']['redis'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    return JsonResponse(status)
```

### 3. System Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs

# Monitor Docker containers
docker stats
docker-compose logs -f
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Check database connectivity
docker-compose exec web python manage.py dbshell

# Test database connection
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

#### 2. Redis Connection Issues

```bash
# Check Redis connectivity
docker-compose exec redis redis-cli ping

# Test Redis connection
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value')
>>> cache.get('test')
```

#### 3. Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static file permissions
sudo chown -R www-data:www-data /var/www/educrowd/staticfiles/
```

#### 4. Celery Not Processing Tasks

```bash
# Check Celery status
docker-compose exec celery celery -A educrowd inspect active

# Check Celery logs
docker-compose logs celery
```

### Performance Optimization

#### 1. Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX CONCURRENTLY idx_courses_tenant_id ON courses_course(tenant_id);
CREATE INDEX CONCURRENTLY idx_user_roles_user_tenant ON users_userrole(user_id, tenant_id, is_active);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM courses_course WHERE tenant_id = 1;
```

#### 2. Application Optimization

```python
# Use select_related and prefetch_related
courses = Course.objects.select_related('tenant').prefetch_related(
    'lessons', 'enrollments'
).filter(tenant=request.tenant)

# Use database-level pagination
from django.core.paginator import Paginator
paginator = Paginator(courses, 20)
```

#### 3. Caching Strategy

```python
# Cache expensive queries
from django.core.cache import cache

def get_tenant_stats(tenant_id):
    cache_key = f"tenant_stats_{tenant_id}"
    stats = cache.get(cache_key)
    if not stats:
        stats = calculate_tenant_stats(tenant_id)
        cache.set(cache_key, stats, 3600)  # Cache for 1 hour
    return stats
```

### Backup and Recovery

#### 1. Database Backup

```bash
# Create database backup
docker-compose exec db pg_dump -U educrowd educrowd > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database backup
docker-compose exec -T db psql -U educrowd educrowd < backup_20240101_120000.sql
```

#### 2. Media Files Backup

```bash
# Backup media files
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/

# Restore media files
tar -xzf media_backup_20240101_120000.tar.gz
```

### Security Checklist

- [ ] Change default passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable monitoring and alerting
- [ ] Keep system and dependencies updated
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable security headers
- [ ] Regular security audits

---

**Deployment Status**: Ready for Week 1  
**Next Update**: Week 2 (LMS Module Deployment)  
**Support**: deployment@educrowd.com
