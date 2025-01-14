import streamlit as st
from streamlit_option_menu import option_menu

def create_sidebar():
    return option_menu(
        "메뉴",
        ["네이버 뉴스", "부동산 데이터"],
        icons=["newspaper", "building"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#FAFAFA"},
            "icon": {"color": "#1F77B4", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#F0F8FF",
            },
            "nav-link-selected": {"background-color": "#87CEFA", "font-weight": "bold"},  # 선택된 메뉴 배경 하늘색, 텍스트 볼드
        },
    )
