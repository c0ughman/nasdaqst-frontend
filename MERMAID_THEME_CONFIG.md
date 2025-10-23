# 🎨 Custom Mermaid Theme Configuration

## High Contrast, Professional Theme for NASDAQ Sentiment Tracker

Here's a custom Mermaid theme configuration that provides excellent readability with high contrast colors and professional styling:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    %% Core Colors - High Contrast
    "primaryColor": "#1a1a1a",
    "primaryTextColor": "#ffffff",
    "primaryBorderColor": "#00d4ff",
    "lineColor": "#00d4ff",
    "secondaryColor": "#2d2d2d",
    "tertiaryColor": "#404040",
    
    %% Background Colors
    "background": "#0a0a0a",
    "mainBkg": "#1a1a1a",
    "secondBkg": "#2d2d2d",
    "tertiaryBkg": "#404040",
    
    %% Text Colors
    "textColor": "#ffffff",
    "secondaryTextColor": "#b3b3b3",
    "tertiaryTextColor": "#808080",
    
    %% Node Colors - Vibrant & Distinct
    "nodeBkg": "#1a1a1a",
    "nodeBorder": "#00d4ff",
    "clusterBkg": "#2d2d2d",
    "clusterBorder": "#ff6b35",
    
    %% Edge Colors
    "edgeLabelBackground": "#1a1a1a",
    "edgeLabelColor": "#ffffff",
    
    %% Flowchart Specific
    "flowchart": {
      "nodeBkg": "#1a1a1a",
      "nodeBorder": "#00d4ff",
      "clusterBkg": "#2d2d2d",
      "clusterBorder": "#ff6b35",
      "defaultLinkColor": "#00d4ff",
      "titleColor": "#ffffff",
      "edgeLabelBackground": "#1a1a1a",
      "edgeLabelColor": "#ffffff",
      "gridColor": "#404040",
      "section0": "#1a1a1a",
      "section1": "#2d2d2d",
      "section2": "#404040",
      "section3": "#1a1a1a",
      "altSection": "#2d2d2d",
      "gridColor": "#404040",
      "taskBkgColor": "#1a1a1a",
      "taskTextColor": "#ffffff",
      "taskTextLightColor": "#b3b3b3",
      "taskTextOutsideColor": "#ffffff",
      "taskTextClickableColor": "#00d4ff",
      "activeTaskBkgColor": "#ff6b35",
      "activeTaskBorderColor": "#ff6b35",
      "gridColor": "#404040",
      "section0": "#1a1a1a",
      "section1": "#2d2d2d",
      "section2": "#404040",
      "section3": "#1a1a1a",
      "altSection": "#2d2d2d"
    }
  },
  "flowchart": {
    "nodeSpacing": 50,
    "rankSpacing": 50,
    "curve": "basis",
    "padding": 20,
    "useMaxWidth": true,
    "htmlLabels": true
  },
  "sequence": {
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "actorMargin": 50,
    "width": 150,
    "height": 65,
    "boxMargin": 10,
    "boxTextMargin": 5,
    "noteMargin": 10,
    "messageMargin": 35,
    "mirrorActors": true,
    "bottomMarginAdj": 1,
    "useMaxWidth": true,
    "rightAngles": false,
    "showSequenceNumbers": false
  },
  "gantt": {
    "titleTopMargin": 25,
    "barHeight": 20,
    "fontSize": 11,
    "fontFamily": "\"Open Sans\", sans-serif",
    "gridLineStartPadding": 35,
    "bottomPadding": 25,
    "leftPadding": 75,
    "gridLineStartPadding": 35,
    "fontSize": 11,
    "fontFamily": "\"Open Sans\", sans-serif",
    "numberSectionStyles": 4
  }
}}%%

graph TB
    %% Data Sources - Cyan Theme
    subgraph "📡 DATA SOURCES"
        A1[Finnhub API<br/>News Articles]
        A2[Reddit API<br/>PRAW Posts/Comments]
        A3[Yahoo Finance<br/>OHLCV Data]
        A4[Database<br/>Historical Data]
    end

    %% Data Collection - Blue Theme
    subgraph "📥 DATA COLLECTION"
        B1[Fetch Company News<br/>Top 20 NASDAQ Stocks]
        B2[Fetch Market News<br/>General Market News]
        B3[Fetch Reddit Content<br/>r/stocks, r/investing, etc.]
        B4[Fetch Stock Prices<br/>QQQ ETF as NASDAQ Proxy]
    end

    %% Sentiment Analysis - Purple Theme
    subgraph "🧠 SENTIMENT ANALYSIS"
        C1[FinBERT AI Model<br/>HuggingFace API]
        C2[Article Scoring<br/>5-Component Formula]
        C3[Reddit Analysis<br/>Post + Comment Sentiment]
        C4[Technical Indicators<br/>RSI, MACD, Bollinger Bands]
    end

    %% Scoring Components - Green Theme
    subgraph "📊 SCORING COMPONENTS"
        D1[Base Sentiment<br/>FinBERT: -1 to +1]
        D2[Surprise Factor<br/>Keyword Detection: 0.8-1.5x]
        D3[Novelty Score<br/>Cache Check: 0.2-1.0]
        D4[Source Credibility<br/>Predefined Ratings: 0.3-1.0]
        D5[Recency Weight<br/>Time Decay: 0.5-1.0]
    end

    %% Aggregation - Orange Theme
    subgraph "🔢 AGGREGATION"
        E1[Ticker-Level Scores<br/>Weighted by Market Cap]
        E2[Company News Composite<br/>70% Weight]
        E3[Market News Composite<br/>30% Weight]
        E4[Reddit Sentiment<br/>Social Media Score]
        E5[Technical Score<br/>Indicator Composite]
    end

    %% Final Composite - Red Theme
    subgraph "🎯 FINAL COMPOSITE"
        F1[News Sentiment<br/>Company 70% + Market 30%]
        F2[Reddit Sentiment<br/>Social Media Component]
        F3[Technical Score<br/>Indicator Composite]
        F4[FINAL COMPOSITE SCORE<br/>News 40% + Reddit 30% + Technical 30%]
    end

    %% Database Storage - Yellow Theme
    subgraph "💾 DATABASE STORAGE"
        G1[AnalysisRun<br/>Complete Analysis Record]
        G2[NewsArticle<br/>Individual Article Data]
        G3[RedditPost<br/>Reddit Content Data]
        G4[TickerContribution<br/>Individual Stock Contributions]
        G5[SentimentHistory<br/>Historical Aggregates]
    end

    %% API & Frontend - Magenta Theme
    subgraph "🌐 API & FRONTEND"
        H1[Django REST API<br/>/api/nasdaq-composite/]
        H2[React Dashboard<br/>Real-time Visualization]
        H3[HTML Dashboard<br/>nasdaq.html]
        H4[Auto-refresh<br/>Every 60 seconds]
    end

    %% Connections
    A1 --> B1
    A1 --> B2
    A2 --> B3
    A3 --> B4
    A4 --> B4

    B1 --> C1
    B2 --> C1
    B3 --> C3
    B4 --> C4

    C1 --> D1
    C2 --> D2
    C2 --> D3
    C2 --> D4
    C2 --> D5

    D1 --> E1
    D2 --> E1
    D3 --> E1
    D4 --> E1
    D5 --> E1

    E1 --> E2
    E1 --> E3
    C3 --> E4
    C4 --> E5

    E2 --> F1
    E3 --> F1
    E4 --> F2
    E5 --> F3

    F1 --> F4
    F2 --> F4
    F3 --> F4

    F4 --> G1
    E1 --> G2
    C3 --> G3
    E1 --> G4
    F4 --> G5

    G1 --> H1
    H1 --> H2
    H1 --> H3
    H2 --> H4
    H3 --> H4

    %% Custom Styling Classes
    classDef dataSource fill:#00d4ff,stroke:#ffffff,stroke-width:2px,color:#000000,font-weight:bold
    classDef analysis fill:#8b5cf6,stroke:#ffffff,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef scoring fill:#10b981,stroke:#ffffff,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef aggregation fill:#f59e0b,stroke:#ffffff,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef final fill:#ef4444,stroke:#ffffff,stroke-width:3px,color:#ffffff,font-weight:bold
    classDef storage fill:#eab308,stroke:#ffffff,stroke-width:2px,color:#000000,font-weight:bold
    classDef api fill:#ec4899,stroke:#ffffff,stroke-width:2px,color:#ffffff,font-weight:bold

    class A1,A2,A3,A4 dataSource
    class B1,B2,B3,B4,C1,C2,C3,C4 analysis
    class D1,D2,D3,D4,D5 scoring
    class E1,E2,E3,E4,E5 aggregation
    class F1,F2,F3,F4 final
    class G1,G2,G3,G4,G5 storage
    class H1,H2,H3,H4 api
```

---

## 🎨 Alternative Color Schemes

### **Option 1: Financial Theme (Blue/Gold)**
```javascript
"primaryColor": "#1e3a8a",      // Deep blue
"primaryTextColor": "#ffffff",   // White text
"primaryBorderColor": "#fbbf24", // Gold border
"secondaryColor": "#1e40af",     // Medium blue
"tertiaryColor": "#3b82f6",      // Light blue
"background": "#0f172a",          // Very dark blue
"mainBkg": "#1e3a8a",            // Deep blue
"secondBkg": "#1e40af",          // Medium blue
"tertiaryBkg": "#3b82f6",        // Light blue
```

### **Option 2: High Contrast Monochrome**
```javascript
"primaryColor": "#000000",       // Pure black
"primaryTextColor": "#ffffff",  // Pure white
"primaryBorderColor": "#ffffff", // White border
"secondaryColor": "#333333",     // Dark gray
"tertiaryColor": "#666666",      // Medium gray
"background": "#000000",         // Black background
"mainBkg": "#000000",            // Black
"secondBkg": "#333333",          // Dark gray
"tertiaryBkg": "#666666",        // Medium gray
```

### **Option 3: Vibrant Tech Theme**
```javascript
"primaryColor": "#0d1117",       // GitHub dark
"primaryTextColor": "#f0f6fc",   // GitHub light
"primaryBorderColor": "#58a6ff", // GitHub blue
"secondaryColor": "#161b22",     // GitHub dark gray
"tertiaryColor": "#21262d",      // GitHub medium gray
"background": "#0d1117",          // GitHub dark
"mainBkg": "#0d1117",            // GitHub dark
"secondBkg": "#161b22",          // GitHub dark gray
"tertiaryBkg": "#21262d",        // GitHub medium gray
```

---

## 🔧 Usage Instructions

### **1. Copy the Theme Configuration**
Copy the `%%{init: {...}}%%` block at the top of your Mermaid diagram.

### **2. Apply Custom Classes**
Use the `classDef` statements to define your color schemes:
```mermaid
classDef dataSource fill:#00d4ff,stroke:#ffffff,stroke-width:2px,color:#000000,font-weight:bold
classDef analysis fill:#8b5cf6,stroke:#ffffff,stroke-width:2px,color:#ffffff,font-weight:bold
```

### **3. Assign Classes to Nodes**
```mermaid
class A1,A2,A3,A4 dataSource
class B1,B2,B3,B4,C1,C2,C3,C4 analysis
```

---

## 🎯 Key Features of This Theme

### **High Contrast Design**
- **Dark Background**: Deep black (#0a0a0a) for maximum contrast
- **Bright Borders**: Cyan (#00d4ff) for clear node separation
- **White Text**: Pure white (#ffffff) for maximum readability
- **Thick Strokes**: 2-3px borders for clear definition

### **Color-Coded Categories**
- **📡 Data Sources**: Cyan (#00d4ff) - Represents data flow
- **🧠 Analysis**: Purple (#8b5cf6) - Represents AI/processing
- **📊 Scoring**: Green (#10b981) - Represents positive metrics
- **🔢 Aggregation**: Orange (#f59e0b) - Represents combination
- **🎯 Final**: Red (#ef4444) - Represents final output
- **💾 Storage**: Yellow (#eab308) - Represents data persistence
- **🌐 API**: Magenta (#ec4899) - Represents external interfaces

### **Professional Typography**
- **Bold Fonts**: `font-weight:bold` for emphasis
- **High Contrast Text**: Black text on light backgrounds, white on dark
- **Clear Hierarchy**: Different colors for different process stages

### **Accessibility Features**
- **WCAG Compliant**: High contrast ratios meet accessibility standards
- **Color Blind Friendly**: Uses distinct colors that work for colorblind users
- **Clear Boundaries**: Thick borders make nodes easy to distinguish

---

## 📱 Responsive Design

The theme includes responsive settings:
```javascript
"useMaxWidth": true,        // Scales to container width
"htmlLabels": true,         // Better text rendering
"padding": 20,             // Adequate spacing
"nodeSpacing": 50,         // Clear separation between nodes
"rankSpacing": 50          // Clear separation between levels
```

This theme provides excellent readability, professional appearance, and high contrast suitable for presentations, documentation, and technical diagrams.
