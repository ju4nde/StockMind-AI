import reflex as rx
from ..Backend.state import TextState

def navbar():
    return rx.hstack(
        # 1. LOGO (Moved out of the inner hstack)
        rx.heading(
            rx.text.span("S", color="#6a27a8"),
            "tock",
            rx.text.span("M", color="#6a27a8"),
            "ind ",
            rx.text.span("AI", color="#6a27a8"),        
            weight="bold",
            size="7",
        ),
        
        # 2. SEARCH BAR FORM (Now a direct child of the main navbar)
        rx.form(
            rx.input(
                name="symbol",         
                placeholder="Company or stock symbol...",
                width="100%",      
                height="40px",
                border_width="1.5px",
                border_radius=rx.cond(TextState.suggestions, "20px 20px 0px 0px", "20px"),
                font_size="1em",
                border_color="#6a27a8",
                color="white",
                position="relative",         
                on_focus=TextState.set_focus,
                on_blur=TextState.remove_focus, 
                on_change=TextState.handle_typing,
                color_scheme="violet",
                z_index="10",
                background_color="#1e1e1e",
                border_bottom=rx.cond(TextState.suggestions, "none", "1.5px solid #6a27a8"),
                outline="none",
                box_shadow="none",
            ),
            rx.cond(
                TextState.suggestions,
                rx.vstack(
                    rx.foreach(
                        TextState.suggestions,
                        lambda item: 
                        rx.hstack(
                            rx.text(item["ticker"], color="#7e6396"),
                            rx.spacer(),
                            rx.text(item["title"], color="#79757d"),
                            width="100%", 
                            justify_content="space_between",
                            padding="4px",    
                            _hover={"bg": "#b469fa", "cursor": "pointer"},
                            on_click=lambda _: TextState.click_suggestion(item["ticker"])
                        ),
                    ),
                    border="1.5px solid #6a27a8",
                    border_radius="0px 0px 20px 20px",
                    width="100%",   
                    position="absolute",
                    overflow_y="auto",
                    box_shadow="0px 10px 15px -3px rgba(0, 0, 0, 0.5)",
                    background_color="#121212",
                    z_index="5",
                    border_top="none",
                    border_top_radius="10px",
                    padding="5px",
                    transform="translateZ(0)"
                ),
            ),  
            on_submit=TextState.redirect,
            width="100%",
            max_width="500px", 
            position="relative", 
            margin_x="4", # Added a small side margin so it doesn't touch the logo on tiny screens
            right=["0","0","350px"],  # Center the form horizontally
        ),
        
        # 3. HOME BUTTON
        rx.icon(
            tag="home",
            color="#6a27a8",
            size=40,
            on_click=rx.redirect("/"),
            _hover={"cursor": "pointer"},
            stroke_width=1,
        ),
        
        # OUTER NAVBAR SETTINGS
        justify="between",
        align_elements="center",
        width="100%",
        padding="10px",
        position="relative",
        border_bottom="1px solid rgba(255, 255, 255, 0.1)",
        bg="#111113",
    )