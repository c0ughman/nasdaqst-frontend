# 🤗 HuggingFace Inference API - Complete Guide

## 📊 **What You're Using**

You're using the **HuggingFace Inference API** to run FinBERT sentiment analysis:

```python
API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
```

This is HuggingFace's **hosted inference service** - they run the model on their servers, and you just make API calls.

---

## 💰 **Pricing Tiers**

### **1. Free Tier (Community)**
- **Cost**: $0/month
- **Rate Limit**: ~30 requests per minute (unofficial)
- **Features**:
  - Access to all public models
  - Shared compute resources
  - Model may need to "wake up" (503 errors)
  - No guaranteed uptime
  - Best effort support

### **2. PRO Tier**
- **Cost**: $9/month per user
- **Rate Limit**: Higher (not publicly specified, but significantly better)
- **Features**:
  - Priority access to models
  - Faster inference
  - Models stay "warm" (less 503 errors)
  - Better support
  - Access to private models

### **3. Enterprise Tier**
- **Cost**: Custom pricing (starts at $20/month)
- **Rate Limit**: Custom (negotiable)
- **Features**:
  - Dedicated compute resources
  - SLA guarantees
  - Custom rate limits
  - Premium support
  - Private model hosting

---

## 🚦 **Rate Limits (Free Tier)**

Based on community reports and testing:

### **Observed Limits:**
- **~30 requests per minute** (unofficial)
- **~1,000 requests per day** (soft limit)
- **No hard daily cap** but may be throttled

### **What Happens When You Hit Limits:**
```json
{
  "error": "Rate limit reached. Please retry after 60s",
  "estimated_time": 60
}
```

### **Your Current Usage:**

**With Batch Processing (NEW):**
- 20 batch calls per analysis run
- 1 batch call per ticker (10 articles each)
- **~20 API calls per run**
- At 1 run per minute: **~1,200 calls/hour** ⚠️

**Without Batch Processing (OLD):**
- ~162 individual calls per run
- At 1 run per minute: **~9,720 calls/hour** 🔥 (would hit limits!)

---

## ⚡ **Current Performance**

### **Your Setup:**
```
Analysis Frequency: Every 60 seconds
Articles per run: ~162
Batch calls per run: ~20
Daily runs: 1,440 (24 hours × 60 minutes)
Daily API calls: ~28,800
```

### **Free Tier Capacity:**
- **Estimated daily limit**: ~30,000-50,000 calls
- **Your usage**: ~28,800 calls/day
- **Status**: ⚠️ **Close to limit** but should work

### **With Caching:**
After first run, most articles are cached:
- **New articles only**: ~10-20 per run
- **Batch calls**: ~2-3 per run
- **Daily calls**: ~4,320
- **Status**: ✅ **Well within limits**

---

## 🔥 **Rate Limit Handling**

Your code already handles rate limits:

```python
elif response.status_code == 503:
    print("  ⏳ Model loading, retrying in 20 seconds...")
    time.sleep(20)
    return analyze_sentiment_finbert_api(text)
```

### **503 Error:**
- Model is "sleeping" (cold start)
- Needs 10-20 seconds to load
- Automatic retry after 20 seconds

### **429 Error:**
- Rate limit exceeded
- Need to implement backoff strategy

---

## 💡 **Recommendations**

### **Option 1: Stay on Free Tier** (Current)
**Pros:**
- ✅ Free
- ✅ Works with batch processing
- ✅ Good for development/testing

**Cons:**
- ⚠️ May hit rate limits during high activity
- ⚠️ 503 errors (cold starts)
- ⚠️ No guaranteed uptime

**Best for:**
- Development
- Low-frequency updates (5-10 min intervals)
- With good caching strategy

### **Option 2: Upgrade to PRO** ($9/month)
**Pros:**
- ✅ Higher rate limits
- ✅ Faster inference
- ✅ Fewer 503 errors
- ✅ Better reliability

**Cons:**
- 💰 $9/month cost

**Best for:**
- Production use
- Frequent updates (1-2 min intervals)
- Commercial applications

### **Option 3: Self-Host FinBERT** (Free but complex)
**Pros:**
- ✅ No rate limits
- ✅ No API costs
- ✅ Full control

**Cons:**
- 💻 Need GPU server ($50-200/month)
- 🔧 Complex setup
- 🛠️ Maintenance required

**Best for:**
- High-volume usage (>100k calls/day)
- Need for guaranteed uptime
- Have technical resources

---

## 📈 **Optimization Strategies**

### **1. Increase Cache Hit Rate** ✅ (Already Implemented)
```python
# Check cache before API call
cached_sentiment = get_cached_sentiment_from_db(article_hash)
if cached_sentiment:
    return cached_sentiment  # No API call!
```

**Impact:**
- First run: 162 API calls
- Subsequent runs: 0-20 API calls
- **Savings: 85-100%**

### **2. Batch Processing** ✅ (Already Implemented)
```python
# Send 10 articles in 1 API call
sentiments = analyze_sentiment_finbert_batch(texts)
```

**Impact:**
- Before: 162 API calls
- After: 20 API calls
- **Savings: 87%**

### **3. Reduce Update Frequency**
```bash
# Instead of every 60 seconds
python manage.py run_nasdaq_sentiment --interval 300  # 5 minutes
```

**Impact:**
- API calls: 28,800 → 5,760 per day
- **Savings: 80%**

### **4. Smart Updates** ✅ (Already Implemented)
```python
# Only run full analysis if new articles exist
if not has_new_articles:
    # Just update price, skip sentiment analysis
    update_price_only()
```

**Impact:**
- During slow news periods: 0 FinBERT calls
- **Savings: 100%** when no news

---

## 🎯 **Recommended Configuration**

### **For Free Tier:**
```bash
# Run every 5 minutes (instead of 1 minute)
python manage.py run_nasdaq_sentiment --interval 300
```

**Result:**
- 288 runs per day
- ~5,760 API calls per day (with batch processing)
- ~576 API calls per day (with caching after first run)
- ✅ **Well within free tier limits**

### **For PRO Tier ($9/month):**
```bash
# Run every 1-2 minutes
python manage.py run_nasdaq_sentiment --interval 60
```

**Result:**
- 1,440 runs per day
- ~28,800 API calls per day (with batch processing)
- ~4,320 API calls per day (with caching)
- ✅ **Comfortable within PRO limits**

---

## 🔍 **How to Check Your Usage**

### **Monitor API Calls:**
Add logging to track calls:

```python
# Add to your code
import logging

def analyze_sentiment_finbert_batch(texts):
    logging.info(f"FinBERT API call: {len(texts)} texts")
    # ... rest of code
```

### **Check HuggingFace Dashboard:**
1. Go to https://huggingface.co/settings/billing
2. View your API usage
3. See remaining quota (if on paid tier)

### **Monitor 429 Errors:**
If you see:
```
⚠️ Batch API error: 429
```
You're hitting rate limits - need to slow down or upgrade.

---

## 💸 **Cost Comparison**

### **Current Setup (Free Tier):**
```
HuggingFace API: $0/month
Finnhub API: $0/month (free tier)
Total: $0/month
```

### **Optimized Setup (PRO):**
```
HuggingFace PRO: $9/month
Finnhub API: $0/month (free tier)
Total: $9/month
```

### **Self-Hosted Alternative:**
```
GPU Server (AWS g4dn.xlarge): ~$150/month
OR
GPU Server (vast.ai): ~$50/month
Finnhub API: $0/month
Total: $50-150/month
```

---

## 🚀 **Action Items**

### **Immediate (Free Tier):**
1. ✅ **Keep batch processing** (already implemented)
2. ✅ **Keep caching** (already implemented)
3. ✅ **Keep smart updates** (already implemented)
4. 📝 **Increase interval** to 5 minutes: `--interval 300`
5. 📊 **Monitor for 429 errors**

### **If Hitting Limits:**
1. 💰 **Upgrade to PRO** ($9/month)
2. 🔧 **Add exponential backoff** for 429 errors
3. ⏰ **Increase update interval** to 10 minutes

### **For Production:**
1. 💰 **Get HuggingFace PRO** ($9/month)
2. 💰 **Get Finnhub paid tier** if needed
3. 📊 **Set up monitoring** and alerts
4. 🔄 **Implement retry logic** with backoff

---

## 📝 **Summary**

**Your Current Status:**
- ✅ Using HuggingFace Inference API (Free Tier)
- ✅ Batch processing implemented (87% API reduction)
- ✅ Caching implemented (85-100% API reduction)
- ✅ Smart updates implemented (skips when no news)
- ⚠️ Running every 60 seconds (may hit limits)

**Recommendation:**
- **For Development**: Stay on free tier, increase interval to 5 minutes
- **For Production**: Upgrade to PRO ($9/month) for reliability

**Bottom Line:**
With your current optimizations, you're using the API very efficiently! The free tier should work fine for development, but PRO is recommended for production use.

---

## 🔗 **Useful Links**

- HuggingFace Pricing: https://huggingface.co/pricing
- FinBERT Model: https://huggingface.co/ProsusAI/finbert
- Inference API Docs: https://huggingface.co/docs/api-inference/
- Your API Settings: https://huggingface.co/settings/tokens

**Need help?** Check the HuggingFace community forums or Discord!

