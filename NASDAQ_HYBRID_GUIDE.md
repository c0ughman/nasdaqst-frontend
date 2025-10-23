# NASDAQ Composite Sentiment Tracker - Hybrid Approach

## 🎯 Overview

This system tracks NASDAQ composite sentiment using a **hybrid approach**:
- **70% weight**: Top 20 NASDAQ stocks (by market cap)
- **30% weight**: General market news (macro events, Fed policy, geopolitical)

## 📊 What It Tracks

### Top 20 NASDAQ Stocks
1. Apple (AAPL) - 12.0%
2. Microsoft (MSFT) - 10.5%
3. NVIDIA (NVDA) - 8.5%
4. Alphabet (GOOGL) - 6.5%
5. Amazon (AMZN) - 6.0%
6. Meta (META) - 4.5%
7. Tesla (TSLA) - 4.0%
8. Broadcom (AVGO) - 3.5%
9. Costco (COST) - 3.0%
10. Netflix (NFLX) - 2.8%
11. ASML (ASML) - 2.7%
12. AMD (AMD) - 2.6%
13. Adobe (ADBE) - 2.5%
14. PepsiCo (PEP) - 2.4%
15. Cisco (CSCO) - 2.3%
16. T-Mobile (TMUS) - 2.2%
17. Intel (INTC) - 2.1%
18. Comcast (CMCSA) - 2.0%
19. Qualcomm (QCOM) - 1.9%
20. Intuit (INTU) - 1.8%

### Market News Categories
- Federal Reserve & monetary policy
- Economic indicators (CPI, jobs report, GDP)
- Geopolitical events
- Market structure (bond yields, volatility)
- Tech sector trends

## 🚀 Usage

### One-Time Analysis
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py run_nasdaq_sentiment --once
```

### Continuous Monitoring (5-minute intervals)
```bash
python manage.py run_nasdaq_sentiment --interval 300
```

### Custom Interval (e.g., 10 minutes)
```bash
python manage.py run_nasdaq_sentiment --interval 600
```

## 📈 How It Works

### Phase 1: Company News (70% weight)
1. Fetches news for all 20 tickers (with 0.5s rate limiting between requests)
2. Analyzes sentiment for each company's news
3. Weights each company's sentiment by market cap
4. Calculates weighted composite score

### Phase 2: Market News (30% weight)
1. Fetches general market news
2. Filters for market-moving keywords (Fed, inflation, tech sector, etc.)
3. Excludes opinion pieces and noise
4. Analyzes sentiment of relevant market news

### Phase 3: Final Composite
```
NASDAQ Sentiment = (Company News × 70%) + (Market News × 30%)
```

## 🗄️ Database Structure

### Key Models

**AnalysisRun**: Main composite sentiment score for NASDAQ
- `composite_score`: Final -100 to +100 sentiment score
- `sentiment_label`: BULLISH/BEARISH/NEUTRAL
- `stock_price`: NASDAQ index price (via QQQ)
- Component averages: base sentiment, surprise factor, novelty, etc.

**TickerContribution**: Individual stock contributions
- Shows how each of the 20 stocks contributed to composite
- Tracks sentiment, weight, and weighted contribution per stock

**NewsArticle**: All analyzed articles
- `article_type`: 'company' or 'market'
- Full sentiment breakdown
- Source, headline, summary, URL

## 📊 Viewing Results

### Django Admin
```bash
python manage.py createsuperuser  # If you haven't already
python manage.py runserver
```
Visit: http://localhost:8000/admin/

Navigate to:
- **Analysis Runs**: See all composite sentiment scores
- **Ticker Contributions**: See individual stock breakdowns
- **News Articles**: Browse all analyzed articles

### API Endpoints
The sentiment data is available via REST API at:
- `/api/sentiment/` - All analysis runs
- `/api/sentiment/latest/` - Most recent analysis
- `/api/tickers/` - All tracked tickers

## 🔧 Configuration

Edit `backend/api/management/commands/nasdaq_config.py` to customize:

### Adjust Company/Market Split
```python
SENTIMENT_WEIGHTS = {
    'company_news': 0.70,  # Increase for more company focus
    'market_news': 0.30,   # Increase for more macro focus
}
```

### Add/Remove Stocks
```python
NASDAQ_TOP_20 = {
    'AAPL': 0.120,
    # Add or remove tickers as needed
}
```

### Adjust Market Keywords
```python
MARKET_MOVING_KEYWORDS = [
    # Add keywords to filter market news
    'your custom keyword',
]
```

### Rate Limiting
```python
API_RATE_LIMIT_DELAY = 0.5  # Seconds between API requests
```

## 📈 Sentiment Score Interpretation

| Score Range | Label | Meaning |
|------------|-------|---------|
| +50 to +100 | Strongly Bullish 🚀 | Very positive sentiment, strong buy signals |
| +20 to +50 | Bullish 📈 | Positive sentiment, favorable conditions |
| -20 to +20 | Neutral ➡️ | Mixed signals, uncertain direction |
| -50 to -20 | Bearish 📉 | Negative sentiment, caution advised |
| -100 to -50 | Strongly Bearish 🔻 | Very negative sentiment, risk-off |

## 🔑 Required API Keys

Set these in your `.env` file:

```bash
FINNHUB_API_KEY=your_finnhub_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
```

Get API keys:
- Finnhub: https://finnhub.io/ (Free tier: 60 calls/minute)
- HuggingFace: https://huggingface.co/ (Free tier available)

## ⚠️ Rate Limits

**Finnhub Free Tier**:
- 60 API calls per minute
- With 20 stocks + 1 market news call = 21 calls per analysis
- Can run analysis ~3 times per minute maximum
- Recommended: 5-minute intervals (--interval 300)

**HuggingFace**:
- Free tier has generous limits
- Sentiment model may need 20s warm-up on first call

## 🐛 Troubleshooting

### "No news found for ticker"
- Stock might not have recent news in past 24 hours
- Check if ticker symbol is correct
- Finnhub may have limited coverage for some stocks

### "API rate limit exceeded"
- Increase `API_RATE_LIMIT_DELAY` in nasdaq_config.py
- Reduce analysis frequency (increase --interval)
- Consider upgrading to Finnhub paid plan

### "Model loading" messages
- HuggingFace model needs to warm up (20s wait)
- Normal on first API call
- Subsequent calls will be fast

## 📝 Next Steps

1. **Test the system**:
   ```bash
   python manage.py run_nasdaq_sentiment --once
   ```

2. **View results in admin**:
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/admin/
   ```

3. **Set up continuous monitoring**:
   ```bash
   python manage.py run_nasdaq_sentiment --interval 300
   ```

4. **Connect to frontend**:
   - Frontend will automatically display NASDAQ composite sentiment
   - Charts will show historical trends
   - Individual ticker contributions visible in detail view

## 🎨 Features

✅ **Market-cap weighted**: Accurately reflects NASDAQ composition
✅ **Hybrid approach**: Captures both company and macro drivers
✅ **Rate-limited**: Respects API limits
✅ **Deduplication**: Caches analyzed articles
✅ **Comprehensive scoring**: 5-factor sentiment analysis
✅ **Real-time updates**: Continuous monitoring mode
✅ **Database storage**: All data persisted for historical analysis
✅ **Admin interface**: Easy data exploration

---

**Happy tracking! 📊🚀**

