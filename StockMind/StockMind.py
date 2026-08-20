import os
import reflex as rx
from dotenv import load_dotenv
from .Pages.index import index
from .Pages.stock import stock_dashboard

load_dotenv()
stock_api_key = os.getenv("STOCKS_API_KEY")

app = rx.App(
    theme=rx.theme(
        appearance="dark",
    )
)
app.add_page(index, route="/") 