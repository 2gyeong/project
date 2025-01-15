import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
from modules.utils import convert_price
from wordcloud import WordCloud
from io import BytesIO


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



def create_dataframe(data, transaction_type):
    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # 필요한 키가 데이터에 포함되어 있는지 확인
    required_columns = ['name', 'price', 'transaction_type', 'area', 'floor']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"필수 컬럼 '{col}'이(가) 데이터에 없습니다.")
            return pd.DataFrame()  # 빈 데이터프레임 반환

    # 선택한 거래 유형 필터링
    df = df[df['transaction_type'] == transaction_type]

    # 컬럼 이름 매핑
    df.rename(columns={
        'name': '단지명',
        'price': '가격',
        'area': '전용면적',
        'floor': '현재 층/전체 층'
    }, inplace=True)

    # 가격 변환
    try:
        df['가격'] = df['가격'].apply(convert_price)
    except Exception as e:
        st.error(f"가격 데이터를 변환하는 중 오류 발생: {e}")
        return pd.DataFrame()

    return df



def create_bar_chart(df, title):
    # 데이터프레임이 비어 있는 경우 처리
    if df.empty:
        st.warning("차트를 생성할 데이터가 없습니다.")
        return None

    # 단지명을 문자열로 변환
    df['단지명'] = df['단지명'].astype(str)

    # Altair 바 차트 생성
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('단지명:N', sort='-y', title="단지명"),
        y=alt.Y('가격:Q', title="가격 (억)"),
        tooltip=['단지명', '가격', '전용면적', '현재 층/전체 층']
    ).properties(
        title=title,
        width=700,
        height=400
    )
    return chart



def create_bar_chart(df, title):
    # 데이터프레임이 비어 있는 경우 처리
    if df.empty:
        st.warning("차트를 생성할 데이터가 없습니다.")
        return None

    # 데이터 타입 변환
    df['단지명'] = df['단지명'].astype(str)  # 범주형
    df['가격'] = pd.to_numeric(df['가격'], errors='coerce')  # 수치형

    # 결측값 제거
    df = df.dropna(subset=['단지명', '가격'])

    # Altair 바 차트 생성
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('단지명:N', sort='-y', title="단지명"),
        y=alt.Y('가격:Q', title="가격 (억)"),
        tooltip=['단지명', '가격', '전용면적', '현재 층/전체 층']
    ).properties(
        title=title,
        width=700,
        height=400
    )
    return chart



def create_heatmap(df, title):
    if df.empty:
        st.write(f"{title} 데이터가 없습니다.")
        return
    price_matrix = df.pivot_table(index='단지명', values='가격', aggfunc='mean')
    price_matrix = price_matrix.sort_values(by='가격', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.heatmap(price_matrix, annot=True, fmt=".0f", cmap="coolwarm")
    plt.title(title)
    st.pyplot(plt)