# Streamlit 앱
import streamlit as st
from modules.visualization import generate_wordcloud_image, display_related_articles
from modules.topic_modeling import preprocess_data, perform_lda
import json
import os

st.title("네이버 뉴스")

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

            # 토픽 선택
            selected_topic = st.selectbox(
                "토픽을 선택하세요:",
                [f"Topic {i + 1}" for i in range(len(topics))],
                key=f"{sanitized_category}_topic_selectbox"
            )

            if selected_topic:
                topic_id = int(selected_topic.split()[1]) - 1  # Topic ID 추출

                # 워드클라우드 생성 및 표시 (이미지 기반)
                st.markdown("### 워드클라우드")
                wordcloud_image = generate_wordcloud_image(lda_model, dictionary, topic_id)

                # 관련 기사 표시
                display_related_articles(lda_model, corpus, topic_id, articles)
        else:
            st.error(f"{category} 데이터를 찾을 수 없습니다.")
