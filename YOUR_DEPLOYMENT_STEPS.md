# Your Next Steps - Quick Reference

## ✅ What I've Done

I've prepared your codebase for deployment with **minimal, non-disruptive changes**:

### Files Created:
1. **`backend/Procfile`** - Tells Railway how to run your app
2. **`backend/runtime.txt`** - Specifies Python version
3. **`backend/railway.json`** - Configures cron job (every minute)
4. **`backend/.env.example`** - Template for environment variables
5. **`netlify.toml`** - Netlify configuration
6. **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide (read this!)

### Files Updated:
1. **`backend/requirements.txt`** - Added missing dependencies (yfinance, praw, pandas, numpy, pytz)
2. **`backend/config/settings.py`** - Made CORS settings environment-based (backward compatible)
3. **`nasdaq.html`** - Made API URL dynamic (localhost vs production)

### What's Safe:
- ✅ All changes are **backward compatible**
- ✅ Local development still works exactly the same
- ✅ No functionality was modified
- ✅ All changes committed to Git

---

## 🚀 Your Action Items

### 1. Push to GitHub (5 minutes)

```bash
cd "/Users/coughman/Desktop/Nasdaq Sentiment Tracker"
git push origin main
```

If you need to create a GitHub repository first:
1. Go to https://github.com/new
2. Create repository named: `nasdaq-sentiment-tracker`
3. Then run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-sentiment-tracker.git
git push -u origin main
```

---

### 2. Deploy Backend to Railway (10 minutes)

#### Quick Steps:
1. **Sign up**: Go to https://railway.app (sign in with GitHub)
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repo**: Choose `nasdaq-sentiment-tracker`
4. **Add Database**: In project, click "+ New" → "Database" → "PostgreSQL"
5. **Set Root Directory**:
   - Click Django service → "Settings"
   - Set "Root Directory" to: `backend`
6. **Add Environment Variables**: Click "Variables" tab, add these:

```bash
DJANGO_SECRET_KEY=<generate-new-random-string>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.up.railway.app
FRONTEND_URLS=https://your-app.netlify.app
FINNHUB_API_KEY=<your-key>
HUGGINGFACE_API_KEY=<your-key>
REDDIT_CLIENT_ID=<your-id>
REDDIT_CLIENT_SECRET=<your-secret>
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

**Generate Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

7. **Deploy**: Railway auto-deploys. Wait for green checkmark.
8. **Run Migrations**: In Railway CLI or dashboard:
```bash
python manage.py migrate
python manage.py createsuperuser
```

9. **Copy Your Railway URL**: You'll need it for step 3!
   - Example: `https://your-app.up.railway.app`

---

### 3. Update Frontend with Backend URL (2 minutes)

1. Open `nasdaq.html` in your editor
2. Find line 1465 (search for `REPLACE_WITH_YOUR_RAILWAY_URL`)
3. Replace with your Railway URL:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : 'https://your-app.up.railway.app/api';  // ← Your Railway URL here
```

4. Save and commit:
```bash
git add nasdaq.html
git commit -m "Update frontend with production backend URL"
git push
```

---

### 4. Deploy Frontend to Netlify (5 minutes)

#### Option A: Drag & Drop (Easiest)
1. Go to https://netlify.com and sign in
2. Click "Add new site" → "Deploy manually"
3. Drag and drop:
   - `nasdaq.html`
   - `netlify.toml`
4. Done! Netlify gives you a URL.

#### Option B: GitHub (Recommended)
1. Go to https://netlify.com and sign in
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub → select `nasdaq-sentiment-tracker`
4. Configure:
   - Base directory: (leave empty)
   - Build command: (leave empty)
   - Publish directory: `.`
5. Click "Deploy site"
6. Copy your Netlify URL (e.g., `https://random-name.netlify.app`)

---

### 5. Update Backend CORS (2 minutes)

1. Go back to Railway
2. Click your Django service → "Variables"
3. Update `FRONTEND_URLS` to your Netlify URL:
```
FRONTEND_URLS=https://your-app.netlify.app
```
4. Railway auto-redeploys

---

### 6. Test Everything! (5 minutes)

#### Test Backend:
```bash
# Health check
curl https://your-app.up.railway.app/api/health/

# Dashboard data
curl https://your-app.up.railway.app/api/dashboard/
```

#### Test Frontend:
Visit: `https://your-app.netlify.app`

Check for:
- [ ] Composite score displays
- [ ] 4 driver cards show (News 35%, Social 20%, Technical 25%, Analyst 20%)
- [ ] Chart loads historical data
- [ ] Market status banner appears

---

## 📋 Troubleshooting Checklist

### Backend not working?
- [ ] Check Railway logs (Service → "Logs")
- [ ] Verify all environment variables are set
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check ROOT_DIRECTORY is set to `backend`

### Frontend can't connect?
- [ ] Verify Railway URL in `nasdaq.html` is correct
- [ ] Check CORS: `FRONTEND_URLS` matches Netlify URL
- [ ] Open browser console (F12) for errors

### Cron job not running?
- [ ] Check Railway logs during market hours
- [ ] Verify `railway.json` is in `backend/` folder
- [ ] May require Railway Pro plan ($5/month)

---

## 💰 Expected Costs

- **Railway**: $5/month (Hobby plan, 500 hours)
- **Netlify**: Free (100GB bandwidth)
- **Total**: ~$5/month

---

## 📚 Full Documentation

For detailed instructions, troubleshooting, and advanced configuration:
👉 **Read: `DEPLOYMENT_GUIDE.md`**

---

## 🎯 Summary

1. ✅ Push code to GitHub
2. ✅ Deploy backend on Railway
3. ✅ Update `nasdaq.html` with Railway URL
4. ✅ Deploy frontend on Netlify
5. ✅ Update Railway CORS with Netlify URL
6. ✅ Test both frontend and backend

**Total Time**: ~30 minutes
**Result**: Production-ready NASDAQ Sentiment Tracker! 🚀

---

## Need Help?

- **Railway Docs**: https://docs.railway.app
- **Netlify Docs**: https://docs.netlify.com
- **Full Guide**: `DEPLOYMENT_GUIDE.md` (in this folder)
