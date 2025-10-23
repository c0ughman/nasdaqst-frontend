# NASDAQ Sentiment Tracker - Quick Start

## 🚀 Get Started in 3 Steps

### Step 1: Run the Analysis

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py run_nasdaq_sentiment --once
```

**What happens:**
- Fetches news for top 20 NASDAQ stocks (Apple, Microsoft, NVIDIA, etc.)
- Fetches general market news (Fed, inflation, geopolitical)
- Analyzes sentiment using AI
- Calculates weighted NASDAQ composite score
- Saves everything to database

**Expected time:** 1-2 minutes for complete analysis

### Step 2: View Results

Start the Django server:
```bash
python manage.py runserver
```

Visit the admin interface:
- URL: http://localhost:8000/admin/
- Login with your superuser credentials
- Navigate to "Analysis Runs" to see NASDAQ sentiment scores
- Navigate to "Ticker Contributions" to see individual stock breakdowns

### Step 3: Set Up Continuous Monitoring

Run every 5 minutes:
```bash
python manage.py run_nasdaq_sentiment --interval 300
```

**Press Ctrl+C to stop.**

---

## 📊 Understanding the Output

### Example Output:
```
🎯 FINAL NASDAQ COMPOSITE SENTIMENT SCORE: +45.67

   Company News Contribution: +52.38 (70%)
   Market News Contribution:  +23.45 (30%)

Current NASDAQ Sentiment: BULLISH 📈
Score: +45.67/100
```

### Score Interpretation:
- **+50 to +100**: Strongly Bullish 🚀 (Very positive)
- **+20 to +50**: Bullish 📈 (Positive)
- **-20 to +20**: Neutral ➡️ (Mixed signals)
- **-50 to -20**: Bearish 📉 (Negative)
- **-100 to -50**: Strongly Bearish 🔻 (Very negative)

---

## 🔍 What's Being Tracked

### Top 20 NASDAQ Stocks (70% weight)
1. AAPL - Apple (12.0%)
2. MSFT - Microsoft (10.5%)
3. NVDA - NVIDIA (8.5%)
4. GOOGL - Alphabet (6.5%)
5. AMZN - Amazon (6.0%)
6. META - Meta Platforms (4.5%)
7. TSLA - Tesla (4.0%)
8. + 13 more...

### General Market News (30% weight)
- Federal Reserve policy & interest rates
- Inflation data (CPI, PPI)
- Jobs reports & unemployment
- Geopolitical events
- Tech sector trends
- Market volatility (VIX, Treasury yields)

---

## ⚙️ Configuration

### Change Update Frequency

**More frequent** (2 minutes - minimum):
```bash
python manage.py run_nasdaq_sentiment --interval 120
```

**Less frequent** (10 minutes - conservative):
```bash
python manage.py run_nasdaq_sentiment --interval 600
```

### Adjust Company/Market Split

Edit `backend/api/management/commands/nasdaq_config.py`:

```python
SENTIMENT_WEIGHTS = {
    'company_news': 0.70,  # Increase for more company focus
    'market_news': 0.30,   # Increase for more macro focus
}
```

---

## 🐛 Troubleshooting

### "API key not set"
Make sure `backend/.env` has:
```
FINNHUB_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here
```

### "No news found"
- Normal for some tickers without recent news
- Analysis will continue with available data

### "Model loading" (20s wait)
- First HuggingFace API call needs model warm-up
- Only happens once per session
- Subsequent calls are fast

### "Rate limit exceeded"
- Wait 1 minute and try again
- Increase interval between analyses
- Consider Finnhub paid plan for higher limits

---

## 📖 Documentation

- **Full Guide**: See `NASDAQ_HYBRID_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Project README**: See `README.md`

---

## ✅ System Status

- ✅ Database migrated and ready
- ✅ Top 20 NASDAQ stocks configured
- ✅ Hybrid analysis (70/30 split) implemented
- ✅ Rate limiting configured (0.5s between calls)
- ✅ API keys validated
- ✅ Admin interface ready
- ✅ Command line tool ready

**You're all set! Run the analysis and start tracking NASDAQ sentiment! 🚀📊**

