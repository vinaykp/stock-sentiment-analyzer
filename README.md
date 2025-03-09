# Stock Market Sentiment Analyzer

A Streamlit-based application that determines the bull or bear of the day based on market fear index and news sentiment analysis.

## Features

- Real-time Fear & Greed Index tracking
- News sentiment analysis for major stocks
- Daily market sentiment indicator
- Interactive visualizations
- Bull/Bear stock recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vinaykp/stock-sentiment-analyzer.git
cd stock-sentiment-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

The application will automatically fetch and analyze:
- Current Fear & Greed Index
- Latest market news
- Stock sentiment indicators

Based on this analysis, it will recommend the bull or bear stock of the day.

## Data Sources

- Fear & Greed Index: CNN Money
- Market News: Various financial news APIs
- Stock Data: Yahoo Finance

## License

MIT License