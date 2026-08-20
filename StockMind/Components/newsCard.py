import reflex as rx
from ..Backend.stockState import StockState


def news_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.link(f"{StockState.headline}", href=f"{StockState.link}", is_external=True),
        ),
        padding="2em",
        border_radius="10px",
        box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
        background_color="#1e1e1e",
        color="white",
    )