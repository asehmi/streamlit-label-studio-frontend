import streamlit as st

# -----------------------------------------------------------------------------

BACKGROUND_COLOR = 'white'
COLOR = 'black'

# -----------------------------------------------------------------------------
# Set page style

def set_page_container_style(
    max_width: int = 800, max_width_100_percent: bool = False,
    padding_top: int = 10, padding_right: int = 10, padding_left: int = 10, padding_bottom: int = 10,
    color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    sidebar_overflow = 'auto', main_overflow = 'auto',
):
    sidebar_class = "css-hxt7ib e1fqkh3o2"
    mainapp_class = "block-container css-18e3th9 egzxvld2"

    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'
    st.markdown(
        f'''
        <style>
            header {{
                visibility: visible;
                height: 0%;
            }}
            .appview-container {{
                color: {color};
                background-color: {background_color};
                overflow: {main_overflow};
            }}
            div[class="{sidebar_class}"] {{
                color: {color};
                {max_width_str}
                padding-top: {padding_top}px;
                overflow: {sidebar_overflow};
            }}
            div[class="{mainapp_class}"] {{
                {max_width_str}
                padding-top: {padding_top}px;
                padding-right: {padding_right}px;
                padding-left: {padding_left}px;
                padding-bottom: {padding_bottom}px;
            }}
        </style>
        ''',
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Hide decoration

def hide_streamlit_styles():
    hide_streamlit_styles = """
    <style>
        div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
        div[data-testid="stDecoration"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
        div[data-testid="stStatusWidget"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
        }
        #MainMenu {
            visibility: hidden;
            height: 0%;
        }
        header {
            visibility: hidden;
            height: 0%;
        }
        footer {
            visibility: hidden;
            height: 0%;
        }
    </style>
    """
    # hide_streamlit_styles = """
    # <style>
    #     #MainMenu {visibility: hidden;}
    #     footer {visibility: hidden;}
    # </style>
    # """
    st.markdown(hide_streamlit_styles, unsafe_allow_html=True)
