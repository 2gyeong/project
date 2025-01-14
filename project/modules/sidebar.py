from streamlit_option_menu import option_menu

def create_sidebar():
    return option_menu(
        "메뉴",
        ["메인 페이지", "네이버 뉴스", "부동산 정보"],
        icons=["house", "newspaper", "building"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#FAFAFA"},
            "icon": {"color": "blue", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#E0F7FA",
            },
            "nav-link-selected": {"background-color": "#B3E5FC", "font-weight": "bold"},
        },
    )
