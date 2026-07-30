import reflex as rx
from .api import ALL_TICKERS 
from .engine import generate_signal

class TextState(rx.State):
    text: str = ""
    is_focused: bool = False
    suggestions: list[dict] = []
    is_loading: bool = False

    @rx.event
    def redirect(self):
        return rx.redirect(f"/stock/{self.text}")


    @rx.event
    def click_suggestion(self, clicked_ticker: str):
        self.text = clicked_ticker
        return rx.redirect(f"/stock/{self.text}")

    @rx.event
    def clean_list(self):
        self.suggestions=[]


    @rx.event
    def set_focus(self):
        self.is_focused = True

    @rx.event
    def remove_focus(self):
        self.is_focused = False

    @rx.event
    def handle_typing(self, value: str):
        self.text = value.upper()
        if len(value) < 1:
            self.suggestions = []
            return
        
        self.suggestions = [
            stock for stock in ALL_TICKERS.values()
            if stock.get("ticker", "").lower().startswith(value.lower()) 
            or value.lower() in stock.get("title", "").lower()
        ][:3]

    
        