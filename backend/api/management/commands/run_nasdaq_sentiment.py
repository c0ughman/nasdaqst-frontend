"""
NASDAQ Composite Sentiment Tracker - Hybrid Approach
Tracks sentiment across top 20 NASDAQ stocks + general market news
Run with: python manage.py run_nasdaq_sentiment
"""

import os
import time
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Avg, Min, Max, Count, Sum
from django.db import transaction
import requests
import finnhub
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))

# Import models
from api.models import Ticker, AnalysisRun, NewsArticle, SentimentHistory, TickerContribution

# Import NASDAQ configuration
from .nasdaq_config import (
    NASDAQ_TOP_20,
    COMPANY_NAMES,
    MARKET_MOVING_KEYWORDS,
    EXCLUDE_KEYWORDS,
    SOURCE_CREDIBILITY,
    SENTIMENT_WEIGHTS,
    API_RATE_LIMIT_DELAY,
    INDICATOR_SYMBOLS,
    INDICATOR_RESOLUTION,
    INDICATOR_LOOKBACK_HOURS,
    INDICATOR_PERIODS,
)

# Import technical indicators calculator (uses Yahoo Finance OHLCV + math)
from .technical_indicators import fetch_indicators_with_fallback, fetch_latest_ohlcv_from_yfinance, calculate_technical_composite_score

# Import Reddit sentiment analysis
from .reddit_fetcher import fetch_all_reddit_content
from .reddit_sentiment_analyzer import analyze_reddit_content_batch

# Import market hours checker
from api.utils.market_hours import is_market_open, get_market_status

# ============================================================================
# CONFIGURATION
# ============================================================================

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY', '')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')

# Weights for composite score calculation (within each article)
ARTICLE_WEIGHTS = {
    'base_sentiment': 0.40,
    'surprise_factor': 0.25,
    'novelty': 0.15,
    'source_credibility': 0.10,
    'recency': 0.10
}

# Cache to track seen articles in current session
seen_articles = set()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_article_hash(headline, summary):
    """Generate unique hash for article deduplication"""
    content = f"{headline}{summary}".lower()
    return hashlib.md5(content.encode()).hexdigest()


def get_cached_sentiment_from_db(article_hash):
    """Get cached sentiment from database"""
    try:
        article = NewsArticle.objects.filter(article_hash=article_hash).first()
        if article and article.is_analyzed:
            return article.base_sentiment
    except Exception as e:
        print(f"⚠️ Error fetching cached sentiment: {e}")
    return None


def analyze_sentiment_finbert_api(text):
    """Analyze sentiment using FinBERT via HuggingFace API (single text)"""
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    text = text[:512]
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        if response.status_code == 200:
            result = response.json()
            sentiment_map = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            for item in result[0]:
                label = item['label'].lower()
                score = item['score']
                sentiment_map[label] = score
            
            sentiment_score = sentiment_map['positive'] - sentiment_map['negative']
            return sentiment_score
            
        elif response.status_code == 503:
            print("  ⏳ Model loading, retrying in 20 seconds...")
            time.sleep(20)
            return analyze_sentiment_finbert_api(text)
        else:
            print(f"  ⚠️ API error: {response.status_code}")
            return 0.0
            
    except Exception as e:
        print(f"  ⚠️ Error analyzing sentiment: {e}")
        return 0.0


def analyze_sentiment_finbert_batch(texts):
    """
    Analyze sentiment for multiple texts in a single batch API call
    Returns: list of sentiment scores in same order as input texts
    """
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Truncate each text to 512 characters
    truncated_texts = [text[:512] for text in texts]
    
    try:
        # Send batch request
        response = requests.post(API_URL, headers=headers, json={"inputs": truncated_texts})
        
        if response.status_code == 200:
            results = response.json()
            sentiment_scores = []
            
            # Process each result
            for result in results:
                sentiment_map = {'positive': 0, 'negative': 0, 'neutral': 0}
                
                for item in result:
                    label = item['label'].lower()
                    score = item['score']
                    sentiment_map[label] = score
                
                sentiment_score = sentiment_map['positive'] - sentiment_map['negative']
                sentiment_scores.append(sentiment_score)
            
            return sentiment_scores
            
        elif response.status_code == 503:
            print("  ⏳ Model loading, retrying in 20 seconds...")
            time.sleep(20)
            return analyze_sentiment_finbert_batch(texts)
        else:
            print(f"  ⚠️ Batch API error: {response.status_code}")
            # Return zeros for all texts
            return [0.0] * len(texts)
            
    except Exception as e:
        print(f"  ⚠️ Error in batch sentiment analysis: {e}")
        return [0.0] * len(texts)


def calculate_surprise_factor(text):
    """Detect if news is surprising/unexpected"""
    text_lower = text.lower()
    
    surprise_keywords = {
        'unexpected': 1.5, 'surprise': 1.5, 'beats expectations': 1.8,
        'misses estimates': 1.8, 'exceeds expectations': 1.8, 'shock': 2.0,
        'unprecedented': 1.7, 'sudden': 1.4, 'abrupt': 1.4, 'breaking': 1.3
    }
    
    expected_keywords = {
        'as expected': 0.4, 'in line with': 0.4, 'anticipated': 0.5,
        'scheduled': 0.6, 'planned': 0.6
    }
    
    multiplier = 1.0
    for keyword, weight in surprise_keywords.items():
        if keyword in text_lower:
            multiplier = max(multiplier, weight)
    for keyword, weight in expected_keywords.items():
        if keyword in text_lower:
            multiplier = min(multiplier, weight)
    
    return multiplier


def calculate_novelty(article_hash):
    """Check if article is novel or duplicate"""
    if article_hash in seen_articles:
        return 0.2
    seen_articles.add(article_hash)
    return 1.0


def get_source_credibility(source):
    """Get credibility weight for news source"""
    for known_source, weight in SOURCE_CREDIBILITY.items():
        if known_source.lower() in source.lower():
            return weight
    return 0.5


def calculate_recency_weight(published_timestamp):
    """Calculate weight based on how recent the article is"""
    try:
        published_time = datetime.fromtimestamp(published_timestamp)
        hours_old = (datetime.now() - published_time).total_seconds() / 3600
        decay_factor = 2 ** (-hours_old / 6)
        return max(0, min(1.0, decay_factor))
    except:
        return 0.5


# ============================================================================
# NEWS FETCHING FUNCTIONS
# ============================================================================

def fetch_company_news_batch(finnhub_client, tickers, lookback_hours=24):
    """
    Fetch news for multiple tickers with rate limiting
    Returns: dict mapping ticker -> list of news articles
    """
    print(f"\n📰 Fetching company news for {len(tickers)} tickers...")
    
    to_date = datetime.now()
    from_date = to_date - timedelta(hours=lookback_hours)
    from_str = from_date.strftime('%Y-%m-%d')
    to_str = to_date.strftime('%Y-%m-%d')
    
    all_news = {}
    
    for ticker in tickers:
        try:
            print(f"  Fetching {ticker}...", end=' ')
            news = finnhub_client.company_news(ticker, _from=from_str, to=to_str)
            all_news[ticker] = news
            print(f"✓ {len(news)} articles")
            
            # Rate limiting to avoid hitting API limits
            time.sleep(API_RATE_LIMIT_DELAY)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            all_news[ticker] = []
    
    total_articles = sum(len(articles) for articles in all_news.values())
    print(f"✅ Total company news articles fetched: {total_articles}")
    
    return all_news


def fetch_general_market_news(finnhub_client):
    """
    Fetch general market news and filter for market-moving content
    Returns: list of relevant market news articles
    """
    print(f"\n📈 Fetching general market news...")
    
    try:
        # Fetch general news - using 'general' category
        news = finnhub_client.general_news('general', min_id=0)
        
        print(f"  Received {len(news)} general news articles")
        
        # Filter for market-moving news
        relevant_news = []
        
        for article in news:
            headline = article.get('headline', '').lower()
            summary = article.get('summary', '').lower()
            combined_text = f"{headline} {summary}"
            
            # Check if article contains market-moving keywords
            has_market_keyword = any(
                keyword in combined_text 
                for keyword in MARKET_MOVING_KEYWORDS
            )
            
            # Check if article should be excluded (opinion pieces, etc.)
            has_exclude_keyword = any(
                keyword in combined_text 
                for keyword in EXCLUDE_KEYWORDS
            )
            
            if has_market_keyword and not has_exclude_keyword:
                relevant_news.append(article)
        
        print(f"✅ Filtered to {len(relevant_news)} market-moving articles")
        return relevant_news
        
    except Exception as e:
        print(f"❌ Error fetching general market news: {e}")
        return []


# ============================================================================
# SENTIMENT ANALYSIS FUNCTIONS
# ============================================================================

def analyze_article_sentiment(article, ticker_obj, article_type='company', base_sentiment=None):
    """
    Analyze sentiment for a single article and return all metrics
    If base_sentiment is provided, skip FinBERT analysis (used in batch processing)
    Returns: dict with all sentiment components
    """
    headline = article.get('headline', '')
    summary = article.get('summary', '')
    source = article.get('source', 'Unknown')
    url = article.get('url', '')
    published_at = article.get('datetime', int(time.time()))
    
    # Generate unique hash
    article_hash = get_article_hash(headline, summary)
    
    # Check if already analyzed or if sentiment was provided
    if base_sentiment is None:
        cached_sentiment = get_cached_sentiment_from_db(article_hash)
        is_cached = cached_sentiment is not None
        
        # Analyze sentiment
        if is_cached:
            base_sentiment = cached_sentiment
        else:
            combined_text = f"{headline}. {summary}"
            base_sentiment = analyze_sentiment_finbert_api(combined_text)
    else:
        # Sentiment was provided from batch processing
        is_cached = False
    
    # Calculate all component factors
    surprise_factor = calculate_surprise_factor(f"{headline} {summary}")
    novelty_score = calculate_novelty(article_hash)
    source_credibility = get_source_credibility(source)
    recency_weight = calculate_recency_weight(published_at)
    
    # Calculate article score using weighted formula
    article_score = (
        base_sentiment * ARTICLE_WEIGHTS['base_sentiment'] * 100 +
        (surprise_factor - 1) * ARTICLE_WEIGHTS['surprise_factor'] * 50 +
        novelty_score * ARTICLE_WEIGHTS['novelty'] * 30 +
        source_credibility * ARTICLE_WEIGHTS['source_credibility'] * 20 +
        recency_weight * ARTICLE_WEIGHTS['recency'] * 20
    )
    
    return {
        'headline': headline,
        'summary': summary,
        'source': source,
        'url': url,
        'published_at': datetime.fromtimestamp(published_at),
        'article_hash': article_hash,
        'article_type': article_type,
        'base_sentiment': base_sentiment,
        'surprise_factor': surprise_factor,
        'novelty_score': novelty_score,
        'source_credibility': source_credibility,
        'recency_weight': recency_weight,
        'article_score': article_score,
        'is_cached': is_cached
    }


def analyze_articles_batch(articles, ticker_obj, article_type='company'):
    """
    Analyze sentiment for multiple articles using batch processing
    Returns: list of article data dicts
    """
    if not articles:
        return []
    
    # Separate cached and uncached articles
    articles_to_analyze = []
    cached_articles = []
    article_hashes = []
    
    for article in articles:
        headline = article.get('headline', '')
        summary = article.get('summary', '')
        article_hash = get_article_hash(headline, summary)
        article_hashes.append(article_hash)
        
        cached_sentiment = get_cached_sentiment_from_db(article_hash)
        if cached_sentiment is not None:
            # Article already analyzed
            cached_articles.append((article, cached_sentiment))
        else:
            # Need to analyze
            articles_to_analyze.append(article)
    
    # Batch process uncached articles
    new_sentiments = []
    if articles_to_analyze:
        print(f"    🔬 Analyzing {len(articles_to_analyze)} new articles with FinBERT (batched)...")
        texts = [f"{a.get('headline', '')}. {a.get('summary', '')}" for a in articles_to_analyze]
        new_sentiments = analyze_sentiment_finbert_batch(texts)
    
    # Process all articles
    all_articles_data = []
    
    # Add cached articles
    for article, sentiment in cached_articles:
        article_data = analyze_article_sentiment(article, ticker_obj, article_type, base_sentiment=sentiment)
        all_articles_data.append(article_data)
    
    # Add newly analyzed articles
    for article, sentiment in zip(articles_to_analyze, new_sentiments):
        article_data = analyze_article_sentiment(article, ticker_obj, article_type, base_sentiment=sentiment)
        all_articles_data.append(article_data)
    
    if articles_to_analyze:
        print(f"    ✅ Batch analysis complete ({len(cached_articles)} cached, {len(articles_to_analyze)} new)")
    
    return all_articles_data


def analyze_ticker_sentiment(finnhub_client, ticker_symbol, ticker_obj, lookback_hours=24):
    """
    Analyze sentiment for a single ticker's news
    Returns: tuple (sentiment_score, article_count, articles_data)
    """
    # Fetch news
    to_date = datetime.now()
    from_date = to_date - timedelta(hours=lookback_hours)
    from_str = from_date.strftime('%Y-%m-%d')
    to_str = to_date.strftime('%Y-%m-%d')
    
    try:
        news = finnhub_client.company_news(ticker_symbol, _from=from_str, to=to_str)
    except Exception as e:
        print(f"  ❌ Error fetching news for {ticker_symbol}: {e}")
        return 0.0, 0, []
    
    if not news:
        return 0.0, 0, []
    
    # Analyze all articles
    articles_data = []
    total_score = 0
    
    for article in news:
        article_data = analyze_article_sentiment(article, ticker_obj, article_type='company')
        articles_data.append(article_data)
        total_score += article_data['article_score']
    
    # Calculate average sentiment score
    avg_sentiment = total_score / len(articles_data) if articles_data else 0
    
    return avg_sentiment, len(articles_data), articles_data


# ============================================================================
# ANALYST RECOMMENDATIONS FUNCTIONS
# ============================================================================

def check_if_new_recommendations_available(finnhub_client, sample_symbols=None):
    """
    Check if new recommendations are available by sampling a few stocks
    Returns True if new recommendations are found, False if same as last run
    """
    if sample_symbols is None:
        # Sample first 5 stocks to check for updates
        sample_symbols = list(NASDAQ_TOP_20.keys())[:5]
    
    print(f"  🔍 Checking for new recommendations (sampling {len(sample_symbols)} stocks)...")
    
    # Get the latest analysis run to compare against
    latest_run = AnalysisRun.objects.filter(ticker__symbol='^IXIC').order_by('-timestamp').first()
    
    if not latest_run or latest_run.analyst_recommendations_count == 0:
        print(f"    No previous recommendations found - fetching all")
        return True
    
    # Check sample stocks for changes
    new_data_found = False
    
    for symbol in sample_symbols:
        try:
            recommendations = finnhub_client.recommendation_trends(symbol)
            if recommendations and len(recommendations) > 0:
                latest = recommendations[0]
                total_recommendations = (
                    latest.get('strongBuy', 0) + 
                    latest.get('buy', 0) + 
                    latest.get('hold', 0) + 
                    latest.get('sell', 0) + 
                    latest.get('strongSell', 0)
                )
                
                if total_recommendations > 0:
                    # Check if this is significantly different from what we have
                    # For now, just check if the total count has changed
                    # In a more sophisticated version, we could check the actual recommendation breakdown
                    if total_recommendations != (latest_run.analyst_recommendations_count // len(NASDAQ_TOP_20)):
                        new_data_found = True
                        break
                        
        except Exception as e:
            print(f"    ⚠️ Error checking {symbol}: {e}")
            continue
    
    if new_data_found:
        print(f"    ✅ New recommendations detected - fetching all")
    else:
        print(f"    📊 No new recommendations - using cached data")
    
    return new_data_found


def fetch_analyst_recommendations(finnhub_client):
    """
    Fetch analyst recommendations for NASDAQ top 20 stocks and aggregate them
    Returns weighted average recommendation score (-100 to +100)
    """
    print(f"  📊 Fetching analyst recommendations for {len(NASDAQ_TOP_20)} stocks...")
    
    total_strong_buy = 0
    total_buy = 0
    total_hold = 0
    total_sell = 0
    total_strong_sell = 0
    total_weighted_score = 0.0
    total_weight = 0.0
    
    stocks_with_recommendations = 0
    
    for symbol, market_cap_weight in NASDAQ_TOP_20.items():
        try:
            # Fetch recommendations for this stock
            recommendations = finnhub_client.recommendation_trends(symbol)
            
            if recommendations and len(recommendations) > 0:
                latest = recommendations[0]
                
                # Get recommendation counts
                strong_buy = latest.get('strongBuy', 0)
                buy = latest.get('buy', 0)
                hold = latest.get('hold', 0)
                sell = latest.get('sell', 0)
                strong_sell = latest.get('strongSell', 0)
                
                total_recommendations = strong_buy + buy + hold + sell + strong_sell
                
                if total_recommendations > 0:
                    # Calculate weighted score for this stock (-1 to +1 range)
                    # Strong Buy=2, Buy=1, Hold=0, Sell=-1, Strong Sell=-2
                    weighted_score = (
                        strong_buy * 2 + 
                        buy * 1 + 
                        hold * 0 + 
                        sell * -1 + 
                        strong_sell * -2
                    )
                    
                    # Normalize to -1 to +1 range
                    normalized_score = weighted_score / (total_recommendations * 2)
                    
                    # Apply market cap weighting
                    total_weighted_score += normalized_score * market_cap_weight
                    total_weight += market_cap_weight
                    
                    # Add to totals
                    total_strong_buy += strong_buy
                    total_buy += buy
                    total_hold += hold
                    total_sell += sell
                    total_strong_sell += strong_sell
                    
                    stocks_with_recommendations += 1
                    
                    print(f"    {symbol}: {strong_buy}S+{buy}B+{hold}H+{sell}S+{strong_sell}SS (score: {normalized_score:+.2f})")
                else:
                    print(f"    {symbol}: No recommendation data")
            else:
                print(f"    {symbol}: No recommendations available")
                
        except Exception as e:
            print(f"    {symbol}: Error - {e}")
            continue
    
    # Calculate final composite score (-100 to +100)
    if total_weight > 0:
        composite_score = (total_weighted_score / total_weight) * 100
    else:
        composite_score = 0.0
    
    total_recommendations = total_strong_buy + total_buy + total_hold + total_sell + total_strong_sell
    
    return {
        'composite_score': composite_score,
        'total_recommendations': total_recommendations,
        'strong_buy': total_strong_buy,
        'buy': total_buy,
        'hold': total_hold,
        'sell': total_sell,
        'strong_sell': total_strong_sell,
        'stocks_analyzed': stocks_with_recommendations,
        'total_stocks': len(NASDAQ_TOP_20)
    }


# ============================================================================
# MAIN ANALYSIS FUNCTIONS
# ============================================================================

def run_nasdaq_composite_analysis(finnhub_client):
    """
    Main function to run complete NASDAQ composite analysis
    Uses hybrid approach: company news (70%) + market news (30%)
    """
    print("\n" + "="*80)
    print("🚀 STARTING NASDAQ COMPOSITE SENTIMENT ANALYSIS")
    print("="*80)
    
    start_time = time.time()
    
    # Step 1: Initialize or get NASDAQ composite ticker
    nasdaq_ticker, created = Ticker.objects.get_or_create(
        symbol='^IXIC',
        defaults={
            'company_name': 'NASDAQ Composite Index',
            'exchange': 'NASDAQ'
        }
    )
    if created:
        print(f"✨ Created NASDAQ composite ticker: ^IXIC")
    
    # Step 2: Initialize all component tickers
    print(f"\n📊 Initializing {len(NASDAQ_TOP_20)} component tickers...")
    ticker_objects = {}
    for symbol, weight in NASDAQ_TOP_20.items():
        ticker_obj, _ = Ticker.objects.get_or_create(
            symbol=symbol,
            defaults={'company_name': COMPANY_NAMES.get(symbol, f'{symbol} Inc.')}
        )
        ticker_objects[symbol] = ticker_obj
    print(f"✅ All tickers initialized")
    
    # Step 3: Fetch company news for all tickers with rate limiting
    print(f"\n📰 PHASE 1: Fetching company-specific news")
    print(f"   Weight in composite: {SENTIMENT_WEIGHTS['company_news']:.0%}")
    company_news_dict = fetch_company_news_batch(
        finnhub_client, 
        list(NASDAQ_TOP_20.keys()),
        lookback_hours=24
    )
    
    # Step 3.5: Check if we have any new articles
    print(f"\n🔍 Checking for new articles...")
    has_new_articles = False
    all_article_hashes = []
    
    # Collect all article hashes from fetched news
    for symbol, news_articles in company_news_dict.items():
        for article in news_articles[:10]:  # Check top 10 per ticker
            article_hash = get_article_hash(
                article.get('headline', ''),
                article.get('summary', '')
            )
            all_article_hashes.append(article_hash)
    
    # Also check general market news
    market_news_preview = fetch_general_market_news(finnhub_client)
    for article in market_news_preview[:20]:  # Check top 20 market articles
        article_hash = get_article_hash(
            article.get('headline', ''),
            article.get('summary', '')
        )
        all_article_hashes.append(article_hash)
    
    # Check if any articles are new (not in database)
    if all_article_hashes:
        existing_hashes = set(
            NewsArticle.objects.filter(
                article_hash__in=all_article_hashes
            ).values_list('article_hash', flat=True)
        )
        new_hashes = set(all_article_hashes) - existing_hashes
        has_new_articles = len(new_hashes) > 0
        
        print(f"   Total articles found: {len(all_article_hashes)}")
        print(f"   Already analyzed: {len(existing_hashes)}")
        print(f"   New articles: {len(new_hashes)}")

    # Step 3.5: Fetch and analyze Reddit content (runs every time, regardless of new articles)
    print(f"\n🔴 PHASE 4: Analyzing Reddit sentiment")
    reddit_sentiment = 0.0
    reddit_analysis_data = {}

    try:
        # Fetch Reddit posts and comments
        reddit_content = fetch_all_reddit_content()

        if reddit_content and reddit_content['posts']:
            # Analyze Reddit content
            reddit_analysis_data = analyze_reddit_content_batch(
                reddit_content['posts'],
                reddit_content['comments'],
                nasdaq_ticker
            )

            reddit_sentiment = reddit_analysis_data['composite_score']
            print(f"✅ Reddit Sentiment: {reddit_sentiment:+.2f}")
            print(f"   Posts analyzed: {reddit_analysis_data.get('posts_analyzed', 0)}")
            print(f"   Comments analyzed: {reddit_analysis_data.get('comments_analyzed', 0)}")
        else:
            print(f"  ⚠️  No Reddit content fetched (check API credentials)")

    except Exception as e:
        print(f"  ⚠️  Reddit analysis failed: {e}")
        import traceback
        traceback.print_exc()
        reddit_sentiment = 0.0

    # Step 4.5: Fetch and analyze Analyst Recommendations
    print(f"\n📊 PHASE 5: Analyzing Analyst Recommendations")
    analyst_recommendations_score = 0.0
    analyst_recommendations_data = {}

    try:
        # Check if new recommendations are available before fetching all
        if check_if_new_recommendations_available(finnhub_client):
            analyst_recommendations_data = fetch_analyst_recommendations(finnhub_client)
            analyst_recommendations_score = analyst_recommendations_data['composite_score']
            print(f"✅ Analyst Recommendations: {analyst_recommendations_score:+.2f}")
            print(f"   Total recommendations: {analyst_recommendations_data.get('total_recommendations', 0)}")
            print(f"   Strong Buy: {analyst_recommendations_data.get('strong_buy', 0)}")
            print(f"   Buy: {analyst_recommendations_data.get('buy', 0)}")
            print(f"   Hold: {analyst_recommendations_data.get('hold', 0)}")
            print(f"   Sell: {analyst_recommendations_data.get('sell', 0)}")
            print(f"   Strong Sell: {analyst_recommendations_data.get('strong_sell', 0)}")
        else:
            # Use cached data from latest run
            latest_run = AnalysisRun.objects.filter(ticker=nasdaq_ticker).order_by('-timestamp').first()
            if latest_run and latest_run.analyst_recommendations_score is not None:
                analyst_recommendations_score = latest_run.analyst_recommendations_score
                analyst_recommendations_data = {
                    'composite_score': latest_run.analyst_recommendations_score,
                    'total_recommendations': latest_run.analyst_recommendations_count,
                    'strong_buy': latest_run.analyst_strong_buy,
                    'buy': latest_run.analyst_buy,
                    'hold': latest_run.analyst_hold,
                    'sell': latest_run.analyst_sell,
                    'strong_sell': latest_run.analyst_strong_sell
                }
                print(f"✅ Analyst Recommendations (cached): {analyst_recommendations_score:+.2f}")
                print(f"   Total recommendations: {analyst_recommendations_data.get('total_recommendations', 0)}")
                print(f"   Strong Buy: {analyst_recommendations_data.get('strong_buy', 0)}")
                print(f"   Buy: {analyst_recommendations_data.get('buy', 0)}")
                print(f"   Hold: {analyst_recommendations_data.get('hold', 0)}")
                print(f"   Sell: {analyst_recommendations_data.get('sell', 0)}")
                print(f"   Strong Sell: {analyst_recommendations_data.get('strong_sell', 0)}")
            else:
                print(f"  ⚠️  No cached analyst recommendations found")
                analyst_recommendations_score = 0.0
    except Exception as e:
        print(f"  ⚠️  Analyst recommendations analysis failed: {e}")
        import traceback
        traceback.print_exc()
        analyst_recommendations_score = 0.0

    # If no new articles, create a duplicate run with updated price
    if not has_new_articles:
        print(f"\n✅ No new articles found - creating new run with updated price")

        # Get latest analysis run
        latest_run = AnalysisRun.objects.filter(ticker=nasdaq_ticker).order_by('-timestamp').first()

        if latest_run:
            # Fetch current stock price and OHLCV from Yahoo Finance
            try:
                ohlcv = fetch_latest_ohlcv_from_yfinance(symbol='^IXIC', interval='1m')

                if ohlcv:
                    new_price = Decimal(str(ohlcv['close']))
                    new_open = Decimal(str(ohlcv['open']))
                    new_high = Decimal(str(ohlcv['high']))
                    new_low = Decimal(str(ohlcv['low']))
                    new_volume = ohlcv['volume']
                    new_change = ((ohlcv['close'] - ohlcv['open']) / ohlcv['open'] * 100) if ohlcv['open'] != 0 else 0
                else:
                    # Fallback to Finnhub
                    quote = finnhub_client.quote('^IXIC')
                    new_price = Decimal(str(quote['c']))
                    new_open = Decimal(str(quote.get('o', quote['c'])))
                    new_high = Decimal(str(quote.get('h', quote['c'])))
                    new_low = Decimal(str(quote.get('l', quote['c'])))
                    new_change = quote.get('dp', 0)
                    new_volume = None

                # Calculate fresh technical indicators from database history
                tech_indicators, symbol_used = fetch_indicators_with_fallback(
                    symbols=INDICATOR_SYMBOLS,
                    resolution=INDICATOR_RESOLUTION,
                    hours_back=INDICATOR_LOOKBACK_HOURS,
                    config=INDICATOR_PERIODS
                )

                # Calculate technical composite score with error handling
                try:
                    tech_composite = calculate_technical_composite_score(tech_indicators)
                    print(f"✅ Technical composite calculated: {tech_composite}")
                except Exception as tech_error:
                    print(f"⚠️  ERROR calculating technical composite: {tech_error}")
                    import traceback
                    traceback.print_exc()
                    tech_composite = 0.0  # Fallback to 0

                # Recalculate composite score with 4-factor model
                # Keep news from cache, use fresh reddit, technical, and analyst recommendations
                NEWS_WEIGHT = 0.35
                SOCIAL_WEIGHT = 0.20
                TECHNICAL_WEIGHT = 0.25
                ANALYST_WEIGHT = 0.20

                # Extract news sentiment from previous run
                news_composite = latest_run.avg_base_sentiment or 0.0

                # Calculate NEW composite score with 4-factor model
                new_composite_score = (
                    news_composite * NEWS_WEIGHT +
                    reddit_sentiment * SOCIAL_WEIGHT +
                    tech_composite * TECHNICAL_WEIGHT +
                    analyst_recommendations_score * ANALYST_WEIGHT
                )

                # Determine sentiment label
                if new_composite_score >= 30:
                    sentiment_label = 'BULLISH'
                elif new_composite_score <= -30:
                    sentiment_label = 'BEARISH'
                else:
                    sentiment_label = 'NEUTRAL'

                print(f"\n📊 RECALCULATED COMPOSITE SCORE (Cached Articles Path):")
                print(f"   News Sentiment:            {news_composite:+.2f} × {NEWS_WEIGHT:.0%} = {news_composite * NEWS_WEIGHT:+.2f}")
                print(f"   Social Media (Reddit):     {reddit_sentiment:+.2f} × {SOCIAL_WEIGHT:.0%} = {reddit_sentiment * SOCIAL_WEIGHT:+.2f}")
                print(f"   Technical Indicators:      {tech_composite:+.2f} × {TECHNICAL_WEIGHT:.0%} = {tech_composite * TECHNICAL_WEIGHT:+.2f}")
                print(f"   Analyst Recommendations:   {analyst_recommendations_score:+.2f} × {ANALYST_WEIGHT:.0%} = {analyst_recommendations_score * ANALYST_WEIGHT:+.2f}")
                print(f"   Final Composite:           {new_composite_score:+.2f} ({sentiment_label})")

                # Create a new run with recalculated composite and updated price
                new_run = AnalysisRun.objects.create(
                    ticker=nasdaq_ticker,
                    composite_score=new_composite_score,
                    sentiment_label=sentiment_label,
                    stock_price=new_price,
                    price_open=new_open,
                    price_high=new_high,
                    price_low=new_low,
                    price_change_percent=new_change,
                    volume=new_volume,
                    avg_base_sentiment=latest_run.avg_base_sentiment,
                    avg_surprise_factor=latest_run.avg_surprise_factor,
                    avg_novelty=latest_run.avg_novelty,
                    avg_source_credibility=latest_run.avg_source_credibility,
                    avg_recency_weight=latest_run.avg_recency_weight,
                    articles_analyzed=latest_run.articles_analyzed,
                    cached_articles=latest_run.articles_analyzed,
                    new_articles=0,
                    # Copy technical indicators from the most recent run that has them (with MACD calculation)
                    rsi_14=tech_indicators['rsi_14'],
                    macd=tech_indicators['macd'],
                    macd_signal=tech_indicators['macd_signal'],
                    macd_histogram=tech_indicators['macd_histogram'],
                    bb_upper=tech_indicators['bb_upper'],
                    bb_middle=tech_indicators['bb_middle'],
                    bb_lower=tech_indicators['bb_lower'],
                    sma_20=tech_indicators['sma_20'],
                    sma_50=tech_indicators['sma_50'],
                    ema_9=tech_indicators['ema_9'],
                    ema_20=tech_indicators['ema_20'],
                    stoch_k=tech_indicators['stoch_k'],
                    stoch_d=tech_indicators['stoch_d'],
                    williams_r=tech_indicators['williams_r'],
                    atr_14=tech_indicators['atr_14'],
                    qqq_price=tech_indicators['qqq_price'],
                    # Reddit sentiment (fresh analysis even in cached path)
                    reddit_sentiment=reddit_sentiment,
                    reddit_posts_analyzed=reddit_analysis_data.get('posts_analyzed', 0),
                    reddit_comments_analyzed=reddit_analysis_data.get('comments_analyzed', 0),
                    # Technical composite score
                    technical_composite_score=tech_composite,
                    # Analyst recommendations
                    analyst_recommendations_score=analyst_recommendations_score,
                    analyst_recommendations_count=analyst_recommendations_data.get('total_recommendations', 0),
                    analyst_strong_buy=analyst_recommendations_data.get('strong_buy', 0),
                    analyst_buy=analyst_recommendations_data.get('buy', 0),
                    analyst_hold=analyst_recommendations_data.get('hold', 0),
                    analyst_sell=analyst_recommendations_data.get('sell', 0),
                    analyst_strong_sell=analyst_recommendations_data.get('strong_sell', 0)
                )
                
                # Copy ticker contributions from previous run
                prev_contributions = TickerContribution.objects.filter(analysis_run=latest_run)
                for contrib in prev_contributions:
                    TickerContribution.objects.create(
                        analysis_run=new_run,
                        ticker=contrib.ticker,
                        sentiment_score=contrib.sentiment_score,
                        market_cap_weight=contrib.market_cap_weight,
                        weighted_contribution=contrib.weighted_contribution,
                        articles_analyzed=contrib.articles_analyzed
                    )
                
                print(f"📊 Updated NASDAQ (^IXIC) Price: ${new_price:.2f} ({new_change:+.2f}%)")
                print(f"✅ Created new run #{new_run.id} with updated price (sentiment unchanged)")
                print(f"⏱️  Completed in {time.time() - start_time:.1f} seconds")
                
                return new_run
            except Exception as e:
                print(f"⚠️ Error creating new run: {e}")
                return None
        else:
            print(f"⚠️ No previous analysis found - running full analysis")
            has_new_articles = True  # Force full analysis
    
    # Continue with full analysis if we have new articles
    print(f"\n🔬 Proceeding with full sentiment analysis...")
    
    # Step 4: Analyze sentiment for each ticker
    print(f"\n🔍 PHASE 2: Analyzing company sentiment")
    ticker_sentiments = {}
    ticker_contributions = {}
    all_company_articles = []
    
    for symbol, weight in NASDAQ_TOP_20.items():
        print(f"\n  Analyzing {symbol} ({weight:.1%} weight)...")
        ticker_obj = ticker_objects[symbol]
        news_articles = company_news_dict.get(symbol, [])
        
        if not news_articles:
            print(f"    ⚠️ No news found")
            ticker_sentiments[symbol] = 0.0
            ticker_contributions[symbol] = {
                'sentiment': 0.0,
                'weight': weight,
                'contribution': 0.0,
                'articles_count': 0,
                'articles_data': []
            }
            continue
        
        # Batch analyze articles (top 10 most recent)
        articles_to_process = news_articles[:10]
        articles_data = analyze_articles_batch(articles_to_process, ticker_obj, article_type='company')
        
        # Calculate total score
        total_score = sum(article_data['article_score'] for article_data in articles_data)
        all_company_articles.extend(articles_data)
        
        avg_sentiment = total_score / len(articles_data) if articles_data else 0
        weighted_contribution = avg_sentiment * weight
        
        ticker_sentiments[symbol] = avg_sentiment
        ticker_contributions[symbol] = {
            'sentiment': avg_sentiment,
            'weight': weight,
            'contribution': weighted_contribution,
            'articles_count': len(articles_data),
            'articles_data': articles_data
        }
        
        print(f"    ✓ Sentiment: {avg_sentiment:+.2f} | Contribution: {weighted_contribution:+.2f} | Articles: {len(articles_data)}")
    
    # Step 5: Calculate weighted company sentiment
    company_sentiment = sum(
        contrib['contribution'] 
        for contrib in ticker_contributions.values()
    )
    
    print(f"\n📈 Company News Composite Sentiment: {company_sentiment:+.2f}")
    
    # Step 6: Fetch and analyze general market news (reuse if already fetched)
    print(f"\n📡 PHASE 3: Analyzing general market news")
    print(f"   Weight in composite: {SENTIMENT_WEIGHTS['market_news']:.0%}")
    
    # Use the market news we already fetched during the check, or fetch fresh if needed
    market_news = market_news_preview if 'market_news_preview' in locals() else fetch_general_market_news(finnhub_client)
    market_articles_data = []
    market_sentiment = 0.0
    
    if market_news:
        # Batch analyze market news (top 20 most relevant)
        print(f"  📊 Processing {min(20, len(market_news))} market news articles...")
        market_articles_data = analyze_articles_batch(market_news[:20], nasdaq_ticker, article_type='market')
        
        total_market_score = sum(article_data['article_score'] for article_data in market_articles_data)
        market_sentiment = total_market_score / len(market_articles_data) if market_articles_data else 0
        print(f"✅ Market News Sentiment: {market_sentiment:+.2f} | Articles: {len(market_articles_data)}")
    else:
        print(f"⚠️ No relevant market news found")

    # Step 7: Calculate news composite (company + market)
    news_composite = (
        company_sentiment * SENTIMENT_WEIGHTS['company_news'] +
        market_sentiment * SENTIMENT_WEIGHTS['market_news']
    )
    
    # Step 8: Get NASDAQ index price and OHLCV data from Yahoo Finance (NASDAQ Composite Index)
    try:
        print(f"\n📊 Fetching real-time OHLCV from Yahoo Finance...")
        ohlcv = fetch_latest_ohlcv_from_yfinance(symbol='^IXIC', interval='1m')

        if ohlcv:
            index_price = Decimal(str(ohlcv['close']))
            price_open = Decimal(str(ohlcv['open']))
            price_high = Decimal(str(ohlcv['high']))
            price_low = Decimal(str(ohlcv['low']))
            volume = ohlcv['volume']

            # Calculate price change percentage
            price_change = ((ohlcv['close'] - ohlcv['open']) / ohlcv['open'] * 100) if ohlcv['open'] != 0 else 0
        else:
            raise Exception("No OHLCV data from Yahoo Finance")

    except Exception as e:
        print(f"\n⚠️ Could not fetch OHLCV from Yahoo Finance: {e}")
        print(f"  Falling back to Finnhub quote...")
        try:
            quote = finnhub_client.quote('^IXIC')
            index_price = Decimal(str(quote['c']))
            price_open = Decimal(str(quote.get('o', quote['c'])))
            price_high = Decimal(str(quote.get('h', quote['c'])))
            price_low = Decimal(str(quote.get('l', quote['c'])))
            price_change = quote.get('dp', 0)
            volume = None
        except Exception as e2:
            print(f"\n⚠️ Finnhub fallback also failed: {e2}")
            index_price = Decimal('0.00')
            price_open = Decimal('0.00')
            price_high = Decimal('0.00')
            price_low = Decimal('0.00')
            price_change = 0.0
            volume = None
    
    # Step 9: Calculate technical indicators from OHLCV data
    # Fetch fresh OHLCV data and calculate indicators on every run
    technical_indicators, symbol_used = fetch_indicators_with_fallback(
        symbols=INDICATOR_SYMBOLS,
        resolution=INDICATOR_RESOLUTION,
        hours_back=INDICATOR_LOOKBACK_HOURS,
        config=INDICATOR_PERIODS
    )

    # Step 9.5: Calculate technical composite score
    technical_composite_score = calculate_technical_composite_score(technical_indicators)
    print(f"\n📊 Technical Indicators Composite Score: {technical_composite_score:+.2f}")

    # Step 10: Calculate FINAL composite score (4-factor model)
    # Weighting optimized for market movement prediction:
    # - News: Most impactful for immediate market reactions (35%)
    # - Technical: Price action and momentum signals (25%)
    # - Social Media: Retail sentiment and momentum (20%)
    # - Analyst Recommendations: Professional institutional outlook (20%)
    NEWS_WEIGHT = 0.35
    SOCIAL_WEIGHT = 0.20
    TECHNICAL_WEIGHT = 0.25
    ANALYST_WEIGHT = 0.20

    final_composite_score = (
        news_composite * NEWS_WEIGHT +
        reddit_sentiment * SOCIAL_WEIGHT +
        technical_composite_score * TECHNICAL_WEIGHT +
        analyst_recommendations_score * ANALYST_WEIGHT
    )

    print(f"\n{'='*80}")
    print(f"🎯 FINAL NASDAQ COMPOSITE SENTIMENT SCORE: {final_composite_score:+.2f}")
    print(f"{'='*80}")
    print(f"   News Sentiment:            {news_composite:+.2f} × {NEWS_WEIGHT:.0%} = {news_composite * NEWS_WEIGHT:+.2f}")
    print(f"   Social Media (Reddit):     {reddit_sentiment:+.2f} × {SOCIAL_WEIGHT:.0%} = {reddit_sentiment * SOCIAL_WEIGHT:+.2f}")
    print(f"   Technical Indicators:      {technical_composite_score:+.2f} × {TECHNICAL_WEIGHT:.0%} = {technical_composite_score * TECHNICAL_WEIGHT:+.2f}")
    print(f"   Analyst Recommendations:   {analyst_recommendations_score:+.2f} × {ANALYST_WEIGHT:.0%} = {analyst_recommendations_score * ANALYST_WEIGHT:+.2f}")
    print(f"{'='*80}")

    # Step 11: Save to database
    print(f"\n💾 Saving analysis to database...")

    with transaction.atomic():
        # Calculate averages for component scores
        all_articles = all_company_articles + market_articles_data
        total_articles = len(all_articles)
        cached_count = sum(1 for a in all_articles if a['is_cached'])
        new_count = total_articles - cached_count

        avg_base_sentiment = sum(a['base_sentiment'] for a in all_articles) / total_articles if total_articles else 0
        avg_surprise = sum(a['surprise_factor'] for a in all_articles) / total_articles if total_articles else 1.0
        avg_novelty = sum(a['novelty_score'] for a in all_articles) / total_articles if total_articles else 1.0
        avg_credibility = sum(a['source_credibility'] for a in all_articles) / total_articles if total_articles else 0.5
        avg_recency = sum(a['recency_weight'] for a in all_articles) / total_articles if total_articles else 0.5

        # Create AnalysisRun with OHLCV and technical indicators
        analysis_run = AnalysisRun.objects.create(
            ticker=nasdaq_ticker,
            composite_score=float(final_composite_score),
            avg_base_sentiment=avg_base_sentiment,
            avg_surprise_factor=avg_surprise,
            avg_novelty=avg_novelty,
            avg_source_credibility=avg_credibility,
            avg_recency_weight=avg_recency,
            # OHLCV data (from Yahoo Finance)
            stock_price=index_price,
            price_open=price_open,
            price_high=price_high,
            price_low=price_low,
            price_change_percent=price_change,
            volume=volume,
            articles_analyzed=total_articles,
            cached_articles=cached_count,
            new_articles=new_count,
            # Technical indicators
            rsi_14=technical_indicators.get('rsi_14'),
            macd=technical_indicators.get('macd'),
            macd_signal=technical_indicators.get('macd_signal'),
            macd_histogram=technical_indicators.get('macd_histogram'),
            bb_upper=technical_indicators.get('bb_upper'),
            bb_middle=technical_indicators.get('bb_middle'),
            bb_lower=technical_indicators.get('bb_lower'),
            sma_20=technical_indicators.get('sma_20'),
            sma_50=technical_indicators.get('sma_50'),
            ema_9=technical_indicators.get('ema_9'),
            ema_20=technical_indicators.get('ema_20'),
            stoch_k=technical_indicators.get('stoch_k'),
            stoch_d=technical_indicators.get('stoch_d'),
            williams_r=technical_indicators.get('williams_r'),
            atr_14=technical_indicators.get('atr_14'),
            qqq_price=technical_indicators.get('qqq_price'),
            # Reddit sentiment
            reddit_sentiment=reddit_sentiment,
            reddit_posts_analyzed=reddit_analysis_data.get('posts_analyzed', 0),
            reddit_comments_analyzed=reddit_analysis_data.get('comments_analyzed', 0),
            # Technical composite score
            technical_composite_score=technical_composite_score,
            # Analyst recommendations
            analyst_recommendations_score=analyst_recommendations_score,
            analyst_recommendations_count=analyst_recommendations_data.get('total_recommendations', 0),
            analyst_strong_buy=analyst_recommendations_data.get('strong_buy', 0),
            analyst_buy=analyst_recommendations_data.get('buy', 0),
            analyst_hold=analyst_recommendations_data.get('hold', 0),
            analyst_sell=analyst_recommendations_data.get('sell', 0),
            analyst_strong_sell=analyst_recommendations_data.get('strong_sell', 0)
        )
        
        print(f"✓ Created AnalysisRun #{analysis_run.id}")
        
        # Save ticker contributions
        for symbol, contrib in ticker_contributions.items():
            if contrib['articles_count'] > 0:
                TickerContribution.objects.create(
                    analysis_run=analysis_run,
                    ticker=ticker_objects[symbol],
                    sentiment_score=contrib['sentiment'],
                    market_cap_weight=contrib['weight'],
                    weighted_contribution=contrib['contribution'],
                    articles_analyzed=contrib['articles_count']
                )
        
        print(f"✓ Saved {len(ticker_contributions)} ticker contributions")
        
        # Save all articles
        for article_data in all_articles:
            NewsArticle.objects.update_or_create(
                article_hash=article_data['article_hash'],
                defaults={
                    'ticker': nasdaq_ticker if article_data['article_type'] == 'market' else ticker_objects.get(article_data.get('ticker_symbol', '^IXIC'), nasdaq_ticker),
                    'analysis_run': analysis_run,
                    'headline': article_data['headline'],
                    'summary': article_data['summary'],
                    'source': article_data['source'],
                    'url': article_data['url'],
                    'published_at': article_data['published_at'],
                    'article_type': article_data['article_type'],
                    'base_sentiment': article_data['base_sentiment'],
                    'surprise_factor': article_data['surprise_factor'],
                    'novelty_score': article_data['novelty_score'],
                    'source_credibility': article_data['source_credibility'],
                    'recency_weight': article_data['recency_weight'],
                    'article_score': article_data['article_score'],
                    'weighted_contribution': article_data['article_score'] / total_articles if total_articles else 0,
                    'is_analyzed': True,
                    'sentiment_cached': article_data['is_cached']
                }
            )
        
        print(f"✓ Saved {total_articles} news articles")
    
    elapsed_time = time.time() - start_time
    print(f"\n✅ Analysis complete in {elapsed_time:.1f} seconds")
    print(f"📊 View results: http://localhost:8000/admin/api/analysisrun/{analysis_run.id}/change/")
    
    return analysis_run


# ============================================================================
# DJANGO COMMAND
# ============================================================================

class Command(BaseCommand):
    help = 'Run NASDAQ composite sentiment analysis using hybrid approach'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=300,
            help='Update interval in seconds (default: 300 = 5 minutes)'
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run analysis once and exit (don\'t monitor continuously)'
        )
    
    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']

        # Check if market is open (can be skipped with SKIP_MARKET_HOURS_CHECK env var)
        skip_market_check = os.environ.get('SKIP_MARKET_HOURS_CHECK', 'False') == 'True'

        if not skip_market_check:
            market_open, reason = is_market_open()
            if not market_open:
                self.stdout.write(self.style.WARNING(
                    f'⏸️  Market Closed - Skipping Run\n'
                    f'   Reason: {reason}\n'
                    f'   Current time: {get_market_status()["current_time_ct"]}'
                ))
                return

        # Validate API keys
        if not FINNHUB_API_KEY:
            self.stdout.write(self.style.ERROR(
                '❌ FINNHUB_API_KEY not set! Set it in .env file.'
            ))
            return
        
        if not HUGGINGFACE_API_KEY:
            self.stdout.write(self.style.ERROR(
                '❌ HUGGINGFACE_API_KEY not set! Set it in .env file.'
            ))
            return
        
        # Initialize Finnhub client
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        
        self.stdout.write(self.style.SUCCESS(
            '\n🚀 NASDAQ Composite Sentiment Tracker - Hybrid Approach'
        ))
        self.stdout.write(f'📊 Tracking {len(NASDAQ_TOP_20)} top NASDAQ stocks')
        self.stdout.write(f'🔄 Company News Weight: {SENTIMENT_WEIGHTS["company_news"]:.0%}')
        self.stdout.write(f'📡 Market News Weight: {SENTIMENT_WEIGHTS["market_news"]:.0%}')
        self.stdout.write('💾 All data saved to database\n')
        
        if run_once:
            # Run once
            result = run_nasdaq_composite_analysis(finnhub_client)
            if result:
                # Handle both dict (price-only update) and AnalysisRun object
                if isinstance(result, dict):
                    self.stdout.write(f"\n📊 Current Score: {result['composite_score']:+.2f}")
                    self.stdout.write(f"💰 Stock Price: ${result['stock_price']:.2f} ({result['price_change']:+.2f}%)")
                    self.interpret_score(result['composite_score'])
                else:
                    self.interpret_score(result.composite_score)
        else:
            # Run continuously
            self.stdout.write(f'⏱️  Update interval: {interval} seconds')
            self.stdout.write('⌨️  Press Ctrl+C to stop\n')
            
            iteration = 0
            
            try:
                while True:
                    iteration += 1
                    self.stdout.write(f"\n{'>'*30} ITERATION {iteration} {'<'*30}")
                    
                    result = run_nasdaq_composite_analysis(finnhub_client)
                    if result:
                        # Handle both dict (price-only update) and AnalysisRun object
                        if isinstance(result, dict):
                            self.stdout.write(f"\n📊 Current Score: {result['composite_score']:+.2f}")
                            self.stdout.write(f"💰 Stock Price: ${result['stock_price']:.2f} ({result['price_change']:+.2f}%)")
                            self.interpret_score(result['composite_score'])
                        else:
                            self.interpret_score(result.composite_score)
                    
                    self.stdout.write(f"\n💤 Next update in {interval} seconds...")
                    time.sleep(interval)
                    
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING(
                    f'\n\n⛔ Monitoring stopped by user.'
                ))
                self.stdout.write(f'📊 Total iterations: {iteration}')
                self.stdout.write(f'📰 Unique articles seen: {len(seen_articles)}')
    
    def interpret_score(self, score):
        """Interpret and display the sentiment score"""
        if score > 50:
            sentiment = self.style.SUCCESS("STRONGLY BULLISH 🚀")
        elif score > 20:
            sentiment = self.style.SUCCESS("BULLISH 📈")
        elif score > -20:
            sentiment = self.style.WARNING("NEUTRAL ➡️")
        elif score > -50:
            sentiment = self.style.ERROR("BEARISH 📉")
        else:
            sentiment = self.style.ERROR("STRONGLY BEARISH 🔻")
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(f"Current NASDAQ Sentiment: {sentiment}")
        self.stdout.write(f"Score: {score:+.2f}/100")
        self.stdout.write(f"{'='*80}")

