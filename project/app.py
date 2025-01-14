# Streamlit 앱
import streamlit as st
from streamlit_option_menu import option_menu
from modules.naver_news import render_naver_news_page
from modules.real_estate import render_real_estate_page
from modules.sidebar import create_sidebar

# 사이드바 메뉴 생성
with st.sidebar:
    selected = create_sidebar()

# 메인 페이지
if selected == "메인 페이지":
    st.title("📚 메인 페이지")
    st.write("환영합니다! 왼쪽 메뉴에서 원하는 페이지를 선택하세요.")

# 네이버 뉴스 페이지
elif selected == "네이버 뉴스":
    render_naver_news_page()

# 부동산 정보 페이지
elif selected == "부동산 정보":
    render_real_estate_page()
