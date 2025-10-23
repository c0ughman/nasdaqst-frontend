# Railway Setup Guide - Step by Step

## Quick Reference

Your codebase is now pushed to GitHub and ready for Railway deployment!

**GitHub Repo**: `https://github.com/c0ughman/nasdaqsentimenttracker`
**Netlify URL**: `https://nasdaqsentimenttracker.netlify.app`

---

## Step 1: Find Your Railway URL (Where is it?)

After you deploy to Railway, you'll find your URL here:

### Option A: In the Deployment View
1. Go to your Railway project
2. Click on your **Django service** (not PostgreSQL)
3. Look at the top - you'll see a **domain** like:
   ```
   nasdaq-sentiment-production.up.railway.app
   ```
4. Your full API URL will be:
   ```
   https://nasdaq-sentiment-production.up.railway.app/api
   ```

### Option B: In Settings
1. Click your Django service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. You'll see: `nasdaq-sentiment-production.up.railway.app`
5. **Copy this URL** - you'll need it!

---

## Step 2: Set Up PostgreSQL Database

### Add PostgreSQL to Your Project

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway automatically:
   - Creates a PostgreSQL database
   - Sets the `DATABASE_URL` environment variable
   - Links it to your Django service

### Verify Database Connection

1. Click on the PostgreSQL service
2. Go to **"Variables"** tab
3. You should see `DATABASE_URL` - this is auto-injected into your Django app!

**No additional configuration needed** - Django will use this automatically.

---

## Step 3: Run Database Migrations

You have 3 options to run migrations:

### Option A: Using Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

### Option B: Using Railway Dashboard

1. Go to your Django service
2. Click **"Settings"** tab
3. Find **"Deploy Command"** or use the shell
4. Run commands one at a time:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Option C: One-Time Deploy Command

Railway automatically runs migrations via the `Procfile`:
```
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

This runs **automatically on every deployment**!

---

## Step 4: Set Up Scheduled Task (Cron Job)

Your `railway.json` file already configures the cron job! It's set to run every minute:

```json
{
  "deploy": {
    "cron": [
      {
        "name": "nasdaq-sentiment-analysis",
        "schedule": "* * * * *",
        "command": "python manage.py run_nasdaq_sentiment --once"
      }
    ]
  }
}
```

### Verify Cron is Running

1. Go to your Django service in Railway
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. Go to **"Logs"** tab
5. Wait 1-2 minutes (during market hours)
6. You should see logs like:

**If Market is Closed:**
```
⏸️  Market Closed - Skipping Run
   Reason: Market closed (outside trading hours: 8:30 AM - 4:00 PM CT)
```

**If Market is Open:**
```
🚀 NASDAQ Composite Sentiment Tracker - Hybrid Approach
📊 Tracking 20 top NASDAQ stocks
```

### If Cron Doesn't Work

Railway's cron feature requires the **Hobby plan ($5/month)**. If it doesn't work:

**Alternative: Use External Cron Service**

1. Sign up at https://cron-job.org (free)
2. Create new cron job
3. Set URL to: `https://your-railway-url.up.railway.app/api/health/`
4. Schedule: Every minute `* * * * *`

(Note: You may need to create a trigger endpoint if you want it to actually run the analysis)

---

## Step 5: Configure Environment Variables

In Railway, click your Django service → **"Variables"** tab, and add:

### Required Variables:

```bash
# Django Settings
DJANGO_SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app
FRONTEND_URLS=https://nasdaqsentimenttracker.netlify.app

# API Keys
FINNHUB_API_KEY=<your-finnhub-key>
HUGGINGFACE_API_KEY=<your-huggingface-key>

# Reddit API
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_CLIENT_SECRET=<your-reddit-client-secret>
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

### Generate Django Secret Key

Run this locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `DJANGO_SECRET_KEY` in Railway.

### Replace Placeholders

- `your-app-name.up.railway.app` - Your actual Railway domain
- `<your-finnhub-key>` - Your Finnhub API key
- `<your-huggingface-key>` - Your HuggingFace API key
- `<your-reddit-*>` - Your Reddit API credentials

---

## Step 6: Update Frontend with Railway URL

Once you have your Railway URL, update the frontend:

1. Open `nasdaq.html` in your editor
2. Find line ~1475 (search for `YOUR_RAILWAY_URL`)
3. Replace with your actual Railway URL:

```javascript
const API_BASE_URL = (
    window.location.protocol === 'file:' ||
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname === ''
) ? 'http://localhost:8000/api'
  : 'https://your-app-name.up.railway.app/api';  // ← Your Railway URL here
```

4. **Important**: Include `/api` at the end!
5. Save and redeploy to Netlify (or push to GitHub if using Git integration)

---

## Step 7: Test Everything

### Test Backend API

```bash
# Health check
curl https://your-app-name.up.railway.app/api/health/

# Expected output:
{"status":"ok","message":"API is running successfully"}

# Dashboard data
curl https://your-app-name.up.railway.app/api/dashboard/

# Should return JSON with composite_score, drivers, etc.
```

### Test Frontend

Visit: `https://nasdaqsentimenttracker.netlify.app`

Check for:
- [ ] Composite sentiment score displays
- [ ] 4 driver cards show (News 35%, Social 20%, Technical 25%, Analyst 20%)
- [ ] Chart loads historical data
- [ ] Market status banner shows (green/red)
- [ ] No CORS errors in browser console (F12)

---

## Troubleshooting

### "Application Error" on Railway

**Check logs:**
1. Django service → "Logs" tab
2. Look for errors related to:
   - Missing environment variables
   - Database connection issues
   - Missing migrations

**Fix:**
```bash
railway run python manage.py migrate
```

### CORS Errors on Frontend

**Verify:**
1. `FRONTEND_URLS` in Railway matches your Netlify URL exactly
2. Railway has redeployed after changing env vars
3. No typos in the URL

### Cron Job Not Running

**Check:**
1. Railway logs during market hours
2. Verify `railway.json` is in `backend/` directory
3. May require Railway Hobby plan ($5/month)

### Database Not Populating

**During market hours:**
1. Check Railway logs for analysis runs
2. Verify API keys are set correctly
3. Check PostgreSQL data: Service → PostgreSQL → "Data" tab

**After market hours:**
- This is normal! Script exits with "Market Closed - Skipping Run"

---

## Summary Checklist

- [ ] PostgreSQL database added to Railway project
- [ ] All environment variables configured
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Railway URL copied
- [ ] Frontend updated with Railway URL
- [ ] Frontend redeployed to Netlify
- [ ] Backend CORS updated with Netlify URL
- [ ] API health check passes
- [ ] Frontend connects to backend successfully
- [ ] Cron job running (check logs)

---

## Expected Costs

- **Railway Hobby**: $5/month (500 hours, more than enough)
- **PostgreSQL**: Included with Railway
- **Netlify**: Free tier
- **Total**: $5/month

---

## Next Steps

1. **Monitor First Run**: Wait for market hours and watch the logs
2. **Verify Data**: Check PostgreSQL to see sentiment data populating
3. **Test Dashboard**: Visit Netlify URL and verify everything works
4. **Set Up Alerts**: Configure Railway to email you if service goes down

Your NASDAQ Sentiment Tracker is now live! 🚀
