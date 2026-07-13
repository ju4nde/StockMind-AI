import yfinance as yf
import pandas as pd
import pandas_ta as ta


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


# TEMPORARY TEST BLOCK - Remove or comment out later
if __name__ == "__main__":
    print("Testing Market Data Engine...")
    test_data = get_indicators("AAPL")
    print(test_data)