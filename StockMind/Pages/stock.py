import reflex as rx
from ..Backend.state import TextState
from ..Backend.engine import generate_signal
from ..Components.navbar import navbar


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
        print(prediction)


@rx.page(route="/stock/[ticker]", on_load= StockState.analyze_stock)
def stock_dashboard():
    return rx.vstack(
        rx.box(
            navbar(),
            position = "fixed",
            top ="0",
            width= "100%"
            ),
        rx.heading(f"Analysis for {StockState.ticker}"),
        rx.card(
            rx.vstack(
                rx.text("AI Prediction Signal:", font_weight="bold"),
                rx.text(f"{StockState.signal}", color=rx.match(StockState.signal,
                                                               ("BUY", "green"),
                                                               ("SELL", "red"),
                                                               ("HOLD", "blue"),
                                                               "blue",
                                                               ), 
                                                font_size="2em"),
                rx.divider(),
                rx.text(f"Current Price: ${StockState.current_price}", font_weight="bold"),
                rx.text(f"RSI: {StockState.rsi}", font_weight="bold"),
                rx.hstack(
                    rx.text("Trend: ", font_weight="bold"),
                    rx.text(f"{StockState.trend}", font_weight="bold",color=rx.match(StockState.trend,
                                                               ("Downtrend", "red"),
                                                               ("Uptrend", "green"),
                                                               "white",
                                                               ), ),
                ),
                rx.divider(),
                rx.text("Most recent news article:", font_weight="bold"),
                rx.text(f"{StockState.headline}"),
                rx.text(f"Sentiment Score: {StockState.sentiment}", font_weight="bold"),
            ),
            padding="2em",
            width="400px"
        ),
        align_items="center",
        padding_top="10em",
    )