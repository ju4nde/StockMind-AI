import reflex as rx
from ..Backend.state import TextState


def index() -> rx.Component:   
    return rx.vstack(
        rx.heading(
            "Welcome to",
            font_size=["2rem", "3rem", "3.5rem"],
            #size = "9",
            line_height=["2.5", "1", "1"],
            position="absolute",
            top="27vh",           
            left="50%",
            transform="translateX(-50%)",
            opacity=["1", "1",rx.cond(TextState.is_focused, "0", "1")], 
            transition="opacity 0.2s ease-in-out",
        ),

        rx.heading(
            rx.text.span("S", color="#6a27a8"),
            "tock",
            rx.text.span("M", color="#6a27a8"),
            "ind ",
            rx.text.span("AI", color="#6a27a8"),
            font_size=["2rem", "3rem", "3.5rem"],
            line_height=["0", "1", "1"],
            #size = "9",        
            weight="bold",
  
            position="absolute", 
            transition="all 0.5s ease-in-out", 
            top=["35vh", "35vh", rx.cond(TextState.is_focused, "0px", "35vh")],
            left=["50%", "50%", rx.cond(TextState.is_focused, "0", "50%")],
            transform=["translateX(-50%) scale(1)", "translateX(-50%) scale(1)", rx.cond(TextState.is_focused, "translateX(-20%) scale(0.5)", "translateX(-50%) scale(1)")],
            z_index="10",
        ),
        
        rx.text(
            "To start, search for a symbol below.", 
            #size="5",
            font_size=["1rem", "1.5rem", "1.5rem"], 
            color="gray",
            text_align="center",

            opacity=["1", "1", rx.cond(TextState.is_focused, "0", "1")],
            transition="opacity 0.2s ease-in-out",
        ),
        
        rx.form(
            rx.input(
                name="symbol",         
                placeholder="Company or stock symbol...",
                width="100%",          
                height="50px",
                border_width="1.5px",
                border_radius=rx.cond(TextState.suggestions, "20px 20px 0px 0px", "20px"),
                font_size="1.2em",
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
                            rx.text(
                                item["ticker"],
                                color="#7e6396",
                                ),
                            rx.spacer(),
                            rx.text(
                                item["title"],
                                color="#79757d",
                                ),
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
            position="relative",
            width=["300px","400px","600px", "600px"],
            transform=[
                "translateX(0) scale(1)", # Mobile: Always locked
                "translateX(0) scale(1)", # Tablet: Always locked
                rx.cond(TextState.is_focused, "translateY(-350%) scale(1.5)", "translateX(0) scale(1)") # Desktop: Animates!
            ],
            transition="transform 0.5s ease-in-out",
        ),
        
        align_items="center",      
        justify_content="center",  
        height="100vh",            
        spacing="5",               
    )