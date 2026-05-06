# VERCEL & RENDER - QUICK REFERENCE

## TL;DR - Which One to Use?

| Need | Choice | Time |
|------|--------|------|
| **Your best option** | 👉 **Render** | 5 min |
| **Free tier** | Vercel (but not ideal) | 15 min |
| **Simplest setup** | PythonAnywhere | 5 min |
| **Enterprise** | AWS | 30 min |

---

## RENDER (Recommended) ⭐⭐⭐⭐⭐

### Why Render?

```
✅ Built for Flask apps (not serverless)
✅ No cold start delays
✅ Built-in PostgreSQL database
✅ Auto-deploy from GitHub (git push = deploy)
✅ Only $14/month total (web + database)
✅ Better performance than Vercel
✅ Perfect for this project
```

### 5-Minute Deployment

```
1. Go to https://render.com
2. Sign up with GitHub
3. New Web Service → Select your repo
4. Fill in:
   - Runtime: Python 3.11
   - Build: pip install -r requirements.txt
   - Start: gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"
5. Create PostgreSQL → Copy DATABASE_URL
6. Add env vars → FLASK_ENV=production, SECRET_KEY, DATABASE_URL
7. Deploy!
8. Initialize DB (in Render Shell):
   python << EOF
   from app.app import create_app
   from app.models import db
   app = create_app('production')
   db.create_all()
   EOF
9. Visit: https://your-app.onrender.com ✅
```

### Why NOT Vercel?

```
❌ Serverless = cold starts (slow)
❌ No persistent memory between requests
❌ ML models may exceed size limits
❌ Session management is difficult
❌ Not optimized for Flask
```

### Render vs Vercel Comparison

```
                  RENDER          VERCEL
Setup              5 min           15 min
Cost              $14/mo          Free
Cold Start        <1 sec          5-10 sec
Persistent Mem    ✅              ❌
Flask Ready       ✅              ⚠️
Best For          Flask           Serverless
Recommendation    YES ⭐⭐⭐⭐⭐   NO ⚠️⚠️
```

---

## RENDER DEPLOYMENT STEPS

### Step 1: Create Account
```
Visit: https://render.com
Sign up with GitHub (easiest)
```

### Step 2: New Web Service
```
Dashboard → New Web Service
Connect GitHub → Select phishing-detection-system
```

### Step 3: Configure
```
Name:          phishing-detection-system
Runtime:       Python 3.11
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"
Plan:          Starter ($7/month)
```

### Step 4: Create Database
```
New PostgreSQL (Starter) → $7/month
Copy DATABASE_URL from PostgreSQL dashboard
```

### Step 5: Environment Variables
```
FLASK_ENV = production
SECRET_KEY = (click "Add Secret" to auto-generate)
DATABASE_URL = (paste from PostgreSQL)
```

### Step 6: Deploy
```
Click "Create Web Service"
Render auto-deploys
Watch logs for progress
```

### Step 7: Initialize Database
```
Go to: Web Service → Shell
Run:
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
db.create_all()
EOF
```

### Step 8: Access
```
Visit: https://phishing-detection-system.onrender.com
```

### Step 9: Auto-Deploy
```
Every git push to GitHub = auto-deploy on Render!
git push origin main  # Render auto-deploys
```

---

## IF YOU REALLY WANT VERCEL

### Problem: Vercel is Serverless

Vercel functions have limitations:
- Cold start delays (users wait 5-10 seconds on first request)
- No persistent memory
- File size limits
- Not ideal for Flask

### Workaround

Create separate API serverless functions:

```python
# api/predict.py
from flask import Flask, request, jsonify
import pickle
import re

app = Flask(__name__)

# Load models
vector = pickle.load(open("models/vectorizer.pkl", 'rb'))
model = pickle.load(open("models/phishing.pkl", 'rb'))

def is_valid_url(url):
    pattern = re.compile(r'^https?://')
    return re.match(pattern, url) is not None

@app.route("/api/predict", methods=['POST'])
def predict():
    url = request.json.get('url', '').strip()
    
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
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Set environment
vercel env add DATABASE_URL
vercel env add SECRET_KEY
```

### Verdict
**Still not recommended.** Use Render instead.

---

## FILE CHECKLIST

✅ New files created for hosting:

```
✅ VERCEL_AND_RENDER.md        (Complete guide)
✅ RENDER_QUICKSTART.md         (5-min setup)
✅ render.yaml                  (Auto-config)
✅ VERCEL_RENDER_REFERENCE.md   (This file)
```

Updated existing files:

```bash
✅ START_HERE.md                (Now recommends Render)
✅ HOSTING_GUIDE.md             (Added Render & Vercel sections)
✅ requirements.txt             (Has gunicorn for production)
```

---

## QUICK COMMANDS

### Test Locally
```bash
python run.py
```

### Generate SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Initialize Database (Render Shell)
```bash
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
db.create_all()
EOF
```

### View Logs (Render)
```
Render Dashboard → Web Service → Logs
```

---

## COST BREAKDOWN

### Render ($14/month)
- Web Service: $7/month
- PostgreSQL: $7/month
- Total: $14/month

### Vercel (Free to $20/month)
- Web Service: Free
- Database: Need external (AWS RDS, etc.)
- + External DB cost

### PythonAnywhere ($5-29/month)
- Web hosting: $5-29/month
- Database: Included

### Heroku ($7-50/month)
- Web hosting: $7-50/month
- Database: Add'l cost

---

## RECOMMENDATION MATRIX

```
Small Project, Learning?          → PythonAnywhere
Production, Scaling?              → Render ⭐
Complex Enterprise?               → AWS ECS
Simple Serverless API?            → Vercel
Rapid Prototyping?                → Heroku
Full Control?                      → Docker + VPS
```

---

## TIME TO DEPLOYMENT

| Platform | Setup Time | Difficulty |
|----------|-----------|-----------|
| Render | 5 min | Easy |
| Heroku | 3 min | Very Easy |
| PythonAnywhere | 5 min | Very Easy |
| Vercel | 15 min | Medium |
| AWS | 30 min | Hard |
| Docker | 1 hr | Hard |

---

## DOCUMENTATION FILES

Read in this order:

1. **VERCEL_AND_RENDER.md** (comprehensive guide)
2. **RENDER_QUICKSTART.md** (5-minute setup)
3. **HOSTING_GUIDE.md** (all options)
4. **START_HERE.md** (overview)

---

## NEXT STEPS

1. Choose platform (recommended: Render)
2. Follow deployment guide (5 minutes for Render)
3. Test application
4. Configure custom domain (optional)
5. Set up monitoring

---

**RECOMMENDATION: Use Render - Best choice for this Flask app! 🚀**

---

**Last Updated: May 2026**
