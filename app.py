import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from textblob import TextBlob
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup

# Page config
st.set_page_config(
    page_title="Bull/Bear Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Bull/Bear Stock Analyzer")
st.markdown("""Analyze market sentiment and find the bull or bear stock of the day 
            based on fear index and news sentiment.""")

def get_fear_greed_index():
    try:
        # Note: In a production environment, you would use the actual Fear & Greed API
        # This is a simplified version for demonstration
        response = requests.get('https://alternative.me/crypto/fear-and-greed-index/')
        soup = BeautifulSoup(response.text, 'html.parser')
        fng_value = 50  # Default value
        # Extract the actual value from the page
        fng_div = soup.find('div', {'class': 'fng-value'})
        if fng_div:
            fng_value = int(fng_div.text.strip())
        return fng_value
    except Exception as e:
        st.error(f"Error fetching Fear & Greed Index: {e}")
        return 50

def get_news_sentiment(symbol):
    try:
        # Get news from Yahoo Finance
        stock = yf.Ticker(symbol)
        news = stock.news
        
        if not news:
            return 0
        
        # Calculate sentiment scores
        sentiments = []
        for article in news[:5]:  # Analyze last 5 news items
            analysis = TextBlob(article['title'])
            sentiments.append(analysis.sentiment.polarity)
        
        return sum(sentiments) / len(sentiments)
    except Exception as e:
        st.error(f"Error analyzing news for {symbol}: {e}")
        return 0

def get_stock_recommendation(fear_index, sentiment_score):
    # Combined score (50% fear index, 50% news sentiment)
    normalized_fear = fear_index / 100  # Fear index is 0-100
    normalized_sentiment = (sentiment_score + 1) / 2  # Sentiment is -1 to 1
    
    combined_score = (normalized_fear + normalized_sentiment) / 2
    
    if combined_score >= 0.6:
        return "Strong Bull"
    elif combined_score >= 0.5:
        return "Moderate Bull"
    elif combined_score <= 0.4:
        return "Strong Bear"
    else:
        return "Moderate Bear"

# Main app layout
fear_index = get_fear_greed_index()

# Display Fear & Greed Index
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fear & Greed Index")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = fear_index,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "red"},
                {'range': [25, 50], 'color': "orange"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig)

# Stock analysis section
st.subheader("Stock Analysis")
default_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
selected_stocks = st.multiselect(
    "Select stocks to analyze:",
    default_stocks,
    default=default_stocks
)

if st.button("Analyze Stocks"):
    analysis_data = []
    
    for symbol in selected_stocks:
        sentiment_score = get_news_sentiment(symbol)
        recommendation = get_stock_recommendation(fear_index, sentiment_score)
        
        analysis_data.append({
            'Symbol': symbol,
            'Sentiment Score': round(sentiment_score, 2),
            'Recommendation': recommendation
        })
    
    # Display results
    df = pd.DataFrame(analysis_data)
    st.dataframe(df)
    
    # Find bull and bear of the day
    bull = df[df['Sentiment Score'] == df['Sentiment Score'].max()].iloc[0]
    bear = df[df['Sentiment Score'] == df['Sentiment Score'].min()].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"🐂 Bull of the Day: {bull['Symbol']}")
        st.write(f"Sentiment Score: {bull['Sentiment Score']}")
        st.write(f"Recommendation: {bull['Recommendation']}")
    
    with col2:
        st.error(f"🐻 Bear of the Day: {bear['Symbol']}")
        st.write(f"Sentiment Score: {bear['Sentiment Score']}")
        st.write(f"Recommendation: {bear['Recommendation']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Data sources: Yahoo Finance, Alternative.me</p>
</div>
""", unsafe_allow_html=True)