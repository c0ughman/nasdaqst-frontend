# Railway Troubleshooting Guide

## Issue #1: Admin Dashboard Not Working (/admin shows no CSS)

### Problem
When visiting `https://your-app.railway.app/admin`, the page loads but has no styling (looks broken).

### Root Cause
Django admin needs static files (CSS/JS) to display correctly. WhiteNoise middleware was missing.

### Solution ✅ FIXED
I've added WhiteNoise middleware to serve static files in production.

**After pushing this fix to GitHub:**
1. Railway will auto-deploy
2. The `release` command in `Procfile` will run `collectstatic`
3. Admin will work with full styling

**To test after deployment:**
```
https://your-railway-url.up.railway.app/admin/
```

You should see the styled Django admin login page.

---

## Issue #2: Cron Job Not Running (No "Market Closed" Logs)

### Problem
Railway logs don't show the cron job running - no "Market Closed - Skipping Run" messages.

### Root Cause ✅ FOUND AND FIXED

**The cron schedule was configured to run every minute (`* * * * *`), but Railway requires a MINIMUM of 5 minutes between executions.**

Railway was silently rejecting the cron job because it violated the frequency limit.

### Solution ✅ FIXED
Changed cron schedule from `* * * * *` to `*/5 * * * *` (every 5 minutes).

After Railway redeploys, the cron job should run every 5 minutes.

#### Cause 2: Cron Service Not Created
Railway might need a **separate cron service** instead of running cron within the web service.

**Alternative Setup:**
1. In Railway project, click **"+ New"**
2. Select **"Empty Service"**
3. Connect to same GitHub repo
4. Set **root directory** to `backend`
5. Add environment variables (same as web service)
6. In service settings, set **"Start Command"**:
   ```
   python manage.py run_nasdaq_sentiment --once
   ```
7. Add cron schedule in Railway dashboard

#### Cause 3: `railway.json` Not Being Read
Railway might not be picking up the cron configuration from `railway.json`.

**Verify:**
1. Check Railway deployment logs
2. Look for mentions of "cron" or "railway.json"
3. If not mentioned, the file might not be in the right location

**Fix:**
- Make sure `railway.json` is in the `backend/` directory (it is!)
- Railway's root directory should be set to `backend`

---

## Alternative: External Cron Service (Free Workaround)

If Railway cron doesn't work or you want to avoid the $5/month fee:

### Option A: Cron-job.org (Free)

1. Sign up at https://cron-job.org
2. Create new cron job
3. Set URL: `https://your-railway-url.up.railway.app/api/trigger-analysis/`
   (You'll need to create this endpoint - see below)
4. Schedule: Every minute `* * * * *`

### Option B: GitHub Actions (Free, but limited)

GitHub Actions free tier allows:
- Workflows every 5 minutes minimum
- 2000 minutes/month

**Create `.github/workflows/cron.yml`:**
```yaml
name: Run Sentiment Analysis
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  run-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Analysis
        run: |
          curl -X POST https://your-railway-url.up.railway.app/api/trigger-analysis/ \
            -H "Authorization: Bearer ${{ secrets.CRON_TOKEN }}"
```

### Create Trigger Endpoint (If Using External Cron)

Add to `backend/api/views.py`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.management import call_command
import os

@api_view(['POST'])
def trigger_analysis(request):
    """Trigger sentiment analysis (for external cron services)"""
    # Simple token authentication
    auth_header = request.headers.get('Authorization', '')
    expected_token = os.environ.get('CRON_TOKEN', 'your-secret-token-here')

    if auth_header != f'Bearer {expected_token}':
        return Response({'error': 'Unauthorized'}, status=401)

    # Run the analysis command
    try:
        call_command('run_nasdaq_sentiment', '--once')
        return Response({'status': 'Analysis triggered successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
```

Add to `backend/api/urls.py`:
```python
path('trigger-analysis/', views.trigger_analysis, name='trigger-analysis'),
```

Set `CRON_TOKEN` in Railway environment variables.

---

## How to Check If Cron Is Actually Running

### Method 1: Railway Logs (Real-time)
1. Go to your Django service
2. Click **"Observability"** → **"Logs"**
3. Watch for logs appearing every minute
4. You should see (if market is closed):
   ```
   ⏸️  Market Closed - Skipping Run
   Reason: Market closed (outside trading hours: 8:30 AM - 4:00 PM CT)
   Current time: 2025-10-22 08:15:00 PM CDT
   ```

### Method 2: Check Database
Run this query in Railway PostgreSQL:

```sql
SELECT timestamp, composite_score
FROM api_analysisrun
ORDER BY timestamp DESC
LIMIT 10;
```

If cron is working during market hours, you'll see new entries every minute.

### Method 3: Test Endpoint
Create a test endpoint to manually trigger analysis:

```bash
# Using Railway CLI
railway run python manage.py run_nasdaq_sentiment --once

# Or via curl (if you create trigger endpoint)
curl -X POST https://your-railway-url.up.railway.app/api/trigger-analysis/ \
  -H "Authorization: Bearer your-token"
```

---

## Summary

### Admin Issue ✅ FIXED
- Added WhiteNoise middleware
- Added static files configuration
- Push to GitHub → Railway will auto-deploy

### Cron Issue - 3 Solutions:

1. **Easiest**: Upgrade to Railway Hobby plan ($5/month)
2. **Free Alternative**: Use cron-job.org + create trigger endpoint
3. **GitHub Actions**: Free but limited to every 5 minutes

---

## Next Steps

1. **Push the admin fix:**
   ```bash
   git push origin main
   ```

2. **Wait for Railway deployment** (~2-3 minutes)

3. **Test admin:**
   ```
   https://your-railway-url.up.railway.app/admin/
   ```

4. **For cron:**
   - Check if you're on Railway Hobby plan
   - If not, decide: upgrade or use external cron service

5. **Monitor logs** during market hours to verify cron works

Let me know which cron solution you prefer, and I can help set it up!
