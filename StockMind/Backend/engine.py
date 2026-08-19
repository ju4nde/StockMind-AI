import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import numpy as np
import joblib
import os
import re
from dotenv import load_dotenv

load_dotenv()


current_dir = os.path.dirname(__file__)
MODEL_PATH= os.path.join(current_dir,"stockmind.joblib")


try:
    ML_CLASSIFIER = joblib.load(MODEL_PATH)
    print("Model succesfully loaded")
except FileNotFoundError:
    print("stockmind.joblib not found")
    ML_CLASSIFIER= None

def get_news(ticker_symbol:str):
    try:
        ticker= yf.Ticker(ticker_symbol.upper())
        news= ticker.news
        if news:
            organic_news = [
                n for n in news 
                if not n.get("content", {}).get("metadata", {}).get("editorsPick", False)
            ]
            valid_news = organic_news if organic_news else news
            valid_news.sort(
                key=lambda x: x.get("content", {}).get("pubDate", ""), 
                reverse=True
            )
            article=valid_news[0]
            article_content= article.get("content", {})
            print(article_content)
            if not article_content.get("description"):
                title= article_content.get("title") or ""
                summary = article_content.get("summary") or ""
                raw_text = title + ". " + summary
            else:
                raw_text = article_content.get("description")
            clean_description = re.sub(r'<[^>]+>', '', raw_text) if raw_text else "No recent news available."

            return clean_description
    
    except Exception as e:
        return "No news available"



#Uses pandas-ta to calculate a 50-day Simple moving average
def get_sma(ticker_symbol:str):
    try:
        ticker = yf.Ticker(ticker_symbol.upper())
        df= ticker.history(period="6mo",interval="1d")

        if df.empty:
            return {"error": f"No 6 month-1 day interval data found for ticker {ticker}"}
        
        df.ta.sma(close="Close", length=50, append=True)
        latest_row=df.iloc[-1]


        return latest_row["SMA_50"]
    
    except Exception as e:
        return {"error": f"An error occurred while processing data: {str(e)}"}


def get_indicators(ticker_symbol: str) -> dict:

    try:
        #this is to connect to yahoo finance and get live stock data
        ticker = yf.Ticker(ticker_symbol.upper())
        print("printing 1d and 1m")
        df= ticker.history(period="1d",interval="1m")
        
        if df.empty:
            return {"error": f"No data found for ticker {ticker}"}

        print(df)
        
        if len(df) < 50:
            return {"error": "Not enough daily data to analyze stock"}
        
        #Uses pandas-ta to calculate RSI(Relative strength index)
        df.ta.rsi(close="Close", length=14, append=True)
        sma = get_sma(ticker_symbol)
        clean_description=get_news(ticker_symbol)

        latest_row= df.iloc[-1]



        metrics = {
            "ticker": ticker_symbol.upper(),
            "current_price": round(float(latest_row["Close"]), 2),
            "rsi": round(float(latest_row["RSI_14"]), 2) if not pd.isna(latest_row["RSI_14"]) else 50.0,
            "sma_50": round(float(sma),2) if not pd.isna(sma) else float(latest_row["Close"]),
            "volume": int(latest_row["Volume"]),
            "headline": clean_description
        }

        metrics["trend"] = "Uptrend" if metrics["current_price"] > metrics["sma_50"] else "Downtrend"
        
        return metrics
    except Exception as e:
        return {"error": f"An error occurred while processing data: {str(e)}"}


def analyze_sentiment(headline:str) -> float:
    hf_token = os.getenv("HF_API_KEY")

    API_URL = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
    
    # Replace this with your actual token from HuggingFace!
    headers = {f"Authorization": f"Bearer {hf_token}"} 
    
    payload = {"inputs": headline}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"HuggingFace API Error: {response.text}")
            return 0.0

        results = response.json()[0]
        
        pos_prob = 0.0
        neg_prob = 0.0
    
        for sentiment in results:
            if sentiment['label'] == 'positive':
                pos_prob = sentiment['score']
            elif sentiment['label'] == 'negative':
                neg_prob = sentiment['score']
        
        
        compound_score= pos_prob - neg_prob

        return round(compound_score, 4)

    except Exception as e:
        print(f"Sentiment analysis error: {str(e)}")
        return 0.0

    

def generate_signal(ticker_symbol: str) -> dict:
    ticker_data = get_indicators(ticker_symbol)
    if "error" in ticker_data:
        return ticker_data
    
    sentiment_score= analyze_sentiment(ticker_data["headline"])
    trend_flag= 1 if ticker_data["trend"] == "Uptrend" else 0
    live_features= np.array([[ticker_data["rsi"],sentiment_score, trend_flag]])
    prediction = ML_CLASSIFIER.predict(live_features)[0]
    confidence = ML_CLASSIFIER.predict_proba(live_features)[0]

    signal_map={1:"BUY", -1: "SELL", 0: "HOLD"}

    return {
        "ticker": ticker_data["ticker"],
        "price": ticker_data["current_price"],
        "rsi": ticker_data["rsi"],
        "trend": ticker_data["trend"],
        "sentiment": sentiment_score,
        "signal": signal_map[prediction],
        "confidence_sell": round(float(confidence[0]),2),
        "confidence_hold":round(float(confidence[1]),2),
        "headline": ticker_data["headline"],
        "confidence_buy":round(float(confidence[2]),2)
    }






if __name__ == "__main__":
    print("\n--- Testing Market Data Engine ---")