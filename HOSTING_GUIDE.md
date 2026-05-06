# Hosting & Deployment Guide for Phishing Detection System

A comprehensive guide on how to properly host and deploy this Flask application in production.

## Table of Contents

1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Hosting Options](#hosting-options)
4. [Database Setup](#database-setup)
5. [Environment Variables](#environment-variables)
6. [Security Best Practices](#security-best-practices)
7. [Render (Recommended)](#render-recommended) ⭐
8. [Vercel (Alternative)](#vercel-alternative)

**See also:** [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md) | [VERCEL_AND_RENDER.md](VERCEL_AND_RENDER.md)

---

## Local Development

### Quick Start

```bash
# 1. Activate virtual environment
env\Scripts\activate          # Windows
# or
source env/bin/activate       # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run development server
python run.py
```

**Access:** http://localhost:5000

### Development Settings

Development mode enables:
- Debug mode (auto-reload on code changes)
- Detailed error messages
- CORS disabled for security

Set environment:
```bash
set FLASK_ENV=development     # Windows
export FLASK_ENV=development  # Linux/macOS
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure proper database
- [ ] Set up logging
- [ ] Configure SSL/HTTPS
- [ ] Set up monitoring
- [ ] Create backup strategy
- [ ] Test all features

### Production Environment Variables

```bash
# Essential
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-key-here
DATABASE_URL=postgresql://user:pass@localhost/phishing_db

# Optional
PORT=5000
WORKERS=4
LOG_LEVEL=INFO
```

### Generate Secure SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## Hosting Options

### 1. **Heroku** (Easiest - Recommended for beginners)

#### Setup:

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create phishing-detection-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<your-secret-key>

# Add Procfile
echo "web: gunicorn app.app:create_app('production')" > Procfile

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Pros:** Easy deployment, automatic scaling, free tier available
**Cons:** Paid plans required for production, slower cold starts

**Cost:** Free tier + $7-50/month for production

---

### 2. **AWS (Elastic Beanstalk)** (Professional)

#### Setup:

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 phishing-detection

# Create environment
eb create production-env

# Deploy
eb deploy

# View logs
eb logs
```

**Configuration file (.ebextensions/01_flask.config):**

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: run:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
    PYTHONPATH: /var/app/current:$PYTHONPATH
```

**Pros:** Scalable, reliable, AWS ecosystem integration
**Cons:** More complex setup, requires AWS account

**Cost:** $0.25-1/hour depending on instance type

---

### 3. **PythonAnywhere** (Simple & Fast)

#### Setup:

1. Sign up at https://www.pythonanywhere.com
2. Upload code via Git or web interface
3. Configure virtual environment
4. Add web app with Flask configuration
5. Reload web app

**Configuration:**

```python
# /var/www/yourusername_pythonanywhere_com_wsgi.py
import sys
path = '/home/yourusername/phishing-detection-system'
if path not in sys.path:
    sys.path.insert(0, path)

from app.app import create_app
application = create_app('production')
```

**Pros:** Beginner-friendly, instant hosting, good support
**Cons:** Limited customization, not ideal for large-scale

**Cost:** $5-29/month

---

### 4. **DigitalOcean App Platform** (Mid-tier)

#### Setup:

```yaml
# app.yaml
name: phishing-detection
services:
- name: api
  github:
    master_branch: main
    repo: yourusername/phishing-detection-system
  http_port: 8080
  build_command: pip install -r requirements.txt
  run_command: gunicorn -w 4 -b 0.0.0.0:8080 "app.app:create_app('production')"
  envs:
  - key: FLASK_ENV
    value: production
  - key: SECRET_KEY
    scope: RUN_AND_BUILD_TIME
    value: ${SECRET_KEY}
```

**Pros:** Good performance, git integration, transparent pricing
**Cons:** Requires learning App Platform

**Cost:** $5/month (basic), scales with usage

---

### 5. **Docker + Any Cloud** (Professional/Enterprise)

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.app:create_app('production')"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=phishing
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=phishing_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### Run Docker:

```bash
docker-compose build
docker-compose up -d
```

**Deploy to:**
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Kubernetes

**Pros:** Consistent across environments, scalable, cloud-agnostic
**Cons:** Steeper learning curve

---

## Database Setup

### SQLite (Development)
```python
# Default in config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
```

### PostgreSQL (Production - Recommended)

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/phishing_db"
```

### MySQL

```bash
# Install MySQL driver
pip install mysql-connector-python

# Set environment variable
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/phishing_db"
```

### Initialize Database

```python
from app.app import create_app
from app.models import db

app = create_app('production')
with app.app_context():
    db.create_all()
    print("Database initialized!")
```

---

## Environment Variables

### Required Variables

```
FLASK_ENV          # production / development / testing
SECRET_KEY         # Long random string (min 32 chars)
DATABASE_URL       # Connection string to database
```

### Optional Variables

```
PORT                # Default: 5000
WORKERS             # Gunicorn workers, default: 4
LOG_LEVEL           # DEBUG / INFO / WARNING / ERROR
DEBUG               # True / False (should be False in production)
MAIL_SERVER         # For email notifications
MAIL_PORT           # SMTP port (usually 587 or 465)
```

### Load from .env file

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
load_dotenv()
```

**.env file:**
```
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:pass@localhost/db
```

---

## Security Best Practices

### 1. **HTTPS/SSL**

```bash
# Let's Encrypt (Free SSL)
pip install certbot

# Generate certificate
certbot certonly --standalone -d yourdomain.com
```

### 2. **Strong SECRET_KEY**

```python
import secrets
secret = secrets.token_urlsafe(32)
# Store in environment variable, NOT in code
```

### 3. **Disable Debug in Production**

```python
app.debug = False  # NEVER True in production
```

### 4. **CORS Security**

```python
from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

### 5. **Rate Limiting**

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/api/detect', methods=['POST'])
@limiter.limit("10 per minute")
def detect_phishing():
    pass
```

### 6. **Security Headers**

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 7. **Database Security**

- Use strong passwords
- Don't commit credentials
- Use environment variables
- Create separate database users for production
- Enable SSL for database connections

---

## WSGI Server (Production)

### Gunicorn (Recommended)

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app.app:create_app('production')"

# With SSL
gunicorn \
  --certfile=/path/to/cert.pem \
  --keyfile=/path/to/key.pem \
  -w 4 -b 0.0.0.0:5000 \
  "app.app:create_app('production')"
```

### Uwsgi

```bash
pip install uwsgi

uwsgi --http :5000 --wsgi-file run.py --callable app -p 4
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    filename='phishing_detection.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app.logger.info("Application started")
```

### Sentry for Error Tracking

```bash
pip install sentry-sdk

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://your-sentry-url@sentry.io/12345",
    integrations=[FlaskIntegration()]
)
```

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    return {'status': 'OK'}, 200
```

---

## Recommended Production Stack

```
┌─────────────────────────────────────┐
│  Domain (GoDaddy / Namecheap)       │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Nginx Reverse Proxy + SSL          │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Gunicorn (4 workers)               │
│  Flask Application                  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  PostgreSQL Database                │
└─────────────────────────────────────┘
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Quick Deployment Comparison

| Platform | Difficulty | Cost | Scalability | Best For |
|----------|-----------|------|------------|----------|
| Heroku | Easy | $7-50/mo | Good | Startups |
| PythonAnywhere | Very Easy | $5-29/mo | Limited | Learning |
| AWS EB | Medium | $0.25-2/hr | Excellent | Enterprise |
| DigitalOcean | Medium | $5-40/mo | Good | SMB |
| Docker + K8s | Hard | Varies | Excellent | Large Scale |

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

### Import Errors in Production
- Ensure all dependencies are in `requirements.txt`
- Test in virtual environment first
- Check PYTHONPATH configuration

### Model Files Not Found
- Verify models directory exists
- Check file permissions
- Use absolute paths in configuration

### SSL Certificate Issues
- Verify certificate validity
- Check certificate chain
- Ensure proper permissions (644 for certs, 600 for keys)

---

## Render (Recommended) ⭐

**Render** is purpose-built for Python Flask applications and offers excellent performance and value.

### 5-Minute Setup

See: [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md) for step-by-step instructions.

### Key Advantages

✅ Python/Flask optimized (not serverless limitations)
✅ Auto-deploy from GitHub push
✅ Built-in PostgreSQL database
✅ No cold starts (unlike Vercel serverless)
✅ Perfect for this project
✅ SSL/HTTPS automatic
✅ Professional dashboard
✅ Good performance
✅ Production-ready

### Render Pricing

- **Web Service (Starter):** $7/month
- **PostgreSQL (Starter):** $7/month
- **Total:** $14/month

### Quick Stats

- Setup time: 5 minutes
- Auto-deploy: Yes (on GitHub push)
- Scalability: Good
- Recommended: ⭐⭐⭐⭐⭐ (BEST for this project)

### Configuration

Use the included `render.yaml` file for automatic setup, or manually configure:

```yaml
services:
  - type: web
    name: phishing-detection-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    autoDeploy: true

  - type: pserv
    name: phishing-detection-db
    plan: starter
```

---

## Vercel (Alternative)

**Vercel** is optimized for serverless functions and frontend deployments, not ideal for Flask.

### Why Vercel is NOT Recommended for This Project

❌ **Serverless limitations** - Cold starts (5-10 second delays)
❌ **Stateless** - No persistent memory between requests
❌ **ML models** - .pkl files may exceed bundle size limits
❌ **Session storage** - Difficult with serverless architecture
❌ **Performance** - Slower for heavy computation than Render

### If You Still Want to Use Vercel

#### Workaround: Serverless Functions

Create `api/index.py`:

```python
from flask import Flask, request, jsonify
import pickle
import re

app = Flask(__name__)

# Load models
vector = pickle.load(open("models/vectorizer.pkl", 'rb'))
model = pickle.load(open("models/phishing.pkl", 'rb'))

@app.route("/api/predict", methods=['POST'])
def predict():
    try:
        url = request.json.get('url', '').strip()
        # ... prediction logic ...
        return jsonify({'prediction': prediction, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

#### Vercel Configuration

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "runtime": "python3.9",
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" }
  ]
}
```

#### Deploy

```bash
npm install -g vercel
vercel
```

### Vercel Verdict

For this Flask application: **Not recommended**

If you want serverless: Use **Render** instead (better for Flask)

For simple API-only: Vercel could work with significant modifications

---

## Platform Comparison: Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| **Best For** | Flask apps ⭐ | Serverless frontend |
| **Setup Time** | 5 minutes | 15 minutes |
| **Cost** | $14/mo (web+db) | Free tier available |
| **Cold Starts** | <1 second | 5-10 seconds |
| **Persistent Backend** | ✅ Yes | ❌ No |
| **Database** | ✅ Built-in | ❌ External only |
| **Flask Compatibility** | ⭐⭐⭐⭐⭐ | ⭐⭐ (difficult) |
| **ML Models** | ✅ Good | ⚠️ Limited |
| **Scalability** | Good | Excellent (for serverless) |
| **Recommendation** | ✅ YES | ⚠️ Not ideal |

---

## Complete Deployment Comparison

| Platform | Difficulty | Cost | Setup | Best For | Recommendation |
|----------|-----------|------|-------|----------|---|
| **Render** | Easy | $14/mo | 5 min | Flask apps | ⭐⭐⭐⭐⭐ BEST |
| **Heroku** | Easy | $7-50/mo | 3 min | Quick prototypes | ⭐⭐⭐⭐ Good |
| **PythonAnywhere** | Very Easy | $5-29/mo | 5 min | Beginners | ⭐⭐⭐⭐ Good |
| **DigitalOcean** | Medium | $5-40/mo | 20 min | SMB | ⭐⭐⭐⭐ Good |
| **AWS EB** | Medium | $0.25-2/hr | 30 min | Enterprise | ⭐⭐⭐⭐ Good |
| **Docker + K8s** | Hard | Varies | 1+ hour | Large Scale | ⭐⭐⭐ Complex |
| **Vercel** | Medium | Free-$20 | 15 min | Serverless | ⭐⭐ Not ideal |

---

## Resources

- [Render Documentation](https://render.com/docs)
- [Render Quick Deploy](https://render.com/docs/deploy-flask)
- [Vercel Documentation](https://vercel.com/docs)
- [RENDER_QUICKSTART.md](RENDER_QUICKSTART.md) - 5-minute setup
- [VERCEL_AND_RENDER.md](VERCEL_AND_RENDER.md) - Detailed comparison

---

**Last Updated: May 2026**
