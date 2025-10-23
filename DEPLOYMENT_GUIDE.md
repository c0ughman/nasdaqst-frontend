# NASDAQ Sentiment Tracker - Deployment Guide

## Overview
This guide will walk you through deploying your NASDAQ Sentiment Tracker with:
- **Backend**: Railway (Django REST API + PostgreSQL + Cron jobs)
- **Frontend**: Netlify (Static HTML dashboard)

**Estimated Time**: 20-30 minutes
**Monthly Cost**: ~$5 (Railway) + Free (Netlify)

---

## Prerequisites

Before you begin, make sure you have:
- [ ] GitHub account
- [ ] Railway account (sign up at [railway.app](https://railway.app))
- [ ] Netlify account (sign up at [netlify.com](https://netlify.com))
- [ ] Your API keys ready:
  - Finnhub API key
  - HuggingFace API key
  - Reddit API credentials (client ID, client secret, user agent)

---

## Part 1: Deploy Backend to Railway

### Step 1: Push Code to GitHub

```bash
cd "/Users/coughman/Desktop/Nasdaq Sentiment Tracker"
git add -A
git commit -m "Prepare for deployment"
git push origin main
```

If you don't have a remote repository yet:
```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-sentiment-tracker.git
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `nasdaq-sentiment-tracker` repository
6. Railway will detect it's a Django app and start deploying

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Link it to your Django app

### Step 4: Configure Environment Variables

1. Click on your Django service
2. Go to **"Variables"** tab
3. Add the following variables:

```
DJANGO_SECRET_KEY=<generate-a-long-random-string>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.up.railway.app
FRONTEND_URLS=https://your-app.netlify.app
FINNHUB_API_KEY=<your-finnhub-key>
HUGGINGFACE_API_KEY=<your-huggingface-key>
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_CLIENT_SECRET=<your-reddit-client-secret>
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

**Generate Django Secret Key:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Set Root Directory

Since your Django app is in the `backend/` folder:

1. Go to **"Settings"** tab
2. Find **"Root Directory"**
3. Set it to: `backend`
4. Click **"Save"**

### Step 6: Deploy & Run Migrations

Railway will automatically deploy. Once deployed:

1. Go to **"Deployments"** tab
2. Wait for deployment to complete (green checkmark)
3. Click on your service → **"Settings"** → **"Metrics"**
4. Find the public URL (e.g., `https://your-app.up.railway.app`)

Run migrations using Railway CLI or the dashboard:
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli
railway login
railway link
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

**OR** use the Railway dashboard:
1. Click **"Settings"** → **"Deploy Triggers"** → **"Add Command"**
2. Run: `python manage.py migrate`
3. Run: `python manage.py createsuperuser` (follow prompts)

### Step 7: Verify Backend is Running

Visit your Railway URL + `/api/dashboard/`:
```
https://your-app.up.railway.app/api/dashboard/
```

You should see JSON data (may be empty initially).

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Update Frontend with Backend URL

1. Open `nasdaq.html` in your editor
2. Find line ~1465:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : (window.BACKEND_URL || 'REPLACE_WITH_YOUR_RAILWAY_URL');
```

3. Replace `'REPLACE_WITH_YOUR_RAILWAY_URL'` with your Railway backend URL:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : 'https://your-app.up.railway.app/api';
```

4. Save and commit:
```bash
git add nasdaq.html
git commit -m "Update frontend with production backend URL"
git push
```

### Step 2: Deploy to Netlify

**Option A: Drag and Drop (Easiest)**
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"Add new site"** → **"Deploy manually"**
3. Drag and drop these files:
   - `nasdaq.html`
   - `netlify.toml`
4. Netlify will deploy instantly

**Option B: GitHub Integration (Recommended)**
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect to GitHub and select your repository
4. Configure:
   - **Base directory**: Leave empty (root)
   - **Build command**: Leave empty
   - **Publish directory**: `.` (root)
5. Click **"Deploy site"**

### Step 3: Update Backend CORS Settings

Once Netlify gives you a URL (e.g., `https://random-name.netlify.app`):

1. Go back to Railway
2. Update the `FRONTEND_URLS` environment variable:
```
FRONTEND_URLS=https://your-app.netlify.app
```

3. If using a custom domain, add it too:
```
FRONTEND_URLS=https://your-app.netlify.app,https://yourdomain.com
```

4. Railway will automatically redeploy

### Step 4: Verify Frontend Works

Visit your Netlify URL:
```
https://your-app.netlify.app
```

You should see the dashboard loading data from your Railway backend!

---

## Part 3: Configure Scheduled Task (Cron Job)

The `railway.json` file already configures a cron job to run every minute.

### Verify Cron Job is Running:

1. In Railway, go to your service
2. Click **"Observability"** tab → **"Logs"**
3. Wait 1-2 minutes during market hours
4. You should see logs like:
```
⏸️  Market Closed - Skipping Run
```
OR (during market hours):
```
🚀 NASDAQ Composite Sentiment Tracker - Hybrid Approach
```

### If Cron Job Isn't Working:

Railway's cron feature may require the **Pro plan**. Alternative:

**Use an External Cron Service:**

1. Create a simple trigger endpoint in Django (optional)
2. Use a free service like **cron-job.org**:
   - Visit https://cron-job.org
   - Create account
   - Add new cron job
   - URL: `https://your-app.up.railway.app/api/trigger/` (if you create endpoint)
   - Schedule: `* * * * *` (every minute)

**OR stick with Railway's cron in `railway.json` - it should work!**

---

## Part 4: Final Verification & Testing

### Backend Health Check:
```bash
curl https://your-app.up.railway.app/api/health/
```
Should return: `{"status":"ok","message":"API is running successfully"}`

### Test API Endpoint:
```bash
curl https://your-app.up.railway.app/api/dashboard/
```
Should return JSON with composite score, drivers, etc.

### Frontend Dashboard:
Visit `https://your-app.netlify.app` and verify:
- [ ] Composite sentiment score displays
- [ ] 4 driver cards show correct weights (35%, 25%, 20%, 20%)
- [ ] Chart displays historical data
- [ ] Market status banner shows (green if open, red if closed)

---

## Troubleshooting

### Backend Issues:

**"Application Error" or 500 errors:**
1. Check Railway logs: Service → "Logs" tab
2. Common issues:
   - Missing environment variables
   - Database connection issues
   - Missing migrations

**Fix:** Run migrations again:
```bash
railway run python manage.py migrate
```

**CORS Errors:**
1. Verify `FRONTEND_URLS` in Railway matches your Netlify URL
2. Make sure Railway has redeployed after changing env vars

### Frontend Issues:

**"Failed to fetch" errors:**
1. Check browser console (F12)
2. Verify the `API_BASE_URL` in `nasdaq.html` is correct
3. Test backend directly: `curl https://your-app.up.railway.app/api/dashboard/`

**Chart not showing data:**
1. Wait for cron job to run during market hours
2. Check if database has data: Railway → PostgreSQL → "Data" tab
3. Query: `SELECT * FROM api_analysisrun ORDER BY timestamp DESC LIMIT 5;`

### Cron Job Not Running:

1. Check Railway logs for cron output
2. Verify `railway.json` is in the `backend/` directory
3. Railway may require Pro plan for cron - consider external cron service

---

## Monitoring & Maintenance

### Railway Metrics:
- Monitor CPU, memory, and bandwidth usage
- View logs in real-time
- Set up alerts for downtime

### Database Management:
- Railway PostgreSQL has 500MB free tier
- Monitor database size: Service → PostgreSQL → "Metrics"
- Consider adding data retention policy if growing too fast

### Cost Optimization:
- Railway: $5/month for 500 hours (plenty for this app)
- Netlify: Free tier is sufficient (100GB bandwidth)
- **Total: ~$5-10/month**

---

## Optional: Custom Domain

### For Frontend (Netlify):
1. Go to Netlify site settings
2. **"Domain management"** → **"Add custom domain"**
3. Follow DNS setup instructions
4. Netlify provides free SSL automatically

### For Backend (Railway):
1. Railway service → **"Settings"** → **"Domains"**
2. Click **"+ Custom Domain"**
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS with CNAME record
5. Railway provides free SSL

---

## Next Steps

1. **Monitor First Run**: Wait for market hours and watch the first analysis run
2. **Check Data**: Verify database is populating with sentiment data
3. **Test All Features**: Test all 4 sentiment drivers, chart timeframes, etc.
4. **Set Up Alerts**: Configure Railway to notify you of downtime
5. **Backup Database**: Consider periodic backups via Railway

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Netlify Docs**: https://docs.netlify.com
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

## Summary

✅ **Backend**: Railway (Django + PostgreSQL + Cron)
✅ **Frontend**: Netlify (Static HTML)
✅ **Cron Job**: Runs every minute during market hours
✅ **Cost**: ~$5/month
✅ **SSL**: Free on both platforms

Your NASDAQ Sentiment Tracker is now live! 🚀
