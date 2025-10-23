# Railway Environment Variables Configuration

## Required Environment Variables for Production Deployment

Configure these environment variables in your Railway dashboard under **Variables** tab.

### Django Settings

```bash
# Django secret key - GENERATE A NEW ONE FOR PRODUCTION
# Use: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
DJANGO_SECRET_KEY=your-super-secret-key-here-generate-a-new-one

# Debug mode - MUST be False for production
DEBUG=False

# Allowed hosts - add your Railway domain
ALLOWED_HOSTS=nasdaqsentimenttracker-production.up.railway.app,.railway.app,localhost,127.0.0.1

# Frontend URLs for CORS - add your Netlify URL
FRONTEND_URLS=https://nasdaqsentimenttracker.netlify.app,https://*.netlify.app
```

### API Keys

```bash
# Finnhub API Key (for stock data and news)
FINNHUB_API_KEY=your-finnhub-api-key-here

# HuggingFace API Key (for sentiment analysis)
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Alpha Vantage API Key (for stock data)
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key-here
```

### Reddit API Credentials

```bash
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password
REDDIT_USER_AGENT=NASDAQ_Sentiment_Tracker/1.0
```

### Database Settings

```bash
# Railway automatically provides DATABASE_URL
# No need to set this manually - Railway will inject it
# DATABASE_URL=postgresql://...
```

### Port Settings

```bash
# Railway automatically provides PORT
# No need to set this manually - Railway will inject it
# PORT=8000
```

## How to Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your backend service
3. Navigate to the **Variables** tab
4. Click **+ New Variable**
5. Add each variable listed above
6. Click **Deploy** to apply changes

## Security Notes

⚠️ **IMPORTANT**:
- Never commit these values to Git
- Generate a new `DJANGO_SECRET_KEY` for production
- Rotate API keys if they've been exposed
- Keep `DEBUG=False` in production

## Verification

After setting all variables, check the deployment logs to ensure:
1. Migrations run successfully
2. Static files are collected
3. Gunicorn starts without errors
4. No missing environment variable warnings

## Netlify Configuration

No environment variables needed for Netlify - the frontend is static HTML.

Just ensure the **Publish directory** is set to `frontend` in Netlify build settings.
