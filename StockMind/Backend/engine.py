import yfinance as yf
import pandas as pd
import pandas_ta as ta
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

FINBERT_TOKENIZER = AutoTokenizer.from_pretrained("ProsusAI/finbert")
FINBERT_MODEL = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


def get_indicators(ticker_symbol: str) -> dict:

    try:
        #this is to connect to yahoo finance and get live stock data
        ticker = yf.Ticker(ticker_symbol.upper())
        df= ticker.history(period="1mo",interval="1h")
        
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






if __name__ == "__main__":
    print("\n--- Testing Market Data Engine ---")
    print(get_indicators("AAPL"))
    
    print("\n--- Testing Sentiment Engine (FinBERT) ---")
    good_news = "Apple quarterly profits smash expectations, setting new revenue record."
    bad_news = "Antitrust lawsuit filed against Apple threatens App Store ecosystem."
    
    print(f"Headline: '{good_news}'")
    print(f"AI Score: {analyze_sentiment(good_news)}") 
    
    print(f"Headline: '{bad_news}'")
    print(f"AI Score: {analyze_sentiment(bad_news)}") 