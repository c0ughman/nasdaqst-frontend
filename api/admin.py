from django.contrib import admin
from .models import Ticker, SentimentScore, StockPrice, NewsArticle, SentimentHistory, Example


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    """Admin configuration for Ticker model"""
    list_display = ['symbol', 'company_name', 'exchange', 'created_at']
    search_fields = ['symbol', 'company_name']
    list_filter = ['exchange', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SentimentScore)
class SentimentScoreAdmin(admin.ModelAdmin):
    """Admin configuration for SentimentScore model"""
    list_display = ['ticker', 'score', 'sentiment_label', 'articles_analyzed', 'timestamp']
    list_filter = ['sentiment_label', 'timestamp', 'ticker']
    search_fields = ['ticker__symbol']
    readonly_fields = ['timestamp', 'sentiment_label']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Ticker & Score', {
            'fields': ('ticker', 'score', 'sentiment_label', 'timestamp')
        }),
        ('Analysis Statistics', {
            'fields': ('articles_analyzed', 'cached_articles', 'new_articles')
        }),
    )


@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    """Admin configuration for StockPrice model"""
    list_display = ['ticker', 'price', 'change_percent', 'volume', 'timestamp']
    list_filter = ['ticker', 'timestamp']
    search_fields = ['ticker__symbol']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ticker', 'price', 'timestamp')
        }),
        ('Price Details', {
            'fields': ('open_price', 'high_price', 'low_price', 'change_percent', 'volume'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    """Admin configuration for NewsArticle model"""
    list_display = ['ticker', 'headline_short', 'source', 'base_sentiment', 'published_at', 'is_analyzed']
    list_filter = ['ticker', 'source', 'is_analyzed', 'sentiment_cached', 'published_at']
    search_fields = ['headline', 'summary', 'ticker__symbol', 'source']
    readonly_fields = ['article_hash', 'fetched_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Article Information', {
            'fields': ('ticker', 'headline', 'summary', 'source', 'url', 'published_at', 'fetched_at')
        }),
        ('Identification', {
            'fields': ('article_hash',),
            'classes': ('collapse',)
        }),
        ('Sentiment Analysis', {
            'fields': ('base_sentiment', 'surprise_factor', 'novelty_score', 
                      'source_credibility', 'recency_weight', 'article_score', 
                      'weighted_contribution')
        }),
        ('Status', {
            'fields': ('is_analyzed', 'sentiment_cached')
        }),
    )
    
    def headline_short(self, obj):
        """Return shortened headline for list display"""
        return obj.headline[:60] + '...' if len(obj.headline) > 60 else obj.headline
    headline_short.short_description = 'Headline'


@admin.register(SentimentHistory)
class SentimentHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for SentimentHistory model"""
    list_display = ['ticker', 'date', 'avg_sentiment', 'total_articles', 'closing_price', 'price_change_percent']
    list_filter = ['ticker', 'date']
    search_fields = ['ticker__symbol']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ticker', 'date')
        }),
        ('Sentiment Metrics', {
            'fields': ('avg_sentiment', 'min_sentiment', 'max_sentiment', 'total_articles')
        }),
        ('Stock Price', {
            'fields': ('closing_price', 'price_change_percent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    """
    Admin configuration for Example model.
    This shows how to customize the admin interface.
    """
    list_display = ['title', 'created_by', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user if not set."""
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

