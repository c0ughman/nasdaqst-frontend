from django.db import models
from django.contrib.auth.models import User


class Ticker(models.Model):
    """Stock ticker information"""
    symbol = models.CharField(max_length=10, unique=True, db_index=True)
    company_name = models.CharField(max_length=200, blank=True)
    exchange = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['symbol']
        verbose_name = "Ticker"
        verbose_name_plural = "Tickers"
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}" if self.company_name else self.symbol


class SentimentScore(models.Model):
    """Sentiment score for a ticker at a specific time"""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name='sentiment_scores')
    score = models.FloatField(help_text="Sentiment score from -100 to 100")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Additional metrics
    articles_analyzed = models.IntegerField(default=0)
    cached_articles = models.IntegerField(default=0)
    new_articles = models.IntegerField(default=0)
    
    # Sentiment classification
    SENTIMENT_CHOICES = [
        ('STRONGLY_BULLISH', 'Strongly Bullish'),
        ('BULLISH', 'Bullish'),
        ('NEUTRAL', 'Neutral'),
        ('BEARISH', 'Bearish'),
        ('STRONGLY_BEARISH', 'Strongly Bearish'),
    ]
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Sentiment Score"
        verbose_name_plural = "Sentiment Scores"
        indexes = [
            models.Index(fields=['ticker', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.ticker.symbol} - {self.score:.2f} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate sentiment label based on score"""
        if self.score > 50:
            self.sentiment_label = 'STRONGLY_BULLISH'
        elif self.score > 20:
            self.sentiment_label = 'BULLISH'
        elif self.score > -20:
            self.sentiment_label = 'NEUTRAL'
        elif self.score > -50:
            self.sentiment_label = 'BEARISH'
        else:
            self.sentiment_label = 'STRONGLY_BEARISH'
        super().save(*args, **kwargs)


class StockPrice(models.Model):
    """Stock price data"""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name='stock_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current stock price")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Additional price data (optional)
    open_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    high_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    change_percent = models.FloatField(null=True, blank=True, help_text="Percentage change")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Stock Price"
        verbose_name_plural = "Stock Prices"
        indexes = [
            models.Index(fields=['ticker', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.ticker.symbol} - ${self.price} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class NewsArticle(models.Model):
    """News article with sentiment analysis"""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name='news_articles')
    
    # Article information
    headline = models.TextField()
    summary = models.TextField(blank=True)
    source = models.CharField(max_length=100)
    url = models.URLField(max_length=500, blank=True)
    published_at = models.DateTimeField(db_index=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    # Unique identifier to prevent duplicates
    article_hash = models.CharField(max_length=32, unique=True, db_index=True)
    
    # Sentiment analysis results
    base_sentiment = models.FloatField(help_text="Base sentiment from -1 to 1")
    surprise_factor = models.FloatField(default=1.0)
    novelty_score = models.FloatField(default=1.0)
    source_credibility = models.FloatField(default=0.5)
    recency_weight = models.FloatField(default=1.0)
    article_score = models.FloatField(help_text="Calculated article score")
    weighted_contribution = models.FloatField(help_text="Contribution to composite score")
    
    # Status
    is_analyzed = models.BooleanField(default=False)
    sentiment_cached = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        indexes = [
            models.Index(fields=['ticker', '-published_at']),
            models.Index(fields=['article_hash']),
        ]
    
    def __str__(self):
        return f"{self.ticker.symbol} - {self.headline[:50]}... ({self.published_at.strftime('%Y-%m-%d')})"


class SentimentHistory(models.Model):
    """Aggregated historical sentiment data for charting/analysis"""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name='sentiment_history')
    date = models.DateField(db_index=True)
    
    # Daily aggregates
    avg_sentiment = models.FloatField(help_text="Average sentiment score for the day")
    min_sentiment = models.FloatField(help_text="Minimum sentiment score")
    max_sentiment = models.FloatField(help_text="Maximum sentiment score")
    total_articles = models.IntegerField(default=0)
    
    # Stock price on that day
    closing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_change_percent = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Sentiment History"
        verbose_name_plural = "Sentiment History"
        unique_together = ['ticker', 'date']
        indexes = [
            models.Index(fields=['ticker', '-date']),
        ]
    
    def __str__(self):
        return f"{self.ticker.symbol} - {self.date} (Avg: {self.avg_sentiment:.2f})"


# Keep the example model for reference
class Example(models.Model):
    """
    Example model to demonstrate Django admin integration.
    Delete this and create your own models as needed.
    """
    title = models.CharField(max_length=200, help_text="Title of the example")
    description = models.TextField(blank=True, help_text="Description of the example")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='examples',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is this example active?")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Example"
        verbose_name_plural = "Examples"
    
    def __str__(self):
        return self.title

