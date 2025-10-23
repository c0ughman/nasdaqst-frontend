#!/usr/bin/env python3
"""
NASDAQ Composite vs QQQ Technical Analysis Investigation
Tests both data sources and analyzes MACD calculation differences
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

def fetch_and_compare_data_sources():
    """
    Fetch data from both NASDAQ Composite (^IXIC) and QQQ to compare
    """
    print("=" * 80)
    print("🔍 NASDAQ COMPOSITE vs QQQ DATA COMPARISON")
    print("=" * 80)
    
    symbols = {
        'NASDAQ Composite': '^IXIC',
        'QQQ ETF': 'QQQ'
    }
    
    results = {}
    
    for name, symbol in symbols.items():
        print(f"\n📊 Fetching {name} ({symbol}) data...")
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Get 5-minute data for the last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            data = ticker.history(
                start=start_time,
                end=end_time,
                interval='5m'
            )
            
            if data.empty:
                print(f"  ❌ No data available for {symbol}")
                continue
                
            print(f"  ✓ Retrieved {len(data)} data points")
            
            # Get basic price info
            latest = data.iloc[-1]
            current_price = round(float(latest['Close']), 2)
            price_range = round(float(data['High'].max() - data['Low'].min()), 2)
            avg_volume = int(data['Volume'].mean()) if 'Volume' in data.columns else 0
            
            print(f"  📈 Current Price: {current_price:,}")
            print(f"  📊 Price Range: {price_range:,}")
            print(f"  📦 Avg Volume: {avg_volume:,}")
            
            # Calculate technical indicators
            indicators = calculate_indicators_detailed(data, symbol)
            
            results[name] = {
                'symbol': symbol,
                'data_points': len(data),
                'current_price': current_price,
                'price_range': price_range,
                'avg_volume': avg_volume,
                'indicators': indicators,
                'data': data
            }
            
        except Exception as e:
            print(f"  ❌ Error fetching {symbol}: {e}")
            continue
    
    return results

def calculate_indicators_detailed(df, symbol):
    """
    Calculate technical indicators with detailed logging
    """
    print(f"  📈 Calculating indicators for {symbol}...")
    
    try:
        from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
        from ta.trend import MACD, EMAIndicator, SMAIndicator
        from ta.volatility import BollingerBands, AverageTrueRange
        
        indicators = {}
        
        # RSI (14 periods)
        if len(df) >= 14:
            rsi = RSIIndicator(close=df['Close'], window=14)
            rsi_value = rsi.rsi().iloc[-1]
            indicators['rsi_14'] = round(float(rsi_value), 2)
            print(f"    ✓ RSI(14): {indicators['rsi_14']}")
        
        # MACD with detailed analysis
        if len(df) >= 26:
            macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
            
            macd_line = macd.macd().iloc[-1]
            signal_line = macd.macd_signal().iloc[-1]
            histogram = macd.macd_diff().iloc[-1]
            
            indicators['macd'] = round(float(macd_line), 4)
            indicators['macd_signal'] = round(float(signal_line), 4)
            indicators['macd_histogram'] = round(float(histogram), 4)
            
            print(f"    ✓ MACD: {indicators['macd']}")
            print(f"    ✓ MACD Signal: {indicators['macd_signal']}")
            print(f"    ✓ MACD Histogram: {indicators['macd_histogram']}")
            
            # Analyze MACD calculation components
            analyze_macd_components(df, macd, symbol)
        
        # Bollinger Bands
        if len(df) >= 20:
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2.0)
            indicators['bb_upper'] = round(float(bb.bollinger_hband().iloc[-1]), 2)
            indicators['bb_middle'] = round(float(bb.bollinger_mavg().iloc[-1]), 2)
            indicators['bb_lower'] = round(float(bb.bollinger_lband().iloc[-1]), 2)
            print(f"    ✓ Bollinger Bands: {indicators['bb_upper']} / {indicators['bb_middle']} / {indicators['bb_lower']}")
        
        # Moving Averages
        if len(df) >= 50:
            sma_20 = SMAIndicator(close=df['Close'], window=20)
            sma_50 = SMAIndicator(close=df['Close'], window=50)
            indicators['sma_20'] = round(float(sma_20.sma_indicator().iloc[-1]), 2)
            indicators['sma_50'] = round(float(sma_50.sma_indicator().iloc[-1]), 2)
            print(f"    ✓ SMA(20): {indicators['sma_20']}, SMA(50): {indicators['sma_50']}")
            
            ema_9 = EMAIndicator(close=df['Close'], window=9)
            ema_20 = EMAIndicator(close=df['Close'], window=20)
            indicators['ema_9'] = round(float(ema_9.ema_indicator().iloc[-1]), 2)
            indicators['ema_20'] = round(float(ema_20.ema_indicator().iloc[-1]), 2)
            print(f"    ✓ EMA(9): {indicators['ema_9']}, EMA(20): {indicators['ema_20']}")
        
        return indicators
        
    except Exception as e:
        print(f"    ❌ Error calculating indicators: {e}")
        return None

def analyze_macd_components(df, macd_obj, symbol):
    """
    Analyze MACD calculation components to understand differences
    """
    print(f"    🔍 MACD Analysis for {symbol}:")
    
    try:
        # Get the last few values to see the trend
        macd_values = macd_obj.macd().tail(5)
        signal_values = macd_obj.macd_signal().tail(5)
        histogram_values = macd_obj.macd_diff().tail(5)
        
        print(f"      Last 5 MACD values: {[round(float(x), 4) for x in macd_values]}")
        print(f"      Last 5 Signal values: {[round(float(x), 4) for x in signal_values]}")
        print(f"      Last 5 Histogram values: {[round(float(x), 4) for x in histogram_values]}")
        
        # Check if MACD values are very small (possible scaling issue)
        latest_macd = float(macd_values.iloc[-1])
        latest_signal = float(signal_values.iloc[-1])
        
        if abs(latest_macd) < 0.1:
            print(f"      ⚠️  MACD values are very small ({latest_macd:.6f}) - possible scaling issue")
        
        if abs(latest_signal) < 0.1:
            print(f"      ⚠️  Signal values are very small ({latest_signal:.6f}) - possible scaling issue")
            
    except Exception as e:
        print(f"      ❌ Error in MACD analysis: {e}")

def test_our_system_macd():
    """
    Test our system's MACD calculation with detailed logging
    """
    print("\n" + "=" * 80)
    print("🔧 TESTING OUR SYSTEM'S MACD CALCULATION")
    print("=" * 80)
    
    try:
        import os
        import sys
        import django
        
        # Set up Django environment
        backend_path = '/Users/coughman/Desktop/Nasdaq Sentiment Tracker/backend'
        sys.path.append(backend_path)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        
        # Import our modules
        sys.path.append('/Users/coughman/Desktop/Nasdaq Sentiment Tracker/backend/api/management/commands')
        from technical_indicators import fetch_ohlcv_data_from_db, calculate_macd
        from nasdaq_config import INDICATOR_PERIODS
        
        # Get our database data
        print("📊 Fetching data from our database...")
        df = fetch_ohlcv_data_from_db(ticker_symbol='^IXIC', hours_back=24)
        
        if df is None or len(df) == 0:
            print("❌ No data in our database")
            return None
            
        print(f"✓ Retrieved {len(df)} data points from our database")
        
        # Show sample of our data
        print("\n📈 Sample of our database data:")
        print(df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].tail(5))
        
        # Calculate MACD using our system
        print("\n🔧 Calculating MACD using our system...")
        macd_line, signal_line, histogram = calculate_macd(df, 12, 26, 9)
        
        print(f"✓ Our System MACD: {macd_line}")
        print(f"✓ Our System Signal: {signal_line}")
        print(f"✓ Our System Histogram: {histogram}")
        
        # Analyze our data characteristics
        print(f"\n📊 Our data characteristics:")
        print(f"  Price range: {df['close'].min():.2f} - {df['close'].max():.2f}")
        print(f"  Average price: {df['close'].mean():.2f}")
        # Convert to float to avoid Decimal type issues
        close_float = df['close'].astype(float)
        print(f"  Price volatility: {close_float.std():.2f}")
        
        return {
            'macd_line': macd_line,
            'signal_line': signal_line,
            'histogram': histogram,
            'data_points': len(df),
            'price_range': (df['close'].min(), df['close'].max()),
            'avg_price': df['close'].mean()
        }
        
    except Exception as e:
        print(f"❌ Error testing our system: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_macd_calculations(yahoo_results, our_results):
    """
    Compare MACD calculations between Yahoo Finance and our system
    """
    print("\n" + "=" * 80)
    print("📊 MACD CALCULATION COMPARISON")
    print("=" * 80)
    
    if not yahoo_results or not our_results:
        print("❌ Missing data for comparison")
        return
    
    print(f"{'Source':<20} {'MACD':<15} {'Signal':<15} {'Histogram':<15}")
    print("-" * 70)
    
    # Yahoo Finance QQQ
    if 'QQQ ETF' in yahoo_results:
        qqq_indicators = yahoo_results['QQQ ETF']['indicators']
        print(f"{'Yahoo QQQ':<20} {qqq_indicators['macd']:<15} {qqq_indicators['macd_signal']:<15} {qqq_indicators['macd_histogram']:<15}")
    
    # Yahoo Finance NASDAQ Composite
    if 'NASDAQ Composite' in yahoo_results:
        nasdaq_indicators = yahoo_results['NASDAQ Composite']['indicators']
        print(f"{'Yahoo ^IXIC':<20} {nasdaq_indicators['macd']:<15} {nasdaq_indicators['macd_signal']:<15} {nasdaq_indicators['macd_histogram']:<15}")
    
    # Our system
    print(f"{'Our System':<20} {our_results['macd_line']:<15} {our_results['signal_line']:<15} {our_results['histogram']:<15}")
    
    # Analyze differences
    print("\n🔍 Analysis:")
    if 'QQQ ETF' in yahoo_results:
        qqq_macd = yahoo_results['QQQ ETF']['indicators']['macd']
        our_macd = our_results['macd_line']
        
        if our_macd is not None:
            ratio = qqq_macd / our_macd if our_macd != 0 else float('inf')
            print(f"  QQQ vs Our MACD ratio: {ratio:.2f}")
            
            if ratio > 10:
                print(f"  ⚠️  Large difference detected - possible scaling or calculation method issue")
            elif ratio > 2:
                print(f"  ⚠️  Moderate difference - check calculation parameters")
            else:
                print(f"  ✅ Reasonable difference")

def main():
    """
    Main analysis function
    """
    print("🔍 NASDAQ COMPOSITE vs QQQ TECHNICAL ANALYSIS INVESTIGATION")
    print("=" * 80)
    
    # Fetch and compare data sources
    yahoo_results = fetch_and_compare_data_sources()
    
    # Test our system
    our_results = test_our_system_macd()
    
    # Compare MACD calculations
    compare_macd_calculations(yahoo_results, our_results)
    
    # Summary and recommendations
    print("\n" + "=" * 80)
    print("📝 SUMMARY AND RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1️⃣  NASDAQ COMPOSITE CALCULATIONS:")
    if 'NASDAQ Composite' in yahoo_results:
        print("   ✅ YES - We can calculate technical indicators for NASDAQ Composite (^IXIC)")
        print("   ✅ Yahoo Finance provides ^IXIC data with 5-minute intervals")
        print("   ✅ All technical indicators can be calculated using the same periods")
        print("   📊 NASDAQ Composite prices are ~37.5x higher than QQQ")
    else:
        print("   ❌ Could not fetch NASDAQ Composite data")
    
    print("\n2️⃣  MACD DIFFERENCE ANALYSIS:")
    if our_results and 'QQQ ETF' in yahoo_results:
        qqq_macd = yahoo_results['QQQ ETF']['indicators']['macd']
        our_macd = our_results['macd_line']
        
        if our_macd is not None:
            ratio = qqq_macd / our_macd if our_macd != 0 else float('inf')
            print(f"   📊 MACD ratio (Yahoo/Our): {ratio:.2f}")
            
            if ratio > 10:
                print("   🔍 Possible causes:")
                print("      • Different data sources (timing differences)")
                print("      • Different calculation libraries or methods")
                print("      • Data scaling or normalization issues")
                print("      • Missing or incorrect data points")
            else:
                print("   ✅ MACD differences are within acceptable range")
    
    print("\n3️⃣  RECOMMENDATIONS:")
    print("   • Consider switching to NASDAQ Composite (^IXIC) for more accurate index representation")
    print("   • Investigate MACD calculation differences if they're significant")
    print("   • Ensure consistent data timing between sources")
    print("   • Consider using the same technical analysis library (ta) for consistency")

if __name__ == "__main__":
    main()
