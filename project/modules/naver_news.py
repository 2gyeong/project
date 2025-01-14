import streamlit as st
import json
import os
import re
from modules.visualization import generate_wordcloud_image, display_related_articles
from modules.topic_modeling import preprocess_data, perform_lda, generate_topic_labels_with_context

# 데이터 디렉토리와 카테고리 설정
DATA_DIR = "data"
CATEGORIES = ["정치", "경제", "사회", "생활/문화", "IT/과학", "세계"]

def render_naver_news_page():
    """
    네이버 뉴스 페이지를 렌더링합니다.
    """
    st.title("📰 네이버 뉴스")

    # 카테고리를 탭으로 생성
    tabs = st.tabs(CATEGORIES)

    for tab, category in zip(tabs, CATEGORIES):
        with tab:
            st.subheader(f"{category} 카테고리 분석")

            # 파일명 변환 (슬래시를 언더스코어로 대체)
            sanitized_category = category.replace("/", "_")
            file_path = os.path.join(DATA_DIR, f"{sanitized_category}.json")

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
                    #st.markdown("### 워드클라우드")
                    wordcloud_image = generate_wordcloud_image(
                        lda_model, dictionary, topic_id, font_path="/Library/Fonts/AppleGothic.ttf"
                    )

                    if wordcloud_image:
                        st.image(wordcloud_image, use_column_width=True)
                    else:
                        st.error("워드클라우드를 생성할 수 없습니다.")

                    # 관련 기사 표시
                    #st.markdown("### 관련 기사")
                    display_related_articles(lda_model, corpus, topic_id, articles)

            else:
                st.error(f"{category} 데이터를 찾을 수 없습니다.")
