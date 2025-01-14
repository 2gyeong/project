from wordcloud import WordCloud
from io import BytesIO
import matplotlib.pyplot as plt
import random
import streamlit as st

def generate_wordcloud_image(lda_model, dictionary, topic_id, topn=10, font_path=None):
    """
    WordCloud 이미지를 생성합니다.
    """
    # LDA 모델에서 토픽의 단어-가중치 데이터 추출
    topic_terms = lda_model.show_topic(topic_id, topn=topn)
    if not topic_terms:
        st.error("선택된 토픽에 대한 단어 데이터가 없습니다.")
        return None

    word_frequencies = {term: weight for term, weight in topic_terms}

    # WordCloud 생성
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis",
        font_path=font_path or "/Library/Fonts/AppleGothic.ttf"  # 기본 폰트 설정
    ).generate_from_frequencies(word_frequencies)

    # 이미지를 BytesIO에 저장
    img_buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    plt.close()

    return img_buffer


def display_related_articles(lda_model, corpus, topic_id, articles):
    """
    선택된 토픽과 관련된 기사를 Streamlit에 표시합니다.
    :param lda_model: 학습된 LDA 모델
    :param corpus: Gensim 코퍼스 (문서의 BOW 표현)
    :param topic_id: 선택된 토픽 ID
    :param articles: 기사 데이터 (리스트 형식, 각 문서의 메타데이터 포함)
    """
    st.markdown(f"### Topic {topic_id + 1} 관련 기사")
    related_articles = []

    # 관련 문서 찾기
    for doc_id, doc in enumerate(corpus):
        doc_topics = lda_model.get_document_topics(doc)
        for t_id, weight in doc_topics:
            if t_id == topic_id and weight > 0.2:  # 가중치 기준
                related_articles.append(articles[doc_id])  # 관련 기사 저장

    # 관련 기사 표시
    if related_articles:
        for idx, article in enumerate(related_articles[:10], start=1):  # 최대 10개 기사 표시
            title = article.get('title', 'No title')
            link = article.get('link', '#')  # 링크가 없으면 기본값 #
            st.markdown(f"- **[{title}]({link})**")
    else:
        st.markdown("관련 기사가 없습니다.")

