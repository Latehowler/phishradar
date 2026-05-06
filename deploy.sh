#!/bin/bash
# Quick deployment script for Linux/macOS servers

set -e

echo "Starting Phishing Detection System deployment..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y nginx

# Clone repository
cd /opt
sudo git clone https://github.com/yourusername/phishing-detection-system.git
cd phishing-detection-system

# Create virtual environment
python3.11 -m venv env
source env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
sudo cp .env.example .env
sudo nano .env  # Edit with your values

# Create database
sudo -u postgres psql << EOF
CREATE USER phishing WITH PASSWORD 'your-password';
CREATE DATABASE phishing_db OWNER phishing;
GRANT ALL PRIVILEGES ON DATABASE phishing_db TO phishing;
EOF

# Initialize database
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF

# Configure systemd service
sudo tee /etc/systemd/system/phishing-detection.service > /dev/null << EOF
[Unit]
Description=Phishing Detection System
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/phishing-detection-system
Environment="PATH=/opt/phishing-detection-system/env/bin"
ExecStart=/opt/phishing-detection-system/env/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app.app:create_app('production')"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable phishing-detection
sudo systemctl start phishing-detection

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/phishing-detection
sudo ln -s /etc/nginx/sites-available/phishing-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up SSL with Let's Encrypt
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

echo "Deployment complete!"
echo "Your application is running at https://yourdomain.com"
