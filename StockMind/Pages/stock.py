import reflex as rx
from ..Components.navbar import navbar
from ..Components.newsCard import news_card
from ..Backend.stockState import StockState



@rx.page(route="/stock/[ticker]", on_load= StockState.analyze_stock)
def stock_dashboard():
    return rx.vstack(
        rx.box(
            navbar(),
            position = "fixed",
            top ="0",
            width= "100%",
            z_index= "100",
            ),
        rx.heading(f"Analysis for {StockState.ticker}"),
        rx.card(
            rx.vstack(
                rx.text("AI Prediction Signal:", font_weight="bold"),
                rx.text(f"{StockState.signal}", color=rx.match(StockState.signal,
                                                               ("BUY", "green"),
                                                               ("SHORT", "red"),
                                                               ("HOLD", "blue"),
                                                               "blue",
                                                               ), 
                                                font_size="2em"),
                rx.divider(),
                rx.text(f"Current Price: ${StockState.current_price}", font_weight="bold"),
                rx.text(f"RSI: {StockState.rsi} ({StockState.rsi_call})", font_weight="bold"),
                rx.text(f"50-day SMA: {StockState.sma_50}", font_weight="bold"),
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
                news_card(),
                rx.text(f"Sentiment Score: {StockState.sentiment} ({StockState.sentiment_call})", font_weight="bold"),
            ),
            padding="2em",
            width="400px"
        ),
        align_items="center",
        padding_top="10em",
    )