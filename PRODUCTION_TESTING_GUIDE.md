# Production Testing & Troubleshooting Guide

## Current Status Analysis

### ✅ Backend (Railway) - RUNNING
- **Status**: API is live and responding
- **URL**: https://nasdaqsentimenttracker-production.up.railway.app
- **Health Check**: ✅ Working (`/api/health/` returns 200)
- **Problem**: Database is empty (no sentiment data)

### ❌ Frontend (Netlify) - OUTDATED
- **Status**: Website loads but shows no data
- **URL**: https://nasdaqsentimenttracker.netlify.app
- **Problem**: Still pointing to old ngrok URL, not Railway
- **Needs**: Git push to deploy updated code

---

## Fix Steps (Do These in Order)

### Step 1: Add Missing Railway Environment Variables

Go to Railway Dashboard → Your Project → Variables Tab → Add these:

```bash
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-generate-a-new-random-one-here
ALLOWED_HOSTS=nasdaqsentimenttracker-production.up.railway.app,.railway.app
FRONTEND_URLS=https://nasdaqsentimenttracker.netlify.app,https://*.netlify.app
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

**Generate a secure Django secret key:**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Remove this variable:**
- `USE_SQLITE` (Railway uses PostgreSQL, not SQLite)

After adding, Railway will auto-redeploy.

---

### Step 2: Push Frontend Changes to GitHub

Your local code has been updated but not deployed. Push it:

```bash
cd "/Users/coughman/Desktop/Nasdaq Sentiment Tracker"
git push origin main
```

This will trigger:
- ✅ Railway to redeploy backend (with new env vars)
- ✅ Netlify to redeploy frontend (with Railway URL)

---

### Step 3: Run Database Migrations on Railway

Railway should run migrations automatically on deploy, but you can verify:

**Option A: Check Railway Logs**
1. Go to Railway Dashboard
2. Click "Deployments" tab
3. Look for: "Running database migrations..."
4. Should see: "Operations to perform: ..."

**Option B: Run Manually via Railway CLI**
```bash
# Install Railway CLI if needed
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate
```

---

### Step 4: Populate Database with Sentiment Data

The database is empty. You need to run your first sentiment analysis.

**Using Railway CLI:**
```bash
railway run python manage.py run_nasdaq_sentiment --once
```

**Or SSH into Railway:**
```bash
railway shell
python manage.py run_nasdaq_sentiment --once
```

This will:
- Fetch news articles
- Analyze sentiment
- Fetch Reddit data
- Calculate technical indicators
- Save everything to PostgreSQL

**Expected**: Takes ~60 seconds, creates AnalysisRun #1

---

### Step 5: Verify Everything Works

#### Test Backend API:

```bash
# Health check
curl https://nasdaqsentimenttracker-production.up.railway.app/api/health/

# Should return:
# {"status":"ok","message":"API is running successfully"}

# Dashboard data (after running sentiment analysis)
curl https://nasdaqsentimenttracker-production.up.railway.app/api/dashboard/ | jq

# Should return JSON with composite_score, drivers, etc.
```

#### Test Frontend:

1. Visit: https://nasdaqsentimenttracker.netlify.app
2. Open Browser Console (F12)
3. Look for:
   - ✅ "✓ Dashboard data received: [score]"
   - ✅ No CORS errors
   - ✅ Sentiment score displays

#### Test CORS (from browser console on Netlify):

```javascript
fetch('https://nasdaqsentimenttracker-production.up.railway.app/api/health/')
  .then(r => r.json())
  .then(console.log)

// Should log: {status: "ok", message: "API is running successfully"}
// Should NOT show CORS error
```

---

## Testing Checklist

### Railway Backend Tests

- [ ] Health endpoint responds: `curl https://nasdaqsentimenttracker-production.up.railway.app/api/health/`
- [ ] Environment variables set (see Step 1)
- [ ] Database migrations completed (check logs)
- [ ] Sentiment analysis ran (populated data)
- [ ] Dashboard endpoint returns data: `/api/dashboard/`
- [ ] No 500 errors in Railway logs

### Netlify Frontend Tests

- [ ] Git changes pushed to GitHub
- [ ] Netlify auto-deployed (check Netlify dashboard)
- [ ] Page loads at https://nasdaqsentimenttracker.netlify.app
- [ ] Frontend points to Railway (not ngrok)
- [ ] Browser console shows API calls to Railway
- [ ] No CORS errors
- [ ] Sentiment data displays on dashboard

### Integration Tests

- [ ] Frontend fetches data from Railway successfully
- [ ] Charts render with real data
- [ ] Drivers section shows 5 components
- [ ] News feed populates (if implemented)
- [ ] Auto-refresh works (updates every 60s)

---

## Common Issues & Solutions

### Issue 1: "Not found" from /api/dashboard/

**Cause**: Database is empty
**Solution**: Run sentiment analysis (Step 4)
```bash
railway run python manage.py run_nasdaq_sentiment --once
```

### Issue 2: CORS Error in Browser Console

**Symptom**:
```
Access to fetch at 'https://...railway.app/api/...' from origin 'https://...netlify.app'
has been blocked by CORS policy
```

**Cause**: Missing `FRONTEND_URLS` in Railway
**Solution**: Add to Railway variables:
```bash
FRONTEND_URLS=https://nasdaqsentimenttracker.netlify.app,https://*.netlify.app
```

### Issue 3: Frontend Still Shows ngrok URL

**Cause**: Changes not deployed to Netlify
**Solution**:
```bash
git push origin main
```
Wait 1-2 minutes for Netlify to redeploy.

### Issue 4: Railway 500 Internal Server Error

**Cause**: Missing environment variables
**Solution**: Check Railway logs for specific error, ensure all variables from Step 1 are set

### Issue 5: "Disallowed Host" Error

**Cause**: Missing `ALLOWED_HOSTS`
**Solution**: Add to Railway:
```bash
ALLOWED_HOSTS=nasdaqsentimenttracker-production.up.railway.app,.railway.app
```

---

## Quick Diagnostic Commands

### Check if Backend is Up:
```bash
curl -I https://nasdaqsentimenttracker-production.up.railway.app/api/health/
# Should see: HTTP/2 200
```

### Check if Database Has Data:
```bash
curl https://nasdaqsentimenttracker-production.up.railway.app/api/dashboard/ | jq '.composite_score'
# Should show a number, not "Not found"
```

### Check Frontend API URL:
```bash
curl -s https://nasdaqsentimenttracker.netlify.app | grep -o "https://[^'\"]*railway[^'\"]*" | head -1
# Should show Railway URL
```

### View Railway Logs:
```bash
railway logs
# Shows real-time logs from backend
```

---

## Production Monitoring

### Railway Dashboard
- **Deployments**: Check build logs, deployment status
- **Metrics**: CPU, memory, request count
- **Logs**: Real-time application logs

### Netlify Dashboard
- **Deploys**: See build history, deploy logs
- **Analytics**: Traffic, bandwidth usage
- **Functions**: (not used in this project)

---

## After Everything Works

### Set Up Automated Sentiment Analysis

**Option 1: Railway Cron Job**
```bash
# Add to Railway as a scheduled job
python manage.py run_nasdaq_sentiment --once
# Schedule: Every hour during market hours
```

**Option 2: GitHub Actions**
Create `.github/workflows/sentiment-analysis.yml`

**Option 3: External Cron Service**
Use services like cron-job.org to hit a trigger endpoint

---

## Expected Results After All Fixes

✅ Railway backend responds to all endpoints
✅ PostgreSQL database contains sentiment data
✅ Netlify frontend loads and connects to Railway
✅ Dashboard shows real-time sentiment score
✅ Charts render with historical data
✅ No CORS errors in browser console
✅ Auto-refresh updates data every 60 seconds

---

## Need Help?

### Railway Logs
```bash
railway logs --json | jq
```

### Django Admin
Visit: https://nasdaqsentimenttracker-production.up.railway.app/admin/
(Create superuser first: `railway run python manage.py createsuperuser`)

### Database Query
```bash
railway run python manage.py shell
# Then in Python:
from api.models import AnalysisRun
print(AnalysisRun.objects.count())  # Should be > 0
```
