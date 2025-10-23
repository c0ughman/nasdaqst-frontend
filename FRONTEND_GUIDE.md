# 📊 Sentiment Dashboard Frontend

## Overview

A simple React interface to view sentiment analysis data for any ticker.

## Features

✅ **Current Score Display** - Shows latest sentiment score, stock price, and change percentage
✅ **Historical Data Table** - Row-by-row view of all analysis runs
✅ **5 Component Scores** - Displays all 5 sentiment factors for each run
✅ **Query Parameter Support** - Set ticker via URL: `?ticker=AAPL`
✅ **Real-time Data** - Fetches from Django REST API

## Starting the Application

### 1. Start Backend (if not running)
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```
Backend runs on: http://localhost:8000

### 2. Start Frontend
```bash
cd frontend
npm start
```
Frontend runs on: http://localhost:3000

## Usage

### Access via URL Query Parameter:
```
http://localhost:3000?ticker=AAPL
http://localhost:3000?ticker=TSLA
http://localhost:3000?ticker=NVDA
```

### Or use the search box:
1. Go to http://localhost:3000
2. Enter ticker symbol (e.g., AAPL)
3. Click "Search"

## API Endpoints

The frontend uses these API endpoints:

### Get Ticker Analysis
```
GET /api/ticker/<symbol>/
```

**Example:**
```bash
curl http://localhost:8000/api/ticker/AAPL/
```

**Response:**
```json
{
  "ticker": {
    "symbol": "AAPL",
    "company_name": "Apple Inc"
  },
  "current_score": {
    "composite_score": 15.99,
    "sentiment_label": "NEUTRAL",
    "stock_price": "252.29",
    "price_change_percent": 1.96,
    "timestamp": "2025-10-20T12:37:51Z"
  },
  "historical_runs": [
    {
      "id": 1,
      "timestamp": "2025-10-20T12:37:51Z",
      "composite_score": 15.99,
      "sentiment_label": "NEUTRAL",
      "stock_price": "252.29",
      "price_change_percent": 1.96,
      "avg_base_sentiment": 0.391,
      "avg_surprise_factor": 1.0,
      "avg_novelty": 1.0,
      "avg_source_credibility": 0.5,
      "avg_recency_weight": 0.162,
      "articles_analyzed": 14,
      "cached_articles": 0,
      "new_articles": 14
    }
  ],
  "total_runs": 1
}
```

### Get Available Tickers
```
GET /api/tickers/
```

## Dashboard Components

### 🎯 Current Score Card
Shows:
- Current composite sentiment score
- Sentiment label (Bullish/Bearish/Neutral)
- Stock price
- Price change percentage
- Last update timestamp

### 📊 Historical Table
Displays all analysis runs with:
- **Timestamp** - When analysis was run
- **Score** - Composite sentiment score
- **Sentiment** - Labeled sentiment
- **Stock Price** - Price at analysis time
- **Change %** - Price change percentage
- **The 5 Component Scores:**
  1. Base Sentiment
  2. Surprise Factor
  3. Novelty
  4. Source Credibility
  5. Recency Weight
- **Articles** - Number analyzed (with cached count)

## Running Analysis for New Tickers

To populate data for a new ticker:

```bash
cd backend
source venv/bin/activate
python manage.py run_sentiment_analysis --ticker TSLA --once
```

Then view in dashboard:
```
http://localhost:3000?ticker=TSLA
```

## Color Coding

Sentiment colors:
- 🟢 **Strongly Bullish** - Green (#22c55e)
- 🟢 **Bullish** - Light Green (#84cc16)
- 🟡 **Neutral** - Yellow (#eab308)
- 🟠 **Bearish** - Orange (#f97316)
- 🔴 **Strongly Bearish** - Red (#ef4444)

## Troubleshooting

### Frontend shows "Failed to fetch data"
- Make sure backend is running on port 8000
- Check CORS settings in Django

### "Ticker not found" error
- Run analysis first: `python manage.py run_sentiment_analysis --ticker <SYMBOL> --once`
- Check ticker exists in database

### Can't access frontend
- Make sure `npm install` was run in frontend directory
- Check port 3000 is not in use
- Restart with `npm start`

## File Structure

```
frontend/
├── src/
│   ├── SentimentDashboard.js     # Main dashboard component
│   ├── SentimentDashboard.css    # Dashboard styles
│   ├── App.js                     # App wrapper
│   ├── services/
│   │   └── api.js                 # Axios API client
│   └── ...
└── package.json

backend/
├── api/
│   ├── views.py                   # API endpoints
│   ├── serializers.py             # DRF serializers
│   ├── urls.py                    # API routing
│   └── ...
└── ...
```

## Development

### Add new API endpoint:
1. Add view function in `backend/api/views.py`
2. Add route in `backend/api/urls.py`
3. Update frontend API calls in `frontend/src/SentimentDashboard.js`

### Customize styling:
Edit `frontend/src/SentimentDashboard.css`

### Add new features:
Modify `frontend/src/SentimentDashboard.js`

## Examples

### View AAPL data:
```
http://localhost:3000?ticker=AAPL
```

### View TSLA data:
```
http://localhost:3000?ticker=TSLA
```

### API test:
```bash
# Get AAPL data
curl http://localhost:8000/api/ticker/AAPL/ | python3 -m json.tool

# Get all tickers
curl http://localhost:8000/api/tickers/ | python3 -m json.tool
```

## Next Steps

1. **Run analysis** for multiple tickers
2. **Access dashboard** via browser
3. **View historical data** row by row
4. **Monitor sentiment** over time

Enjoy tracking sentiment! 📊🚀

