import os
import json
import streamlit as st
from modules.fetch_data import get_apartments
from modules.utils import convert_price, format_price
from modules.visualization import create_dataframe, create_bar_chart

def render_real_estate_page():
    st.title("부동산 정보")

    # JSON 파일 경로
    base_path = os.path.dirname(os.path.abspath(__file__))
    dong_options_path = os.path.join(base_path, '../data/dong_options.json')

    with open(dong_options_path, 'r') as f:
        dong_options = json.load(f)
        
    # 법정동 선택
    selected_dong = st.selectbox("법정동을 선택하세요:", list(dong_options.keys()))
    # 데이터 유형 선택 (매매/전세)
    data_type = st.radio("",("매매", "전세"), horizontal=True)

    if st.button("조회"):
        
        # 데이터 가져오기
        apartments = get_apartments(selected_dong, dong_options)

        if apartments:
            # 데이터프레임 생성
            filtered_df = create_dataframe(apartments, data_type)

            if not filtered_df.empty:
                st.subheader(f"{data_type} 데이터")
                st.dataframe(filtered_df)
                st.altair_chart(create_bar_chart(filtered_df, f"{data_type} 아파트 가격"), use_container_width=True)
            else:
                st.warning(f"{data_type} 데이터가 없습니다.")
        else:
            st.error("데이터를 가져오지 못했습니다.")
