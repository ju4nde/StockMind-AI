import reflex as rx
from ..Backend.state import TextState


def navbar():
    return rx.hstack(
        rx.heading(
            rx.text.span("S", color="#6a27a8"),
            "tock",
            rx.text.span("M", color="#6a27a8"),
            "ind ",
            rx.text.span("AI", color="#6a27a8"),        
            weight="bold",
            size="8",
        ),
        rx.form(
            rx.input(
                name="symbol",         
                placeholder="Company or stock symbol...",
                width="100%",          
                height="45px",
                border_width="3px",
                border_radius= "16px",
                font_size="1.2em",
                border_color="#6a27a8",
                color="white",
                position="relative",         
                on_focus=TextState.set_focus,
                on_blur=TextState.remove_focus, 
                on_change=TextState.handle_typing,
                color_scheme="violet",
                z_index="10",
                background_color="#121212",
                outline="none",
                box_shadow="none",
                value = TextState.text
            ),
            on_submit=TextState.redirect,
            width="500px",
            position="absolute", 
            left="50%", 
            transform="translateX(-50%)",
        ),
        rx.icon(tag="home",
                color= "#6a27a8",
                size= 50,
                on_click=rx.redirect("/"),
                _hover={"cursor": "pointer"},
                ),

        justify= "between",
        align_elements="center",
        width = "100%",
        padding = "20px",
        position="relative"
        #border_width="3px",
        #border_color= "red"
    )