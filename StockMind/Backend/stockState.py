import reflex as rx
from ..Backend.state import TextState
from ..Backend.engine import generate_signal


class StockState(rx.State):
    current_price : float = 0.0
    signal : str = ""
    headline: str = ""
    trend: str = ""
    rsi: float = 0.0
    sentiment: float = 0.0
    confidence_buy: float = 0.0
    confidence_sell: float = 0.0
    confidence_hold: float = 0.0
    link: str = ""
    sma_50: float = 0.0
    sentiment_call: str = ""
    rsi_call: str = ""

    def analyze_stock(self):
        if not self.ticker: return

        prediction = generate_signal(self.ticker)
        if "error" in prediction:
            self.current_price = 0
            self.signal = "none"
            self.headline = "none"
            self.trend = "none"
            self.rsi = 0.0
            self.sentiment = 0.0
            self.confidence_buy = 0.0
            self.confidence_sell = 0.0
            self.confidence_hold = 0.0
            self.link = "none"
            self.sma_50 = 0.0
            self.sentiment_call = "none"
            self.rsi_call = "none"
            return

        self.current_price = prediction["price"]
        self.signal = prediction["signal"]
        self.headline = prediction["headline"]
        self.trend = prediction["trend"]
        self.rsi = prediction["rsi"]
        self.sentiment = prediction["sentiment"]
        self.confidence_buy = prediction["confidence_buy"]
        self.confidence_sell = prediction["confidence_sell"]
        self.confidence_hold = prediction["confidence_hold"]
        self.link = prediction["link"]
        self.sma_50 = prediction["sma_50"]
        self.sentiment_call = "Positive" if self.sentiment > 0.25 else "Negative" if self.sentiment < -0.25 else "Neutral"
        self.rsi_call = "Overbought" if self.rsi > 70 else "Oversold" if self.rsi < 30 else "Neutral"