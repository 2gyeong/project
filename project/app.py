# Streamlit 앱
import streamlit as st
from streamlit_option_menu import option_menu
from modules.naver_news import render_naver_news_page
from modules.real_estate import render_real_estate_page
from modules.sidebar import create_sidebar


# 사이드바 메뉴 생성
with st.sidebar:
    selected = create_sidebar()

# 네이버 뉴스 페이지
if selected == "네이버 뉴스":
    render_naver_news_page()

# 부동산 정보 페이지
elif selected == "부동산 정보":
    render_real_estate_page()
