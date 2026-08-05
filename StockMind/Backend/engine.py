import yfinance as yf
import pandas as pd
import pandas_ta as ta
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import joblib
import os
import re



current_dir = os.path.dirname(__file__)
MODEL_PATH= os.path.join(current_dir,"stockmind.joblib")
FINBERT_PATH = os.path.join(current_dir,"local_finbert")

FINBERT_TOKENIZER = AutoTokenizer.from_pretrained(FINBERT_PATH)
FINBERT_MODEL = AutoModelForSequenceClassification.from_pretrained(FINBERT_PATH)


try:
    ML_CLASSIFIER = joblib.load(MODEL_PATH)
    print("Model succesfully loaded")
except FileNotFoundError:
    print("stockmind.joblib not found")
    ML_CLASSIFIER= None



def get_indicators(ticker_symbol: str) -> dict:

    try:
        #this is to connect to yahoo finance and get live stock data
        ticker = yf.Ticker(ticker_symbol.upper())
        df= ticker.history(period="1mo",interval="1h")
        news = ticker.news
        #print(news)
        article= news[0]
        #print(article)
        article_content = article.get("content", {})
        article_description= article_content.get("summary", "No summary available.")
        clean_description = re.sub(r'<[^>]+>', '', article_description)


        
        if df.empty:
            return {"error": f"No data found for ticker {ticker}"}
        #Uses pandas-ta to calculate RSI(Relative strength index)
        df.ta.rsi(close="Close", length=14, append=True)
        #Uses pandas-ta to calculate a 50-day Simple moving average
        df.ta.sma(close="Close", length=50, append=True)

        #get the latest row
        latest_row= df.iloc[-1]

        metrics = {
            "ticker": ticker_symbol.upper(),
            "current_price": round(float(latest_row["Close"]), 2),
            "rsi": round(float(latest_row["RSI_14"]), 2) if not pd.isna(latest_row["RSI_14"]) else 50.0,
            "sma_50": round(float(latest_row["SMA_50"]),2) if not pd.isna(latest_row["SMA_50"]) else float(latest_row["Close"]),
            "volume": int(latest_row["Volume"]),
            "headline": clean_description
        }

        metrics["trend"] = "Uptrend" if metrics["current_price"] > metrics["sma_50"] else "Downtrend"
        
        return metrics
    except Exception as e:
        return {"error": f"An error occurred while processing data: {str(e)}"}


def analyze_sentiment(headline:str) -> float:
    try:
        inputs = FINBERT_TOKENIZER(headline, return_tensors="pt",padding=True,truncation= True)

        with torch.no_grad():
            outputs = FINBERT_MODEL(**inputs)
        

        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pos_prob = float(predictions[0][0])
        neg_prob = float(predictions[0][1])
        neu_prob = float(predictions[0][2])
        
        compound_score= pos_prob - neg_prob

        return round(compound_score, 4)

    except Exception as e:
        print(f"Sentiment analysis error: {str(e)}")
        return 0.0

    

def generate_signal(ticker_symbol: str, headline: str ) -> dict:
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
    bad_news = "Antitrust lawsuit filed against Apple threatens App Store ecosystem."
    print(generate_signal("AAPL", bad_news))