"""
NASDAQ Sentiment Scorer - Django Management Command
Run with: python manage.py run_sentiment_analysis
"""

import os
import time
import hashlib
import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Avg, Min, Max, Count
import requests
import finnhub
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))

# Import models
from api.models import Ticker, SentimentScore, StockPrice, NewsArticle, SentimentHistory

# ============================================================================
# CONFIGURATION
# ============================================================================

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY', '')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')
UPDATE_INTERVAL_SECONDS = 60  # Run every minute

# Weights for composite score
WEIGHTS = {
    'base_sentiment': 0.40,
    'surprise_factor': 0.25,
    'novelty': 0.15,
    'source_credibility': 0.10,
    'recency': 0.10
}

# Source credibility ratings
SOURCE_CREDIBILITY = {
    'Bloomberg': 1.0,
    'Reuters': 1.0,
    'Wall Street Journal': 0.95,
    'Financial Times': 0.95,
    'CNBC': 0.8,
    'MarketWatch': 0.75,
    'Seeking Alpha': 0.7,
    'Yahoo Finance': 0.7,
    'Benzinga': 0.75,
    'PR Newswire': 0.6,
    'Business Wire': 0.6,
}

# Cache to track seen articles in current session
seen_articles = set()

# ============================================================================
# DATABASE HELPERS
# ============================================================================

def get_or_create_ticker(symbol, company_name=""):
    """Get or create ticker in database"""
    ticker, created = Ticker.objects.get_or_create(
        symbol=symbol.upper(),
        defaults={'company_name': company_name}
    )
    if created:
        print(f"✨ Created new ticker: {symbol}")
    return ticker


def get_cached_sentiment_from_db(article_hash):
    """Get cached sentiment from database"""
    try:
        article = NewsArticle.objects.filter(article_hash=article_hash).first()
        if article and article.is_analyzed:
            return article.base_sentiment
    except Exception as e:
        print(f"⚠️ Error fetching cached sentiment: {e}")
    return None


def save_news_article_to_db(ticker, article_data, sentiment_data):
    """Save news article and sentiment to database"""
    try:
        article_obj, created = NewsArticle.objects.update_or_create(
            article_hash=sentiment_data['article_hash'],
            defaults={
                'ticker': ticker,
                'headline': article_data.get('headline', ''),
                'summary': article_data.get('summary', ''),
                'source': article_data.get('source', 'Unknown'),
                'url': article_data.get('url', ''),
                'published_at': datetime.fromtimestamp(article_data.get('datetime', 0)),
                'base_sentiment': sentiment_data['base_sentiment'],
                'surprise_factor': sentiment_data['surprise_factor'],
                'novelty_score': sentiment_data['novelty'],
                'source_credibility': sentiment_data['source_credibility'],
                'recency_weight': sentiment_data['recency'],
                'article_score': sentiment_data['article_score'],
                'weighted_contribution': sentiment_data['weighted_contribution'],
                'is_analyzed': True,
                'sentiment_cached': sentiment_data['was_cached'],
            }
        )
        return article_obj
    except Exception as e:
        print(f"⚠️ Error saving article to database: {e}")
        return None


def save_sentiment_score_to_db(ticker, score, stats):
    """Save sentiment score to database"""
    try:
        sentiment = SentimentScore.objects.create(
            ticker=ticker,
            score=score,
            articles_analyzed=stats['total_articles'],
            cached_articles=stats['cached'],
            new_articles=stats['new']
        )
        print(f"💾 Saved sentiment score to database: {score:.2f}")
        return sentiment
    except Exception as e:
        print(f"⚠️ Error saving sentiment score: {e}")
        return None


def fetch_and_save_stock_price(finnhub_client, ticker):
    """Fetch current stock price and save to database"""
    try:
        # Get real-time quote from Finnhub
        quote = finnhub_client.quote(ticker.symbol)
        
        if quote and quote.get('c'):  # 'c' is current price
            price_obj = StockPrice.objects.create(
                ticker=ticker,
                price=Decimal(str(quote.get('c', 0))),
                open_price=Decimal(str(quote.get('o', 0))) if quote.get('o') else None,
                high_price=Decimal(str(quote.get('h', 0))) if quote.get('h') else None,
                low_price=Decimal(str(quote.get('l', 0))) if quote.get('l') else None,
                change_percent=float(quote.get('dp', 0)) if quote.get('dp') else None,
            )
            print(f"💰 Stock price saved: ${price_obj.price} (Change: {price_obj.change_percent:.2f}%)")
            return price_obj
        else:
            print(f"⚠️ No price data available for {ticker.symbol}")
            return None
    except Exception as e:
        print(f"⚠️ Error fetching stock price: {e}")
        return None


def update_sentiment_history(ticker):
    """Update daily sentiment history aggregate"""
    try:
        today = timezone.now().date()
        
        # Get today's sentiment scores
        today_scores = SentimentScore.objects.filter(
            ticker=ticker,
            timestamp__date=today
        )
        
        if not today_scores.exists():
            return
        
        # Calculate aggregates
        aggregates = today_scores.aggregate(
            avg=Avg('score'),
            min=Min('score'),
            max=Max('score'),
            total=Count('id')
        )
        
        # Get latest stock price for today
        latest_price = StockPrice.objects.filter(
            ticker=ticker,
            timestamp__date=today
        ).order_by('-timestamp').first()
        
        # Update or create history entry
        history, created = SentimentHistory.objects.update_or_create(
            ticker=ticker,
            date=today,
            defaults={
                'avg_sentiment': aggregates['avg'],
                'min_sentiment': aggregates['min'],
                'max_sentiment': aggregates['max'],
                'total_articles': today_scores.last().articles_analyzed if today_scores.last() else 0,
                'closing_price': latest_price.price if latest_price else None,
                'price_change_percent': float(latest_price.change_percent) if latest_price and latest_price.change_percent else None,
            }
        )
        
        action = "Created" if created else "Updated"
        print(f"📊 {action} sentiment history for {today}")
        
    except Exception as e:
        print(f"⚠️ Error updating sentiment history: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_article_hash(headline, summary):
    """Generate unique hash for article deduplication"""
    content = f"{headline}{summary}".lower()
    return hashlib.md5(content.encode()).hexdigest()


def analyze_sentiment_finbert_api(text):
    """
    Analyze sentiment using FinBERT via HuggingFace API
    Returns: float between -1 (negative) and +1 (positive)
    """
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Truncate text to reasonable length
    text = text[:512]
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        if response.status_code == 200:
            result = response.json()
            
            # HuggingFace returns array of label/score pairs
            sentiment_map = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            for item in result[0]:
                label = item['label'].lower()
                score = item['score']
                sentiment_map[label] = score
            
            # Convert to -1 to +1 scale
            sentiment_score = sentiment_map['positive'] - sentiment_map['negative']
            return sentiment_score
            
        elif response.status_code == 503:
            # Model is loading, wait and retry
            print("  ⏳ Model loading, retrying in 20 seconds...")
            time.sleep(20)
            return analyze_sentiment_finbert_api(text)
        else:
            print(f"  ⚠️ API error: {response.status_code}")
            return 0.0
            
    except Exception as e:
        print(f"  ⚠️ Error analyzing sentiment: {e}")
        return 0.0


def calculate_surprise_factor(text):
    """
    Detect if news is surprising/unexpected
    Returns: multiplier between 0.3 and 2.0
    """
    text_lower = text.lower()
    
    surprise_keywords = {
        'unexpected': 1.5,
        'surprise': 1.5,
        'beats expectations': 1.8,
        'misses estimates': 1.8,
        'exceeds expectations': 1.8,
        'shock': 2.0,
        'unprecedented': 1.7,
        'sudden': 1.4,
        'abrupt': 1.4,
        'breaking': 1.3
    }
    
    expected_keywords = {
        'as expected': 0.4,
        'in line with': 0.4,
        'anticipated': 0.5,
        'scheduled': 0.6,
        'planned': 0.6
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
    """
    Check if article is novel or duplicate
    Returns: score between 0.2 and 1.0
    """
    if article_hash in seen_articles:
        return 0.2
    
    seen_articles.add(article_hash)
    return 1.0


def get_source_credibility(source):
    """
    Get credibility weight for news source
    Returns: weight between 0.4 and 1.0
    """
    for known_source, weight in SOURCE_CREDIBILITY.items():
        if known_source.lower() in source.lower():
            return weight
    
    return 0.5


def calculate_recency_weight(published_timestamp):
    """
    Calculate weight based on how recent the article is
    Returns: weight between 0 and 1.0
    """
    try:
        published_time = datetime.fromtimestamp(published_timestamp)
        hours_old = (datetime.now() - published_time).total_seconds() / 3600
        
        # Exponential decay with 6-hour half-life
        decay_factor = 2 ** (-hours_old / 6)
        
        return max(0, min(1.0, decay_factor))
    except:
        return 0.5


def fetch_news(finnhub_client, ticker_symbol, lookback_hours=24):
    """Fetch recent news from Finnhub"""
    try:
        to_date = datetime.now()
        from_date = to_date - timedelta(hours=lookback_hours)
        
        from_str = from_date.strftime('%Y-%m-%d')
        to_str = to_date.strftime('%Y-%m-%d')
        
        news = finnhub_client.company_news(ticker_symbol, _from=from_str, to=to_str)
        return news
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return []


def calculate_composite_sentiment_score(finnhub_client, ticker):
    """
    Main function to calculate composite sentiment score
    Returns: score from -100 to +100
    """
    print(f"\n{'='*60}")
    print(f"📊 Calculating sentiment score for {ticker.symbol}")
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    articles = fetch_news(finnhub_client, ticker.symbol, lookback_hours=24)
    
    if not articles:
        print("ℹ️  No articles found in the last 24 hours.")
        return 0, {'total_articles': 0, 'cached': 0, 'new': 0}
    
    print(f"📰 Found {len(articles)} articles\n")
    
    weighted_scores = []
    total_weight = 0
    new_articles_count = 0
    cached_articles_count = 0
    
    for idx, article in enumerate(articles):
        headline = article.get('headline', '')
        summary = article.get('summary', '')
        source = article.get('source', 'Unknown')
        published = article.get('datetime', 0)
        
        if not headline and not summary:
            continue
        
        full_text = f"{headline}. {summary}"
        article_hash = get_article_hash(headline, summary)
        
        print(f"📄 Article {idx + 1}:")
        print(f"   Source: {source}")
        print(f"   Headline: {headline[:70]}...")
        
        # Check if we have cached sentiment in database
        cached_sentiment = get_cached_sentiment_from_db(article_hash)
        was_cached = False
        
        if cached_sentiment is not None:
            # Use cached sentiment score
            base_sentiment = cached_sentiment
            cached_articles_count += 1
            was_cached = True
            print(f"   💭 Base Sentiment (DB CACHED): {base_sentiment:.3f} 🚀")
        else:
            # Analyze sentiment with FinBERT
            base_sentiment = analyze_sentiment_finbert_api(full_text)
            new_articles_count += 1
            print(f"   💭 Base Sentiment (NEW): {base_sentiment:.3f}")
        
        # Calculate other factors
        surprise_multiplier = calculate_surprise_factor(full_text)
        print(f"   ⚡ Surprise Factor: {surprise_multiplier:.2f}x")
        
        novelty = calculate_novelty(article_hash)
        print(f"   🆕 Novelty: {novelty:.2f}")
        
        source_cred = get_source_credibility(source)
        print(f"   ✅ Source Credibility: {source_cred:.2f}")
        
        recency = calculate_recency_weight(published)
        print(f"   ⏱️  Recency Weight: {recency:.2f}")
        
        # Combine factors
        article_score = (
            base_sentiment * WEIGHTS['base_sentiment']
        ) * surprise_multiplier
        
        article_weight = (
            novelty * WEIGHTS['novelty'] +
            source_cred * WEIGHTS['source_credibility'] +
            recency * WEIGHTS['recency']
        )
        
        weighted_score = article_score * article_weight
        print(f"   → Article Score: {article_score:.3f}")
        print(f"   → Weighted Contribution: {weighted_score:.3f}\n")
        
        # Save article to database
        sentiment_data = {
            'article_hash': article_hash,
            'base_sentiment': base_sentiment,
            'surprise_factor': surprise_multiplier,
            'novelty': novelty,
            'source_credibility': source_cred,
            'recency': recency,
            'article_score': article_score,
            'weighted_contribution': weighted_score,
            'was_cached': was_cached
        }
        save_news_article_to_db(ticker, article, sentiment_data)
        
        weighted_scores.append(weighted_score)
        total_weight += article_weight
    
    # Calculate final score
    if total_weight == 0:
        final_score = 0
    else:
        final_score = (sum(weighted_scores) / total_weight) * 100
    
    final_score = max(-100, min(100, final_score))
    
    stats = {
        'total_articles': len(articles),
        'cached': cached_articles_count,
        'new': new_articles_count
    }
    
    print(f"{'='*60}")
    print(f"🎯 COMPOSITE SENTIMENT SCORE: {final_score:.2f}")
    print(f"📊 Cache Stats: {cached_articles_count} cached, {new_articles_count} new analyses")
    print(f"{'='*60}\n")
    
    return final_score, stats


# ============================================================================
# DJANGO MANAGEMENT COMMAND
# ============================================================================

class Command(BaseCommand):
    help = 'Run continuous sentiment analysis for NASDAQ stocks with database storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ticker',
            type=str,
            default='AAPL',
            help='Stock ticker to analyze (default: AAPL)'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Update interval in seconds (default: 60)'
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run once instead of continuously'
        )

    def handle(self, *args, **options):
        ticker_symbol = options['ticker'].upper()
        interval = options['interval']
        run_once = options['once']
        
        # Check API keys
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
        
        # Get or create ticker in database
        ticker = get_or_create_ticker(ticker_symbol)
        
        self.stdout.write(self.style.SUCCESS(
            f'\n🚀 Starting sentiment analysis for {ticker.symbol}'
        ))
        self.stdout.write(f'💾 All data will be saved to PostgreSQL database\n')
        
        if run_once:
            # Run once
            score, stats = calculate_composite_sentiment_score(finnhub_client, ticker)
            self.interpret_score(score)
            
            # Save sentiment score to database
            save_sentiment_score_to_db(ticker, score, stats)
            
            # Fetch and save stock price
            fetch_and_save_stock_price(finnhub_client, ticker)
            
            # Update sentiment history
            update_sentiment_history(ticker)
            
            self.stdout.write(self.style.SUCCESS('\n✅ Analysis complete! Data saved to database.'))
        else:
            # Run continuously
            self.stdout.write(f'⏱️  Update interval: {interval} seconds')
            self.stdout.write('⌨️  Press Ctrl+C to stop\n')
            
            iteration = 0
            
            try:
                while True:
                    iteration += 1
                    self.stdout.write(f"\n{'>'*20} ITERATION {iteration} {'<'*20}")
                    
                    score, stats = calculate_composite_sentiment_score(finnhub_client, ticker)
                    self.interpret_score(score)
                    
                    # Save to database
                    save_sentiment_score_to_db(ticker, score, stats)
                    fetch_and_save_stock_price(finnhub_client, ticker)
                    
                    # Update history every iteration
                    update_sentiment_history(ticker)
                    
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
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Current Sentiment: {sentiment}")
        self.stdout.write(f"Score: {score:.2f}/100")
        self.stdout.write(f"{'='*60}")
