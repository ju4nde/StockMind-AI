import reflex as rx
from .api import ALL_TICKERS 

class TextState(rx.State):
    text: str = ""
    is_focused: bool = False
    suggestions: list[dict] = []

    @rx.event
    def set_focus(self):
        self.is_focused = True

    @rx.event
    def remove_focus(self):
        self.is_focused = False

    @rx.event
    def handle_typing(self, value: str):
        self.text = value
        
        if len(value) < 1:
            self.suggestions = []
            return
        
        self.suggestions = [
            stock for stock in ALL_TICKERS
            if value.lower() in stock.get("Symbol", "").lower() 
            or value.lower() in stock.get("Security Name", "").lower()
        ][:5]  

    @rx.event
    def send_to_ai(self, form_data: dict):
        self.text = form_data.get("symbol", "")
        return rx.redirect("/a")