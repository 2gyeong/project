import requests
import time
import random
import json
import os
import streamlit as st
from modules.visualization import create_dataframe, create_bar_chart


def fetch_apartments(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
        if response.status_code != 200:
            raise Exception(f"HTTP 오류: 상태 코드 {response.status_code}")

        if not response.text.strip():
            raise Exception("응답이 비어 있습니다.")

        try:
            data = response.json()  # JSON 변환 시도
        except ValueError as ve:
            raise Exception("JSON 파싱 오류: 응답이 JSON 형식이 아닙니다.") from ve

        return data

    except requests.RequestException as e:
        raise Exception(f"API 요청 중 오류가 발생했습니다: {e}")


def get_apartments(selected_dong, dong_options, max_pages=15):
    """
    선택된 동의 아파트 데이터를 가져옵니다.
    """
    url_template = (
        'https://m.land.naver.com/cluster/ajax/articleList?rletTpCd=APT'
        '&tradTpCd=A1%3AB1&z={z}&lat={lat}&lon={lon}&btm={btm}&lft={lft}'
        '&top={top}&rgt={rgt}&spcMin=66&spcMax=132&showR0=&totCnt={totCnt}'
        '&cortarNo={cortarNo}&sort=rank&page={page}'
    )
    apartments = []
    seen_ids = set()  # 중복 제거를 위한 ID 저장소

    for page in range(1, max_pages + 1):
        url = url_template.format(**dong_options[selected_dong], page=page)
        try:
            data = fetch_apartments(url)
            if not data.get('body'):
                print(f"페이지 {page}: 데이터 없음.")
                break

            for item in data['body']:
                # 고유 ID를 기준으로 중복 검사
                apt_id = item.get('atclNo')  # 고유 ID
                if apt_id and apt_id not in seen_ids:
                    seen_ids.add(apt_id)
                    apartments.append({
                        'name': item.get('atclNm', '알 수 없음'),
                        'price': item.get('hanPrc', '정보 없음'),
                        'transaction_type': item.get('tradTpNm', '알 수 없음'),
                        'area': item.get('spc2', '정보 없음'),
                        'floor': item.get('flrInfo', '정보 없음')
                    })

            print(f"페이지 {page}: {len(data['body'])}개의 데이터 수집 완료.")
            time.sleep(random.uniform(1, 2))  # 요청 간 간격 두기

        except Exception as e:
            print(f"오류 발생: {e}")
            break

    print(f"총 {len(apartments)}개의 아파트 데이터 수집 완료.")
    return apartments


def render_real_estate_page():
    st.title("부동산 정보")

    # JSON 파일 경로
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        dong_options_path = os.path.join(base_path, '../data/dong_options.json')

        # JSON 파일 로드
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
    # 데이터 유형 선택 (매매/전세)
    data_type = st.radio("", ("매매", "전세"), horizontal=True)

    if st.button("조회"):
        # 데이터 가져오기
        try:
            apartments = get_apartments(selected_dong, dong_options)
        except Exception as e:
            st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
            return

        if apartments:
            # 데이터프레임 생성
            filtered_df = create_dataframe(apartments, data_type)

            if not filtered_df.empty:
                st.subheader(f"{data_type} 데이터")
                st.dataframe(filtered_df)

                # 바 차트 생성
                chart = create_bar_chart(filtered_df, f"{data_type} 아파트 가격")
                if chart:
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("차트를 생성할 수 있는 데이터가 없습니다.")
            else:
                st.warning(f"{data_type} 데이터가 없습니다.")
        else:
            st.error("아파트 데이터를 가져오지 못했습니다.")
