# Quick Deploy to Render (5 Minutes)

**RECOMMENDED:** Use Render for this Flask application.

## Prerequisites

- GitHub account (with your code pushed)
- Render account (free at render.com)

## Step 1: Connect GitHub

1. Go to https://render.com
2. Sign up (use GitHub for easiest setup)
3. Click "New +" → "Web Service"
4. Choose "Build from GitHub repository"
5. Search and select `phishing-detection-system`
6. Click "Connect"

## Step 2: Configure Web Service

Fill in these fields:

```
Name:                phishing-detection-system
Runtime:             Python 3.11
Root Directory:      (leave blank)
Build Command:       pip install -r requirements.txt
Start Command:       gunicorn -w 4 -b 0.0.0.0:$PORT "app.app:create_app('production')"
Plan:                Starter ($7/month)
```

Click **Create Web Service**

## Step 3: Add Environment Variables

In the dashboard, go to **Environment**:

```
FLASK_ENV              production
SECRET_KEY             (click "Add Secret" to generate)
```

## Step 4: Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Name: `phishing-detection-db`
3. Plan: Starter
4. Click "Create Database"

5. After creation, note the `DATABASE_URL` shown
6. Go back to Web Service → Environment
7. Add: `DATABASE_URL` = `<copy from PostgreSQL dashboard>`

## Step 5: Deploy

- Render automatically starts deploying
- Watch the logs for completion
- You'll see: `https://phishing-detection-system.onrender.com`

## Step 6: Initialize Database

After deployment succeeds:

1. Go to Web Service → Shell
2. Run:

```bash
python << EOF
from app.app import create_app
from app.models import db
app = create_app('production')
with app.app_context():
    db.create_all()
    print("Database created!")
EOF
```

3. Exit shell

## Step 7: Test

Visit: `https://phishing-detection-system.onrender.com`

✅ **Done!** Your app is live on Render!

---

## Auto-Deploy on GitHub Push

Render automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update phishing detection"
git push origin main

# Render auto-deploys! Check dashboard for status
```

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Web Service | $7/mo | Auto-scales, no cold starts |
| PostgreSQL | $7/mo | 1GB storage, plenty for this app |
| **Total** | $14/mo | Best value for production |

---

## Custom Domain (Optional)

1. Render Dashboard → Settings
2. "Custom Domain"
3. Add your domain
4. Update DNS (CNAME) in your domain provider
5. SSL certificate auto-generated!

---

## Monitoring & Logs

### View Logs
```
Render Dashboard → Web Service → Logs
```

### Health Check
```
Render automatically checks: https://your-app.onrender.com/health
```

---

## Troubleshooting

### "Build failed"
- Check requirements.txt syntax
- Verify no import errors locally
- Check Python version compatibility

### "App crashes after deploy"
- Check logs: Render Dashboard → Logs
- Verify environment variables are set
- Test locally: `python run.py`

### "Database connection error"
- Verify DATABASE_URL in environment
- Check PostgreSQL is running
- Run initialization script

---

## Next Steps

1. ✅ App deployed
2. Test phishing detection feature
3. Add custom domain (optional)
4. Set up monitoring/alerts
5. Configure backup strategy

---

**Your app is now live on Render! 🎉**

Access it at: `https://phishing-detection-system.onrender.com`

---

**Alternative: If you want Vercel instead, see VERCEL_AND_RENDER.md**
