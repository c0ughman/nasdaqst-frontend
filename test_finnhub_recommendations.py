#!/usr/bin/env python3
"""
Quick test script to fetch Finnhub recommendations and see what's available
"""

import os
import finnhub
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY', '')

if not FINNHUB_API_KEY:
    print("❌ FINNHUB_API_KEY not found in environment variables")
    exit(1)

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# Test symbols for recommendations
test_symbols = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'TSLA']

print("🔍 Fetching Finnhub Recommendations Data...")
print("=" * 60)

for symbol in test_symbols:
    print(f"\n📊 {symbol} - Recommendations:")
    try:
        # Fetch recommendations
        recommendations = finnhub_client.recommendation_trends(symbol)
        
        if recommendations:
            print(f"  ✅ Found {len(recommendations)} recommendation entries")
            
            # Show the most recent recommendation
            latest = recommendations[0]
            print(f"  📅 Date: {latest.get('period', 'N/A')}")
            print(f"  📈 Strong Buy: {latest.get('strongBuy', 0)}")
            print(f"  📈 Buy: {latest.get('buy', 0)}")
            print(f"  ➡️ Hold: {latest.get('hold', 0)}")
            print(f"  📉 Sell: {latest.get('sell', 0)}")
            print(f"  📉 Strong Sell: {latest.get('strongSell', 0)}")
            
            # Calculate consensus
            total = (latest.get('strongBuy', 0) + 
                    latest.get('buy', 0) + 
                    latest.get('hold', 0) + 
                    latest.get('sell', 0) + 
                    latest.get('strongSell', 0))
            
            if total > 0:
                buy_score = (latest.get('strongBuy', 0) * 2 + latest.get('buy', 0)) / (total * 2)
                sell_score = (latest.get('strongSell', 0) * 2 + latest.get('sell', 0)) / (total * 2)
                
                print(f"  🎯 Buy Score: {buy_score:.2%}")
                print(f"  🎯 Sell Score: {sell_score:.2%}")
                
                if buy_score > sell_score:
                    print(f"  💡 Consensus: BULLISH")
                elif sell_score > buy_score:
                    print(f"  💡 Consensus: BEARISH")
                else:
                    print(f"  💡 Consensus: NEUTRAL")
        else:
            print(f"  ❌ No recommendations found for {symbol}")
            
    except Exception as e:
        print(f"  ⚠️ Error fetching recommendations for {symbol}: {e}")

print("\n" + "=" * 60)
print("🔍 Testing other Finnhub recommendation endpoints...")

# Test company recommendation trends
print("\n📊 Testing recommendation_trends endpoint:")
try:
    trends = finnhub_client.recommendation_trends('AAPL')
    if trends:
        print(f"  ✅ recommendation_trends works - found {len(trends)} entries")
        print(f"  📋 Sample data structure: {list(trends[0].keys()) if trends else 'None'}")
    else:
        print("  ❌ No data returned from recommendation_trends")
except Exception as e:
    print(f"  ⚠️ Error with recommendation_trends: {e}")

# Test company profile for additional data
print("\n📊 Testing company_profile2 endpoint:")
try:
    profile = finnhub_client.company_profile2(symbol='AAPL')
    if profile:
        print(f"  ✅ company_profile2 works")
        print(f"  📋 Available fields: {list(profile.keys()) if profile else 'None'}")
    else:
        print("  ❌ No data returned from company_profile2")
except Exception as e:
    print(f"  ⚠️ Error with company_profile2: {e}")

print("\n🎉 Finnhub Recommendations Test Complete!")
