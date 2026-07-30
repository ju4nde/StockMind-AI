import reflex as rx
from ..Backend.state import TextState
from ..Backend.engine import generate_signal


class StockState(rx.State):
    current_price : float = 0.0
    signal : str = ""



    def analyze_stock(self):
        if not self.ticker: return

        prediction = generate_signal(self.ticker, "Massive fraud exposed, CEO arrested, company filing for immediate bankruptcy and delisting.")
        self.current_price = prediction["price"]
        self.signal = prediction["signal"]
        print(prediction)








@rx.page(route="/stock/[ticker]", on_load= StockState.analyze_stock)
def stock_dashboard():
    return rx.vstack(
        rx.heading(f"Analysis for {StockState.ticker}"),
        rx.card(
            rx.vstack(
                rx.text("Current Price:", font_weight="bold"),
                rx.text(f"${StockState.current_price}"),
                rx.divider(),
                rx.text("AI Prediction Signal:", font_weight="bold"),
                rx.text(f"{StockState.signal}", color="blue", font_size="2em"),
            ),
            padding="2em",
            width="400px"
        ),
        rx.button("Search Another Stock", on_click=rx.redirect("/"), margin_top="2em"),
        align_items="center",
        padding_top="5em"
    )