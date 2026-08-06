import reflex as rx
from ..Backend.state import TextState
from ..Backend.engine import generate_signal
from ..Components.navbar import navbar


class StockState(rx.State):
    current_price : float = 0.0
    signal : str = ""
    headline: str = ""

    def analyze_stock(self):
        if not self.ticker: return

        prediction = generate_signal(self.ticker)
        if "error" in prediction:
            self.current_price = 0
            self.signal = "none"
            self.headline = "none"
            return

        self.current_price = prediction["price"]
        self.signal = prediction["signal"]
        self.headline = prediction["headline"]
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
                rx.text("Current Price:", font_weight="bold"),
                rx.text(f"${StockState.current_price}"),
                rx.divider(),
                rx.text("AI Prediction Signal:", font_weight="bold"),
                rx.text(f"{StockState.signal}", color=rx.match(StockState.signal,
                                                               ("BUY", "green"),
                                                               ("SELL", "red"),
                                                               ("HOLD", "blue"),
                                                               "blue",
                                                               ), 
                                                font_size="2em"),

                rx.text(f"{StockState.headline}")
            ),
            padding="2em",
            width="400px"
        ),
        align_items="center",
        padding_top="10em",
    )