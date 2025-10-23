# Production Deployment Checklist

## What Was Fixed to Enable Smooth Deployment

### 1. Frontend Configuration ✅
- **Fixed**: Updated API URL from hardcoded ngrok to Railway production URL
- **File**: `frontend/nasdaq.html` line 1469
- **Old**: `https://be6c59a4b213.ngrok-free.app`
- **New**: `https://nasdaqsentimenttracker-production.up.railway.app/api`

### 2. Netlify Configuration ✅
- **Fixed**: Added `publish = "frontend"` to tell Netlify where to find files
- **File**: `netlify.toml`
- **Change**: Set publish directory to `frontend/` folder

### 3. Railway Environment Variables 📋
- **Action Needed**: Set all environment variables in Railway dashboard
- **Reference**: See `RAILWAY_ENV_VARIABLES.md` for complete list
- **Critical**: Set `DEBUG=False` for production

---

## Deployment Steps

### Railway (Backend)

#### Step 1: Set Environment Variables
Go to Railway dashboard and set these variables:

```bash
# Critical Production Settings
DEBUG=False
DJANGO_SECRET_KEY=<generate-new-secret-key>
ALLOWED_HOSTS=nasdaqsentimenttracker-production.up.railway.app,.railway.app

# CORS for Frontend
FRONTEND_URLS=https://nasdaqsentimenttracker.netlify.app,https://*.netlify.app

# API Keys (use your actual keys from .env file)
FINNHUB_API_KEY=your-finnhub-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key

# Reddit API (use your actual credentials from .env file)
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

#### Step 2: Deploy to Railway
```bash
# Commit your changes
git add .
git commit -m "Configure for production deployment"
git push origin main

# Railway will auto-deploy from GitHub
# Or manually trigger deployment in Railway dashboard
```

#### Step 3: Verify Backend
- Visit: `https://nasdaqsentimenttracker-production.up.railway.app/api/health/`
- Should return: `{"status": "ok", "message": "API is running successfully"}`

### Netlify (Frontend)

#### Step 1: Configure Build Settings
In Netlify dashboard, set:
- **Base directory**: Leave empty or set to `/`
- **Publish directory**: `frontend`
- **Build command**: Leave empty (no build needed)

#### Step 2: Deploy to Netlify
```bash
# Option 1: Auto-deploy from GitHub
# Just push to main branch

# Option 2: Manual deploy
# Drag and drop the 'frontend' folder to Netlify

git add .
git commit -m "Configure for production deployment"
git push origin main
```

#### Step 3: Verify Frontend
- Visit: `https://nasdaqsentimenttracker.netlify.app`
- Check browser console for API connection
- Should show: "✅ Dashboard data loaded successfully"

---

## Post-Deployment Verification

### 1. Check Backend Health
```bash
curl https://nasdaqsentimenttracker-production.up.railway.app/api/health/
```
Expected: `{"status": "ok", "message": "API is running successfully"}`

### 2. Check API Endpoints
```bash
# Dashboard endpoint
curl https://nasdaqsentimenttracker-production.up.railway.app/api/dashboard/

# Composite score
curl https://nasdaqsentimenttracker-production.up.railway.app/api/nasdaq/composite-score/
```

### 3. Check Frontend
1. Visit `https://nasdaqsentimenttracker.netlify.app`
2. Open browser console (F12)
3. Look for successful API calls
4. Verify data loads on dashboard

### 4. Test CORS
In browser console on Netlify site:
```javascript
fetch('https://nasdaqsentimenttracker-production.up.railway.app/api/health/')
  .then(r => r.json())
  .then(console.log)
```
Should NOT show CORS errors.

---

## Common Issues and Solutions

### Issue: CORS Error
**Symptom**: Frontend shows "CORS policy blocked" in console
**Solution**:
1. Check `FRONTEND_URLS` in Railway environment variables
2. Must include `https://nasdaqsentimenttracker.netlify.app`
3. Redeploy backend after changing

### Issue: 404 on Netlify
**Symptom**: "Page not found" on Netlify
**Solution**:
1. Check publish directory is set to `frontend`
2. Verify `frontend/nasdaq.html` exists in repo
3. Check `netlify.toml` has correct publish path

### Issue: Backend 500 Error
**Symptom**: API returns 500 Internal Server Error
**Solution**:
1. Check Railway logs for error details
2. Verify all environment variables are set
3. Check `DATABASE_URL` is auto-provided by Railway
4. Ensure migrations ran successfully

### Issue: No Data Showing
**Symptom**: Frontend loads but shows no sentiment data
**Solution**:
1. Run sentiment analysis on Railway:
   ```bash
   python manage.py run_nasdaq_sentiment --once
   ```
2. Check if database has data via Railway admin panel
3. Verify API returns data in browser

---

## Monitoring

### Railway Logs
View in Railway dashboard under **Deployments** → **Logs**

Watch for:
- ✅ "Running database migrations..."
- ✅ "Collecting static files..."
- ✅ "Starting Gunicorn server..."
- ❌ Any error messages

### Netlify Deploy Logs
View in Netlify dashboard under **Deploys**

Watch for:
- ✅ "Site is live"
- ❌ Any 404 or build errors

---

## What's Working Now

✅ **Backend (Django on Railway)**
- API endpoints configured correctly
- CORS setup for Netlify
- Static files served with WhiteNoise
- Database migrations on deploy
- Gunicorn production server

✅ **Frontend (HTML on Netlify)**
- Correct publish directory (`frontend/`)
- Points to Railway production API
- Falls back to localhost for development
- Security headers configured

✅ **Development Setup**
- Virtual environment in `backend/venv/`
- All dependencies installed
- Local testing works perfectly

---

## Next Steps After Deployment

1. **Run Initial Sentiment Analysis**
   ```bash
   # SSH into Railway or use Railway CLI
   python manage.py run_nasdaq_sentiment --once
   ```

2. **Set Up Cron Job** (Optional)
   - Use Railway Cron to run sentiment analysis hourly
   - See `RAILWAY_CRON_TEST.md` for instructions

3. **Monitor Performance**
   - Check Railway metrics for resource usage
   - Monitor API response times
   - Check Netlify analytics for traffic

4. **Backup Database** (If using PostgreSQL)
   - Railway provides automatic backups
   - Can also export manually via Railway CLI
