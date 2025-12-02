# Chart Settings by Timeframe

This document details the configuration for each chart timeframe, including candle sizes, update frequencies, and other settings.

## Overview

The charts support multiple timeframes with different data sources:
- **Granular data** (1-second or 100-tick candles) for shorter timeframes (1m, 5m, 15m, 30m, 1h)
- **Regular sentiment data** for all timeframes
- **Extended datasets** (2d, 3d) for longer timeframes

---

## Timeframe Configurations

### 1 Minute (1m)
- **Time Frame**: Last 1 minute of data
- **Candle Size**: 
  - **With granular data (Second mode)**: 1-second candles (60 candles total)
  - **With granular data (Tick mode)**: 100-tick candles (variable count)
  - **Without granular data**: Uses regular sentiment dataset
- **Update Frequency**: 
  - **Granular mode**: 1 second (1000ms interval)
  - **Regular mode**: 60 seconds
- **Supports Granular Data**: ✅ Yes
- **Aggregation**: None (full 1-second resolution)
- **Label Count**: 5 time labels
- **Dataset**: `sentimentDataset` (or granular datasets when enabled)

---

### 5 Minutes (5m)
- **Time Frame**: Last 5 minutes of data
- **Candle Size**: 
  - **With granular data (Second mode)**: 
    - 1-second candles if dataset ≤ 60 candles
    - **5-second aggregated candles** if dataset > 60 candles
  - **With granular data (Tick mode)**: 100-tick candles (variable count)
  - **Without granular data**: Uses regular sentiment dataset
- **Update Frequency**: 
  - **Granular mode**: 1 second (1000ms interval)
  - **Regular mode**: 60 seconds
- **Supports Granular Data**: ✅ Yes
- **Aggregation**: 5-second intervals when needed (reduces point count)
- **Label Count**: 5 time labels
- **Dataset**: `sentimentDataset` (or granular datasets when enabled)

---

### 15 Minutes (15m)
- **Time Frame**: Last 15 minutes of data
- **Candle Size**: 
  - **With granular data (Second mode)**: 
    - 1-second candles if dataset ≤ 180 candles
    - **5-second aggregated candles** if dataset > 180 candles
  - **With granular data (Tick mode)**: 100-tick candles (variable count)
  - **Without granular data**: Uses regular sentiment dataset
- **Update Frequency**: 
  - **Granular mode**: 1 second (1000ms interval)
  - **Regular mode**: 60 seconds
- **Supports Granular Data**: ✅ Yes
- **Aggregation**: 5-second intervals when needed (reduces point count)
- **Label Count**: 5 time labels
- **Dataset**: `sentimentDataset` (or granular datasets when enabled)

---

### 30 Minutes (30m)
- **Time Frame**: Last 30 minutes of data
- **Candle Size**: 
  - **With granular data (Second mode)**: 
    - 1-second candles if dataset ≤ 120 candles
    - **30-second aggregated candles** if dataset > 120 candles
  - **With granular data (Tick mode)**: 100-tick candles (variable count)
  - **Without granular data**: Uses regular sentiment dataset
- **Update Frequency**: 
  - **Granular mode**: 1 second (1000ms interval)
  - **Regular mode**: 60 seconds
- **Supports Granular Data**: ✅ Yes
- **Aggregation**: 30-second intervals when needed (reduces point count)
- **Label Count**: 6 time labels
- **Dataset**: `sentimentDataset` (or granular datasets when enabled)

---

### 1 Hour (1h)
- **Time Frame**: Last 1 hour of data
- **Candle Size**: 
  - **With granular data (Second mode)**: 
    - 1-second candles if dataset ≤ 120 candles
    - **30-second aggregated candles** if dataset > 120 candles
  - **With granular data (Tick mode)**: 100-tick candles (variable count)
  - **Without granular data**: Uses regular sentiment dataset
- **Update Frequency**: 
  - **Granular mode**: 1 second (1000ms interval)
  - **Regular mode**: 60 seconds
- **Supports Granular Data**: ✅ Yes
- **Aggregation**: 30-second intervals when needed (reduces point count)
- **Label Count**: 5 time labels
- **Dataset**: `sentimentDataset` (or granular datasets when enabled)

---

### 2 Hours (2h)
- **Time Frame**: Last 2 hours of data
- **Candle Size**: Uses regular sentiment dataset (no granular data support)
- **Update Frequency**: 60 seconds
- **Supports Granular Data**: ❌ No
- **Aggregation**: N/A
- **Label Count**: 6 time labels
- **Dataset**: `sentimentDataset`

---

### 4 Hours (4h)
- **Time Frame**: Last 4 hours of data
- **Candle Size**: Uses regular sentiment dataset (no granular data support)
- **Update Frequency**: 60 seconds
- **Supports Granular Data**: ❌ No
- **Aggregation**: N/A
- **Label Count**: 6 time labels
- **Dataset**: `sentimentDataset`

---

### Session (6h)
- **Time Frame**: Current trading day (9:30 AM - 4:00 PM ET)
- **Candle Size**: Uses regular sentiment dataset (no granular data support)
- **Update Frequency**: 60 seconds
- **Supports Granular Data**: ❌ No
- **Aggregation**: N/A
- **Label Count**: 6 time labels
- **Dataset**: `sentimentDataset`
- **Special Behavior**: Shows only current trading day, not rolling 6-hour window

---

### 2 Days (2d)
- **Time Frame**: Last 48 hours (2 complete trading days)
- **Candle Size**: Uses extended 2-day dataset
- **Update Frequency**: 60 seconds
- **Supports Granular Data**: ❌ No
- **Aggregation**: N/A
- **Label Count**: 8 time labels
- **Dataset**: `sentimentDataset2d`
- **Special Behavior**: Shows last 2 complete trading days (yesterday + today)

---

### 3 Days (3d)
- **Time Frame**: Last 72 hours (3 complete trading days)
- **Candle Size**: Uses extended 3-day dataset
- **Update Frequency**: 60 seconds
- **Supports Granular Data**: ❌ No
- **Aggregation**: N/A
- **Label Count**: 10 time labels
- **Dataset**: `sentimentDataset3d`
- **Special Behavior**: Shows last 3 complete trading days

---

## Update Frequency Details

### Granular Data Refresh (1 second)
- **Interval**: 1000ms (1 second)
- **Applies to**: Timeframes with `supportsGranular: true` (1m, 5m, 15m, 30m, 1h)
- **Conditions**:
  - Only refreshes when market is open
  - Only refreshes when user is viewing most recent data (scrollPosition = 100%)
  - Stops automatically when user scrolls to historical data
- **Data Source**: 
  - Second candles: `/second-candles/` endpoint
  - Tick candles: `/tick-candles/` endpoint

### Regular Data Refresh (60 seconds)
- **Interval**: 60000ms (60 seconds)
- **Applies to**: All timeframes
- **Conditions**:
  - Only refreshes when market is open
  - Only updates chart when user is viewing most recent data (scrollPosition = 100%)
  - Does not interrupt historical viewing
- **Data Source**: Main sentiment dataset endpoints

---

## Candle Visualization Settings

### Candlestick Display
- **Style**: Heikin-Ashi candlesticks
- **Candle Width**: 
  - Calculated as 65% of available space per candle
  - Minimum width: 0.5px
  - Maximum: Space per candle × 0.65
- **Wick Width**: 
  - 1/8th of candle body width
  - Minimum: 0.05px (always visible)
- **Colors**:
  - **Bullish (white)**: When close > open
  - **Bearish (blue #3b82f6)**: When close < open
- **Body Height**: Minimum height for doji candles (wickWidth × 1.5)

### Chart Padding
- **Vertical Padding**: 5% top and bottom to prevent candles from being cut off
- **Horizontal Range**: Candles span from x=2 to x=98 (96% of chart width)

---

## Granular Data Modes

### Second Mode
- **Candle Type**: 1-second OHLCV candles
- **Data Limit**: Keeps most recent 1000 candles (~16 minutes)
- **Aggregation**: Automatically aggregates to 5s or 30s for longer timeframes when needed

### Tick Mode
- **Candle Type**: 100-tick OHLCV candles
- **Initial Load**: Last 1000 candles
- **Incremental Updates**: Last 120 candles
- **Data Retention**: Keeps data from last hour

---

## Other Settings

### Scroll Position
- **Default**: 100% (most recent data)
- **Behavior**: Auto-refresh only occurs when scrollPosition = 100%
- **Historical Viewing**: Disables auto-refresh to prevent interruption

### Market Hours
- **Trading Hours**: 9:30 AM - 4:00 PM ET
- **Auto-refresh**: Only active during market hours
- **Closed Market**: Uses last available data point timestamp as "now"

### Data Filtering
- **Maximum Candles**: 
  - For 1m timeframe: Up to 300 candles (5 minutes worth)
  - For other timeframes: Based on timeframe duration
- **Timestamp Filtering**: Strict filtering based on actual timestamps, not just count

---

## Summary Table

| Timeframe | Time Window | Candle Size (Granular) | Candle Size (Regular) | Update Freq (Granular) | Update Freq (Regular) | Supports Granular |
|-----------|-------------|------------------------|------------------------|------------------------|----------------------|-------------------|
| 1m        | 1 minute    | 1 second               | Regular dataset        | 1 second               | 60 seconds           | ✅ Yes            |
| 5m        | 5 minutes   | 1s or 5s aggregated    | Regular dataset        | 1 second               | 60 seconds           | ✅ Yes            |
| 15m       | 15 minutes  | 1s or 5s aggregated    | Regular dataset        | 1 second               | 60 seconds           | ✅ Yes            |
| 30m       | 30 minutes  | 1s or 30s aggregated  | Regular dataset        | 1 second               | 60 seconds           | ✅ Yes            |
| 1h        | 1 hour      | 1s or 30s aggregated  | Regular dataset        | 1 second               | 60 seconds           | ✅ Yes            |
| 2h        | 2 hours     | N/A                    | Regular dataset        | N/A                    | 60 seconds           | ❌ No             |
| 4h        | 4 hours     | N/A                    | Regular dataset        | N/A                    | 60 seconds           | ❌ No             |
| 6h        | Trading day | N/A                    | Regular dataset        | N/A                    | 60 seconds           | ❌ No             |
| 2d        | 48 hours    | N/A                    | Extended dataset       | N/A                    | 60 seconds           | ❌ No             |
| 3d        | 72 hours    | N/A                    | Extended dataset       | N/A                    | 60 seconds           | ❌ No             |


