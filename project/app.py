# Streamlit 앱
import streamlit as st
from streamlit_option_menu import option_menu
from modules.visualization import generate_wordcloud_image, display_related_articles
from modules.topic_modeling import preprocess_data, perform_lda, generate_topic_labels_with_context
import json
import os
import re


# 사이드바 메뉴 생성
with st.sidebar:
    choice = option_menu("Menu", ["네이버 뉴스", "부동산 정보"],
                         icons=['newspaper', 'building'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#f0f2f6"},
                             "icon": {"color": "black", "font-size": "20px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e0f7f4"},
                             "nav-link-selected": {"background-color": "#08c7b4", "color": "white"},
                         }
                         )

# 네이버 뉴스 페이지
if choice == "네이버 뉴스":
    st.title("📰 네이버 뉴스")
    # 예시: 데이터 분석, 워드클라우드, 관련 기사 표시 등

# 부동산 정보 페이지
elif choice == "부동산 정보":
    st.title("🏢 부동산 정보")
    
# 데이터 디렉토리와 카테고리 설정
data_dir = "data"
categories = ["정치", "경제", "사회", "생활/문화", "IT/과학", "세계"]

# 카테고리를 탭으로 생성
tabs = st.tabs(categories)

for tab, category in zip(tabs, categories):
    with tab:
        st.subheader(f"{category} 카테고리 분석")

        # 파일명 변환 (슬래시를 언더스코어로 대체)
        sanitized_category = category.replace("/", "_")
        file_path = os.path.join(data_dir, f"{sanitized_category}.json")

        # 데이터 로드
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                articles = json.load(f)  # 기사 데이터 로드

            # 텍스트 데이터 전처리
            category_texts = [article['processed_body'] for article in articles]
            tokenized_texts = preprocess_data(category_texts)

            # LDA 모델 학습
            lda_model, corpus, dictionary, topics = perform_lda(tokenized_texts, num_topics=5, passes=15)

            # WordNet/KorLex 기반으로 자연스러운 주제 생성
            topic_labels = generate_topic_labels_with_context(lda_model, num_topics=5, topn=5, language="kor")

            # 토픽 선택 (주제 표시)
            selected_topic_label = st.selectbox(
                "토픽을 선택하세요:",
                topic_labels,
                key=f"{sanitized_category}_topic_selectbox"
            )

            if selected_topic_label:
                # 선택한 토픽 ID 추출
                topic_id = int(re.search(r'\d+', selected_topic_label).group()) - 1

                # 워드클라우드 생성 및 표시 (이미지 기반)
                wordcloud_image = generate_wordcloud_image(lda_model, dictionary, topic_id, font_path="/Library/Fonts/AppleGothic.ttf")

                if wordcloud_image:
                    st.image(wordcloud_image, use_column_width=True)
                else:
                    st.error("워드클라우드를 생성할 수 없습니다.")

                # 관련 기사 표시
                display_related_articles(lda_model, corpus, topic_id, articles)
                
        else:
            st.error(f"{category} 데이터를 찾을 수 없습니다.")
