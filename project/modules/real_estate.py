import os
import json
import streamlit as st
from modules.fetch_data import get_apartments
from modules.utils import convert_price, format_price
from modules.visualization import create_dataframe, create_bar_chart
import pandas as pd

def render_real_estate_page():
    st.title("부동산 정보")

    # JSON 파일 경로
    base_path = os.path.dirname(os.path.abspath(__file__))
    dong_options_path = os.path.join(base_path, '../data/dong_options.json')

    # JSON 파일 로드
    try:
        with open(dong_options_path, 'r', encoding='utf-8') as f:
            dong_options = json.load(f)
    except FileNotFoundError:
        st.error("법정동 데이터를 불러오지 못했습니다. JSON 파일 경로를 확인하세요.")
        return
    except json.JSONDecodeError:
        st.error("JSON 파일을 파싱하는 중 오류가 발생했습니다. 파일 형식을 확인하세요.")
        return

    # 법정동 선택
    selected_dong = st.selectbox("법정동을 선택하세요:", list(dong_options.keys()))

    # 탭 생성
    tab_50_60, tab_80_90, tab_average = st.tabs(["50~60㎡", "80~90㎡", "동별 평균 매매/전세"])

    # 50~60㎡ 탭 내용
    with tab_50_60:
        st.subheader("50~60㎡ 아파트 데이터")
        data_type_50_60 = st.radio("거래 유형을 선택하세요:", ("매매", "전세"), horizontal=True, key="data_type_50_60")
        if st.button("50~60㎡ 조회"):
            process_real_estate_data(selected_dong, dong_options, data_type_50_60, 50, 60)

    # 80~90㎡ 탭 내용
    with tab_80_90:
        st.subheader("80~90㎡ 아파트 데이터")
        data_type_80_90 = st.radio("거래 유형을 선택하세요:", ("매매", "전세"), horizontal=True, key="data_type_80_90")
        if st.button("80~90㎡ 조회"):
            process_real_estate_data(selected_dong, dong_options, data_type_80_90, 80, 90)

    # 동별 평균 매매/전세 탭 내용
    with tab_average:
        st.subheader("동별 평균 매매/전세 데이터")
        st.write("이 섹션에서 동별 평균 매매 및 전세 가격을 표시합니다. 데이터 분석 로직 추가 필요.")

def process_real_estate_data(selected_dong, dong_options, data_type, area_min, area_max):
    """
    특정 면적과 거래 유형에 따라 데이터를 필터링하고 시각화합니다.
    """
    try:
        apartments = get_apartments(selected_dong, dong_options)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return

    if apartments:
        # 데이터프레임 생성 및 필터링
        try:
            filtered_df = create_dataframe(apartments, data_type)

            # '전용면적' 컬럼 숫자 변환
            filtered_df['전용면적'] = pd.to_numeric(filtered_df['전용면적'], errors='coerce')
            filtered_df = filtered_df.dropna(subset=['전용면적'])  # 변환 실패한 값 제거
            filtered_df = filtered_df[(filtered_df['전용면적'] >= area_min) & (filtered_df['전용면적'] < area_max)]
        except KeyError as e:
            st.error(f"데이터 필터링 중 오류가 발생했습니다: {e}")
            return
        except Exception as e:
            st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
            return

        if not filtered_df.empty:
            st.dataframe(filtered_df)

            # 차트 생성
            chart = create_bar_chart(filtered_df, f"{area_min}~{area_max}㎡ - {data_type} 아파트 가격")
            if chart:
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("차트를 생성할 수 있는 데이터가 없습니다.")
        else:
            st.warning(f"{area_min}~{area_max}㎡에 해당하는 {data_type} 데이터가 없습니다.")
    else:
        st.error("아파트 데이터를 가져오지 못했습니다.")

