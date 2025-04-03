# Deployment Guide: Flask Application to DigitalOcean with johnboen.com Domain

This comprehensive guide will walk you through deploying your Flask application to DigitalOcean and connecting it to your johnboen.com domain.

## Table of Contents
1. [DigitalOcean Setup](#1-digitalocean-setup)
2. [Domain Configuration](#2-domain-configuration)
3. [Server Configuration](#3-server-configuration)
4. [Application Deployment](#4-application-deployment)
5. [SSL Certificate Setup](#5-ssl-certificate-setup)
6. [Maintenance Tasks](#6-maintenance-tasks)
7. [Troubleshooting](#7-troubleshooting)

## 1. DigitalOcean Setup

### Create a DigitalOcean Account
1. Go to [DigitalOcean](https://www.digitalocean.com/) and sign up for an account
2. Verify your email and set up payment information

### Create a Droplet
1. From the DigitalOcean dashboard, click **Create** → **Droplets**
2. Choose an image: **Ubuntu 22.04 (LTS) x64**
3. Select a plan:
   - Basic (Shared CPU)
   - Regular Intel: $6/mo (1GB RAM, 1 CPU, 25GB SSD)
4. Choose a datacenter region:
   - Select a region close to your target audience (e.g., New York for US East Coast)
5. Authentication:
   - Choose **SSH keys** (recommended) or **Password**
   - If using SSH keys, follow DigitalOcean's guide to add your public key
6. Hostname: `johnboen-web`
7. Click **Create Droplet**

### Create a Project (Optional)
1. From the dashboard, go to **Projects** → **New Project**
2. Name: `johnboen-website`
3. Description: `Flask application for johnboen.com`
4. Move your droplet to this project

## 2. Domain Configuration

### Point johnboen.com to DigitalOcean
1. Log in to your domain registrar where johnboen.com is registered
2. Find the DNS management section
3. Update the nameservers to DigitalOcean's nameservers:
   - `ns1.digitalocean.com`
   - `ns2.digitalocean.com`
   - `ns3.digitalocean.com`
4. Save changes (may take 24-48 hours to propagate)

### Configure DNS in DigitalOcean
1. In DigitalOcean, go to **Networking** → **Domains**
2. Click **Add Domain** and enter `johnboen.com`
3. Create the following DNS records:
   - **A record**: `@` pointing to your Droplet's IP
   - **A record**: `www` pointing to your Droplet's IP
   - **CNAME record**: `*` pointing to `johnboen.com.`
4. If you use email with this domain, add appropriate MX records

## 3. Server Configuration

### Connect to Your Droplet
```bash
ssh root@your_droplet_ip
```

### Initial Server Setup
```bash
# Update packages
apt update && apt upgrade -y

# Set timezone
timedatectl set-timezone America/New_York  # Change to your timezone

# Create a deploy user
adduser deploy
# Enter a strong password when prompted

# Give deploy user sudo privileges
usermod -aG sudo deploy

# Set up SSH for the deploy user (if using SSH keys)
mkdir -p /home/deploy/.ssh
cp ~/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys

# Configure firewall
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### Log in as deploy user
```bash
# Exit root session
exit

# Log in as deploy user
ssh deploy@your_droplet_ip
```

### Install Required Software
```bash
# Install required packages
sudo apt install -y git curl wget unzip software-properties-common

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add deploy user to docker group
sudo usermod -aG docker deploy
# Log out and log back in for this to take effect
exit
ssh deploy@your_droplet_ip

# Install Certbot for SSL certificates
sudo apt install -y certbot
```

## 4. Application Deployment

### Set Up Application Directory
```bash
# Create application directory
mkdir -p ~/apps
cd ~/apps

# Clone your repository (replace with your actual repository URL)
git clone https://github.com/yourusername/yourrepository.git pythonweb
cd pythonweb
```

### Configure Environment Variables
```bash
# Create production environment file
cp .env.production.example .env.production
nano .env.production
```

Edit the `.env.production` file with the following settings:
```
# Flask settings
FLASK_APP=run.py
FLASK_CONFIG=production
SECRET_KEY=generate_a_secure_random_key_here

# Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Database settings
DATABASE_URL=postgresql://postgres:choose_a_secure_password@db:5432/pythonweb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=choose_a_secure_password
POSTGRES_DB=pythonweb

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Mail settings (if applicable)
MAIL_SERVER=your_mail_server
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@johnboen.com
MAIL_PASSWORD=your_email_password
```

### Configure Nginx for johnboen.com
```bash
# Create nginx configuration directory
mkdir -p nginx/conf.d
nano nginx/conf.d/app.conf
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name johnboen.com www.johnboen.com;

    # Redirect HTTP to HTTPS (will be enabled after SSL setup)
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name johnboen.com www.johnboen.com;

    # SSL configuration (will be configured after SSL setup)
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Static files
    location /static/ {
        alias /app/static/;
        expires 30d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://web:8000;
        proxy_redirect off;
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "upgrade";
        proxy_set_header Upgrade $http_upgrade;
    }

    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /500.html;
}
```

### Deploy the Application
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy the application (without SSL for now)
./deploy.sh --env prod --build --migrate
```

## 5. SSL Certificate Setup

### Obtain SSL Certificate
```bash
# Stop any services using ports 80/443
docker-compose down

# Get SSL certificates
sudo certbot certonly --standalone -d johnboen.com -d www.johnboen.com
# Enter your email when prompted
# Agree to the terms of service
# Choose whether to share your email

# Create SSL directory and copy certificates
sudo mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/johnboen.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/johnboen.com/privkey.pem nginx/ssl/key.pem
sudo chown -R deploy:deploy nginx/ssl
```

### Restart the Application with SSL
```bash
# Restart the application
docker-compose up -d
```

### Set Up Automatic SSL Renewal
```bash
# Create a renewal script
nano ~/renew_ssl.sh
```

Add the following content:
```bash
#!/bin/bash
# SSL renewal script for johnboen.com

# Stop services using port 80
cd ~/apps/pythonweb
docker-compose stop nginx

# Renew certificates
certbot renew --quiet

# Copy new certificates
cp /etc/letsencrypt/live/johnboen.com/fullchain.pem ~/apps/pythonweb/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/johnboen.com/privkey.pem ~/apps/pythonweb/nginx/ssl/key.pem

# Restart services
docker-compose start nginx
```

Make the script executable and set up a cron job:
```bash
chmod +x ~/renew_ssl.sh

# Edit crontab
crontab -e
```

Add this line to run the renewal script twice a month:
```
0 3 1,15 * * ~/renew_ssl.sh
```

## 6. Maintenance Tasks

### Set Up Database Backups
```bash
# Create a backup script
nano ~/backup.sh
```

Add the following content:
```bash
#!/bin/bash
# Backup script for johnboen.com

# Set variables
BACKUP_DIR="/home/deploy/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/deploy/apps/pythonweb"
BACKUP_RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Database backup
echo "Creating database backup..."
cd $APP_DIR
docker-compose exec -T db pg_dump -U postgres pythonweb > $BACKUP_DIR/johnboen_db_$TIMESTAMP.sql

# Compress the backup
gzip $BACKUP_DIR/johnboen_db_$TIMESTAMP.sql

# Backup environment files
echo "Backing up environment files..."
cp $APP_DIR/.env.production $BACKUP_DIR/env_production_$TIMESTAMP.bak

# Remove old backups
echo "Removing backups older than $BACKUP_RETENTION_DAYS days..."
find $BACKUP_DIR -name "johnboen_db_*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete
find $BACKUP_DIR -name "env_production_*.bak" -type f -mtime +$BACKUP_RETENTION_DAYS -delete

echo "Backup completed: $BACKUP_DIR/johnboen_db_$TIMESTAMP.sql.gz"
```

Make the script executable and set up a cron job:
```bash
chmod +x ~/backup.sh

# Edit crontab if not already open
crontab -e
```

Add this line to run daily backups at 2 AM:
```
0 2 * * * ~/backup.sh
```

### Create a Deployment Script for Updates
```bash
# Create a deployment script
nano ~/deploy_update.sh
```

Add the following content:
```bash
#!/bin/bash
# Update deployment script for johnboen.com

cd ~/apps/pythonweb

# Pull latest changes
git pull

# Build and restart containers
docker-compose build
docker-compose up -d

# Run database migrations
docker-compose exec web flask db upgrade

echo "Update completed successfully!"
```

Make the script executable:
```bash
chmod +x ~/deploy_update.sh
```

## 7. Troubleshooting

### Check Application Status
```bash
# Check if containers are running
cd ~/apps/pythonweb
docker-compose ps

# Check application logs
docker-compose logs web

# Check nginx logs
docker-compose logs nginx

# Check database logs
docker-compose logs db
```

### Common Issues and Solutions

#### Website Not Loading
```bash
# Check if DNS is properly configured
nslookup johnboen.com

# Check if Nginx is running
docker-compose ps nginx

# Check Nginx configuration
docker-compose exec nginx nginx -t
```

#### Database Connection Issues
```bash
# Check if database container is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Connect to database
docker-compose exec db psql -U postgres -d pythonweb
```

#### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Manually renew certificates
sudo certbot renew --dry-run
```

#### Application Errors
```bash
# Check application logs
docker-compose logs web

# Access application shell
docker-compose exec web bash

# Test database connection from application
docker-compose exec web python -c "from app import db; print(db.engine.connect())"
```

## Final Verification

After completing all steps, verify your deployment:

1. Visit https://johnboen.com in your browser
2. Check that HTTPS is working correctly
3. Test all major functionality of your application
4. Verify that the site loads at both johnboen.com and www.johnboen.com

Congratulations! Your Flask application is now deployed to DigitalOcean and accessible at johnboen.com with HTTPS.

## Additional Resources

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
