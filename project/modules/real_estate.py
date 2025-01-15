import os
import json
import streamlit as st
import altair as alt
import pandas as pd
from modules.fetch_data import get_apartments
from modules.utils import convert_price
from modules.visualization import create_dataframe, create_bar_chart

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

        # 50~60㎡ 동별 평균 매매/전세
        with st.expander("50~60㎡ 동별 평균 매매/전세"):
            calculate_and_display_average_prices(dong_options, 50, 60)

        # 80~90㎡ 동별 평균 매매/전세
        with st.expander("80~90㎡ 동별 평균 매매/전세"):
            calculate_and_display_average_prices(dong_options, 80, 90)

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

def calculate_and_display_average_prices(dong_options, area_min, area_max):
    """
    주어진 면적 범위에 대한 동별 평균 매매가 및 전세가를 계산하고 표시합니다.
    """
    average_prices = []
    average_rent_prices = []
    for dong in dong_options.keys():
        apartments = get_apartments(dong, dong_options)
        sale_prices = []
        rent_prices = []
        for apt in apartments:
            area_value = float(apt['area']) if apt['area'] else 0
            price_value = convert_price(apt['price']) if apt['price'] else None
            if area_min <= area_value < area_max:
                if apt['transaction_type'] == '매매' and price_value is not None:
                    sale_prices.append(price_value)
                elif apt['transaction_type'] == '전세' and price_value is not None:
                    rent_prices.append(price_value)
        average_sale_price = sum(sale_prices) / len(sale_prices) if sale_prices else 0
        average_rent_price = sum(rent_prices) / len(rent_prices) if rent_prices else 0
        average_prices.append({'법정동': dong, '평균 매매가': average_sale_price / 100000000})
        average_rent_prices.append({'법정동': dong, '평균 전세가': average_rent_price / 100000000})

    df_avg_prices = pd.DataFrame(average_prices)
    df_avg_rent_prices = pd.DataFrame(average_rent_prices)
    df_combined = pd.merge(df_avg_prices, df_avg_rent_prices, on='법정동')

    st.write(f"{area_min}~{area_max}㎡ 동별 평균 매매가 및 전세가")

    # 시각화
    line_chart = alt.Chart(df_combined).mark_line(point=True).encode(
        x='법정동:N',
        y=alt.Y('평균 매매가:Q', title='가격(억)'),
        color=alt.value('red'),
        tooltip=[alt.Tooltip('법정동:N', title='법정동'), alt.Tooltip('평균 매매가:Q', title='가격(억)')]
    )
    line_chart_rent = alt.Chart(df_combined).mark_line(point=True).encode(
        x='법정동:N',
        y=alt.Y('평균 전세가:Q', title='가격(억)'),
        color=alt.value('blue'),
        tooltip=[alt.Tooltip('법정동:N', title='법정동'), alt.Tooltip('평균 전세가:Q', title='가격(억)')]
    )
    combined_chart = line_chart + line_chart_rent
    st.altair_chart(combined_chart, use_container_width=True)
