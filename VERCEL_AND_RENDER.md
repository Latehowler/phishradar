# Hosting on Vercel & Render

Complete guide to deploy your Phishing Detection System on **Vercel** and **Render**.

## Table of Contents

1. [Render (Recommended for Flask)](#render-recommended)
2. [Vercel (Alternative)](#vercel-alternative)
3. [Comparison](#comparison)
4. [Troubleshooting](#troubleshooting)

---

## Render (Recommended) ⭐

**Render** is purpose-built for Python/Flask apps and is the better choice for this project.

### Step-by-Step Setup

#### 1. **Create Render Account**
- Go to: https://render.com
- Sign up (use GitHub for easy login)

#### 2. **Connect Repository**
- Click "New +" → "Web Service"
- Choose "Build from GitHub repository"
- Connect your GitHub account
- Select your `phishing-detection-system` repository

#### 3. **Configure Deployment**

**Runtime Settings:**
- **Name:** `phishing-detection-system`
- **Runtime:** `Python 3.11`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"`

#### 4. **Set Environment Variables**

In Render dashboard, add:

```
FLASK_ENV = production
SECRET_KEY = <generate-with: python -c "import secrets; print(secrets.token_urlsafe(32))">
DATABASE_URL = postgresql://<user>:<password>@<host>:<port>/<database>
```

#### 5. **Add Database (PostgreSQL)**

**Option A: Render PostgreSQL (Recommended)**
```
1. In Render: New "PostgreSQL" service
2. Copy DATABASE_URL from Render
3. Paste into web service environment variables
4. Click "Deploy"
```

**Option B: Use External Database**
```
1. Use Render PostgreSQL, AWS RDS, or other service
2. Set DATABASE_URL environment variable to connection string
```

#### 6. **Deploy**
- Click "Deploy"
- Watch logs for any errors
- Once deployed: `your-app-name.onrender.com`

#### 7. **Initialize Database**

After first deployment, run:
```bash
# In Render dashboard, go to Web Service → Shell
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
with app.app_context():
    db.create_all()
    print("Database initialized!")
EOF
```

### render.yaml (Automatic Setup - Optional)

Create `render.yaml` in your repo root:

```yaml
services:
  - type: web
    name: phishing-detection
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"
    
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.10
    
    autoDeploy: true
    
  - type: pserv
    name: phishing-detection-db
    ipAllowList: []
    plan: starter
```

**Deploy with render.yaml:**
```bash
# Push to GitHub
git add render.yaml
git commit -m "Add Render configuration"
git push

# In Render dashboard: "New" → "Blueprint" → Select repo → Auto-deploy
```

### Render Pricing

- **Web Service (Starter):** $7/month
- **PostgreSQL (Starter):** $7/month
- **Total:** $14/month for production

Free tier available for testing (limited resources)

---

## Vercel (Alternative)

**Note:** Vercel is optimized for serverless, but can work with Python using serverless functions.

### Challenges with Vercel + Flask

1. **No persistent backend** - Vercel uses serverless functions
2. **Cold start delays** - Functions take time to initialize
3. **ML models** - .pkl files can exceed size limits
4. **Session management** - Difficult with serverless

### Workaround: Vercel Frontend + External Backend

**Best approach:**

```
┌─────────────────────┐
│   Vercel Frontend   │
│  (React/Next.js)    │
└──────────┬──────────┘
           │ API calls
           ▼
┌─────────────────────┐
│  Render Backend     │
│  (Flask API)        │
└─────────────────────┘
```

### If You Still Want to Use Vercel

#### 1. **Create Vercel Function for Flask**

Create `api/index.py`:

```python
from flask import Flask, request, jsonify
import pickle
import os
import re

app = Flask(__name__)

# Load models
vector = pickle.load(open("models/vectorizer.pkl", 'rb'))
model = pickle.load(open("models/phishing.pkl", 'rb'))

def is_valid_url(url):
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

@app.route("/api/predict", methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url.startswith("http"):
            url = "http://" + url
        
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL'}), 400
        
        cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
        X = vector.transform([cleaned_url])
        proba = model.predict_proba(X)[0]
        classes = model.classes_
        
        result_index = proba.argmax()
        prediction = classes[result_index]
        confidence = round(proba[result_index] * 100, 2)
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'url': url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/health", methods=['GET'])
def health():
    return jsonify({'status': 'OK'})
```

#### 2. **Deploy to Vercel**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment if needed
vercel env add SECRET_KEY
```

#### 3. **vercel.json**

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".",
  "functions": {
    "api/*.py": {
      "runtime": "python3.9"
    }
  },
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### Vercel Limitations

❌ **Cold starts** - 5-10 second delays on first request
❌ **Model files** - Limited to /tmp for model storage
❌ **Sessions** - Stateless (no persistent memory)
❌ **Database** - Connect to external DB only
❌ **Concurrent requests** - Limited

**Verdict:** Vercel is NOT recommended for this project. Render is much better.

---

## Comparison

| Feature | Render | Vercel |
|---------|--------|--------|
| **Cost** | $7-14/mo | Free (serverless) |
| **Setup** | 5 minutes | 15 minutes |
| **Best For** | Flask apps | Serverless functions |
| **Cold start** | < 1 sec | 5-10 secs |
| **Persistent backend** | ✅ Yes | ❌ No (serverless) |
| **Database** | ✅ Built-in | ❌ External only |
| **Session storage** | ✅ Yes | ❌ No |
| **ML models** | ✅ Good | ⚠️ Limited |
| **Scalability** | ✅ Excellent | ✅ Auto-scale |
| **Recommendation** | ⭐⭐⭐⭐⭐ | ⭐⭐ (for this project) |

---

## Quick Comparison Table

### For This Project:

```
┌──────────────────────┬────────────┬────────────┐
│ Criterion            │ Render     │ Vercel     │
├──────────────────────┼────────────┼────────────┤
│ Flask compatibility  │ Excellent  │ Difficult  │
│ Setup time          │ 5 min      │ 15 min     │
│ Cost               │ $7-14/mo   │ Free       │
│ Production ready   │ Yes        │ Not ideal  │
│ ML model loading   │ Fast       │ Slow       │
│ Database storage   │ Easy       │ Complex    │
│ Recommended        │ YES ✅     │ NO ⚠️      │
└──────────────────────┴────────────┴────────────┘
```

---

## Troubleshooting

### Render Issues

**Problem: "Build failed"**
```
Solution:
1. Check requirements.txt is in root
2. Verify syntax: pip install -r requirements.txt locally
3. Check Python version in Render (should be 3.9+)
```

**Problem: "Database connection refused"**
```
Solution:
1. Verify DATABASE_URL is set
2. Check PostgreSQL service is running
3. Run database initialization script
```

**Problem: "Model files not found"**
```
Solution:
1. Ensure models/ folder is in Git repo
2. Check .gitignore doesn't exclude .pkl files
3. Verify file paths are relative
```

**Problem: App crashes on startup**
```
Solution:
1. Check logs: Render Dashboard → Logs
2. Verify FLASK_ENV=production
3. Check SECRET_KEY is set
4. Test locally: python run.py
```

### Vercel Issues

**Problem: "Timeout errors"**
```
Solution:
1. Increase timeout in vercel.json
2. Use background tasks for heavy processing
3. Split into multiple serverless functions
```

**Problem: "Module not found"**
```
Solution:
1. Add to requirements.txt
2. Rebuild: vercel --prod
```

---

## Recommended Approach

### **Use Render + GitHub**

This is the optimal setup:

```
┌─────────────────┐
│  GitHub Repo    │
│  (your code)    │
└────────┬────────┘
         │ auto-deploy on push
         ▼
┌─────────────────┐
│ Render Platform │
├─────────────────┤
│ Web Service     │ $7/mo
│  (Gunicorn)     │
├─────────────────┤
│ PostgreSQL DB   │ $7/mo
└─────────────────┘
```

**Benefits:**
- ✅ Automatic deployment on GitHub push
- ✅ Built-in PostgreSQL database
- ✅ Easy environment variables
- ✅ Good performance
- ✅ Professional dashboard
- ✅ Easy SSL/HTTPS (automatic)
- ✅ Logs and monitoring
- ✅ Only $14/month for both

**Steps:**
1. Push code to GitHub
2. Go to render.com
3. Connect GitHub repo
4. Select Python 3.11
5. Click Deploy
6. Done! 🚀

---

## Deploy to Render (5-Minute Setup)

### Command-Line Version

If you have Render CLI:

```bash
# Install Render CLI
npm install -g @render-com/cli

# Login
render login

# Deploy
render deploy \
  --name phishing-detection \
  --runtime python-3.11 \
  --buildCommand "pip install -r requirements.txt" \
  --startCommand "gunicorn -w 4 -b 0.0.0.0:\$PORT 'app.app:create_app(\"production\")'"
```

### Web Dashboard Version (Easier)

1. **Visit:** https://render.com
2. **Sign-up** → Connect GitHub
3. **New Web Service** → Select your repo
4. **Configure:**
   - Runtime: Python 3.11
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"`
5. **Environment vars:**
   ```
   FLASK_ENV=production
   SECRET_KEY=<generated>
   DATABASE_URL=<from Render Postgres>
   ```
6. **Create PostgreSQL** → Copy DATABASE_URL
7. **Deploy!** ✅

---

## Post-Deployment

### Initialize Database

```bash
# SSH into Render via Shell tab
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
with app.app_context():
    db.create_all()
EOF
```

### Monitor Logs

```bash
# In Render Dashboard
tail -f logs/render.log
```

### Custom Domain

```
1. Render Dashboard → Settings
2. Add custom domain
3. Update DNS records (CNAME)
4. SSL auto-provisioned!
```

---

## Summary

| Platform | Recommendation | Setup | Cost |
|----------|---|---|---|
| **Render** | ✅ YES (Recommended) | 5 min | $14/mo |
| **Vercel** | ⚠️ Not ideal | 15 min | Free |
| **Heroku** | ✅ Good | 3 min | $7-50 |
| **PythonAnywhere** | ✅ Good | 5 min | $5-29 |

---

**Best Choice: Render** 🏆

Start here: https://render.com

---

**Last Updated: May 2026**
