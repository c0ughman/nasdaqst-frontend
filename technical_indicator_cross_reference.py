#!/usr/bin/env python3
"""
Technical Indicator Cross-Reference Tool
Scrapes TradingView for NASDAQ Composite (^IXIC) technical indicators
to compare against our internal calculations.
"""

import requests
import json
import time
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import re

class TradingViewScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_nasdaq_technical_data(self):
        """
        Scrape TradingView for NASDAQ Composite technical indicators
        """
        print("🔍 Fetching NASDAQ Composite technical data from TradingView...")
        
        try:
            # TradingView NASDAQ Composite technical analysis page
            url = "https://www.tradingview.com/symbols/NASDAQ-IXIC/technicals/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for technical indicator data in the page
            indicators = self._extract_indicators_from_page(soup)
            
            return indicators
            
        except Exception as e:
            print(f"❌ Error fetching TradingView data: {e}")
            return None
    
    def _extract_indicators_from_page(self, soup):
        """
        Extract technical indicators from TradingView page
        """
        indicators = {}
        
        # Look for various patterns that might contain indicator data
        # This is a simplified extraction - TradingView's actual data might be loaded via JavaScript
        
        # Try to find RSI
        rsi_patterns = soup.find_all(text=re.compile(r'RSI|Relative Strength'))
        if rsi_patterns:
            print("  ✓ Found RSI references")
        
        # Try to find MACD
        macd_patterns = soup.find_all(text=re.compile(r'MACD'))
        if macd_patterns:
            print("  ✓ Found MACD references")
            
        return indicators

def fetch_yahoo_finance_indicators():
    """
    Fetch technical indicators from Yahoo Finance as an alternative
    """
    print("\n📊 Fetching technical data from Yahoo Finance...")
    
    try:
        import yfinance as yf
        
        # Get NASDAQ Composite data
        ticker = yf.Ticker("^IXIC")
        
        # Get 5-minute data for the last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        data = ticker.history(
            start=start_time,
            end=end_time,
            interval='5m'
        )
        
        if data.empty:
            print("  ❌ No data available from Yahoo Finance")
            return None
            
        print(f"  ✓ Retrieved {len(data)} data points from Yahoo Finance")
        
        # Calculate indicators using the same periods as our system
        indicators = calculate_indicators_from_yahoo_data(data)
        
        return indicators
        
    except Exception as e:
        print(f"  ❌ Error fetching Yahoo Finance data: {e}")
        return None

def calculate_indicators_from_yahoo_data(df):
    """
    Calculate technical indicators from Yahoo Finance data
    using the same periods as our system
    """
    print("  📈 Calculating technical indicators...")
    
    try:
        from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
        from ta.trend import MACD, EMAIndicator, SMAIndicator
        from ta.volatility import BollingerBands, AverageTrueRange
        
        indicators = {}
        
        # RSI (14 periods)
        if len(df) >= 14:
            rsi = RSIIndicator(close=df['Close'], window=14)
            indicators['rsi_14'] = round(float(rsi.rsi().iloc[-1]), 2)
            print(f"    ✓ RSI(14): {indicators['rsi_14']}")
        
        # MACD (12, 26, 9)
        if len(df) >= 26:
            macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
            indicators['macd'] = round(float(macd.macd().iloc[-1]), 4)
            indicators['macd_signal'] = round(float(macd.macd_signal().iloc[-1]), 4)
            indicators['macd_histogram'] = round(float(macd.macd_diff().iloc[-1]), 4)
            print(f"    ✓ MACD: {indicators['macd']}, Signal: {indicators['macd_signal']}, Histogram: {indicators['macd_histogram']}")
        
        # Bollinger Bands (20 periods, 2 std dev)
        if len(df) >= 20:
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2.0)
            indicators['bb_upper'] = round(float(bb.bollinger_hband().iloc[-1]), 2)
            indicators['bb_middle'] = round(float(bb.bollinger_mavg().iloc[-1]), 2)
            indicators['bb_lower'] = round(float(bb.bollinger_lband().iloc[-1]), 2)
            print(f"    ✓ Bollinger Bands: Upper={indicators['bb_upper']}, Middle={indicators['bb_middle']}, Lower={indicators['bb_lower']}")
        
        # Moving Averages
        if len(df) >= 50:
            # SMA
            sma_20 = SMAIndicator(close=df['Close'], window=20)
            sma_50 = SMAIndicator(close=df['Close'], window=50)
            indicators['sma_20'] = round(float(sma_20.sma_indicator().iloc[-1]), 2)
            indicators['sma_50'] = round(float(sma_50.sma_indicator().iloc[-1]), 2)
            print(f"    ✓ SMA(20): {indicators['sma_20']}, SMA(50): {indicators['sma_50']}")
            
            # EMA
            ema_9 = EMAIndicator(close=df['Close'], window=9)
            ema_20 = EMAIndicator(close=df['Close'], window=20)
            indicators['ema_9'] = round(float(ema_9.ema_indicator().iloc[-1]), 2)
            indicators['ema_20'] = round(float(ema_20.ema_indicator().iloc[-1]), 2)
            print(f"    ✓ EMA(9): {indicators['ema_9']}, EMA(20): {indicators['ema_20']}")
        
        # Stochastic (14, 3, 3)
        if len(df) >= 14:
            stoch = StochasticOscillator(
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                window=14,
                smooth_window=3
            )
            indicators['stoch_k'] = round(float(stoch.stoch().iloc[-1]), 2)
            indicators['stoch_d'] = round(float(stoch.stoch_signal().iloc[-1]), 2)
            print(f"    ✓ Stochastic %K: {indicators['stoch_k']}, %D: {indicators['stoch_d']}")
        
        # Williams %R (14 periods)
        if len(df) >= 14:
            williams = WilliamsRIndicator(high=df['High'], low=df['Low'], close=df['Close'], lbp=14)
            indicators['williams_r'] = round(float(williams.williams_r().iloc[-1]), 2)
            print(f"    ✓ Williams %R: {indicators['williams_r']}")
        
        # ATR (14 periods)
        if len(df) >= 14:
            atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
            indicators['atr_14'] = round(float(atr.average_true_range().iloc[-1]), 2)
            print(f"    ✓ ATR(14): {indicators['atr_14']}")
        
        # Current price
        indicators['current_price'] = round(float(df['Close'].iloc[-1]), 2)
        print(f"    ✓ Current Price: {indicators['current_price']}")
        
        return indicators
        
    except Exception as e:
        print(f"    ❌ Error calculating indicators: {e}")
        return None

def fetch_investing_com_data():
    """
    Alternative: Fetch data from Investing.com
    """
    print("\n📊 Fetching data from Investing.com...")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        url = "https://www.investing.com/technical/nasdaq-composite-technical-analysis"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for technical analysis data
        print("  ✓ Retrieved Investing.com page")
        
        # This would need more specific parsing based on their HTML structure
        return None
        
    except Exception as e:
        print(f"  ❌ Error fetching Investing.com data: {e}")
        return None

def compare_with_our_data():
    """
    Compare external data with our internal calculations
    """
    print("\n🔄 Comparing with our internal data...")
    
    try:
        # Set up Django environment
        import os
        import sys
        import django
        
        # Add the backend directory to Python path
        backend_path = '/Users/coughman/Desktop/Nasdaq Sentiment Tracker/backend'
        sys.path.append(backend_path)
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        # Import our technical indicators module
        sys.path.append('/Users/coughman/Desktop/Nasdaq Sentiment Tracker/backend/api/management/commands')
        
        from technical_indicators import calculate_all_indicators
        from nasdaq_config import INDICATOR_PERIODS
        
        # Get our internal calculations
        our_indicators = calculate_all_indicators(
            symbol='^IXIC',
            resolution='5',
            hours_back=24,
            config=INDICATOR_PERIODS
        )
        
        print("  ✓ Retrieved our internal calculations")
        return our_indicators
        
    except Exception as e:
        print(f"  ❌ Error getting our internal data: {e}")
        return None

def main():
    """
    Main function to run the cross-reference comparison
    """
    print("=" * 80)
    print("🔍 TECHNICAL INDICATOR CROSS-REFERENCE TOOL")
    print("=" * 80)
    print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Symbol: ^IXIC (NASDAQ Composite)")
    print(f"⏱️  Timeframe: 5-minute candles")
    print(f"📈 Lookback: 24 hours")
    print("=" * 80)
    
    # Fetch external data
    yahoo_indicators = fetch_yahoo_finance_indicators()
    
    # Get our internal data
    our_indicators = compare_with_our_data()
    
    # Display comparison
    print("\n" + "=" * 80)
    print("📊 COMPARISON RESULTS")
    print("=" * 80)
    
    if yahoo_indicators and our_indicators:
        print(f"{'Indicator':<20} {'Yahoo Finance':<15} {'Our System':<15} {'Difference':<15}")
        print("-" * 70)
        
        for key in yahoo_indicators:
            if key in our_indicators:
                yahoo_val = yahoo_indicators[key]
                our_val = our_indicators[key]
                
                if yahoo_val is not None and our_val is not None:
                    diff = abs(yahoo_val - our_val)
                    print(f"{key:<20} {yahoo_val:<15} {our_val:<15} {diff:<15.4f}")
                else:
                    print(f"{key:<20} {str(yahoo_val):<15} {str(our_val):<15} {'N/A':<15}")
    
    print("\n" + "=" * 80)
    print("✅ Cross-reference analysis complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
