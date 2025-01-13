from gensim import corpora
from gensim.models import LdaModel
from konlpy.tag import Okt
from wordcloud import WordCloud
import re
import os
import json
import matplotlib.pyplot as plt
import io


def load_data(data_dir):
    """
    지정된 디렉터리에서 JSON 파일을 읽어 텍스트 데이터를 로드합니다.
    :param data_dir: JSON 파일이 저장된 디렉터리 경로
    :return: 텍스트 데이터 리스트
    """
    all_texts = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(data_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                for article in articles:
                    body = article.get('processed_body', '')  # 정제된 본문 로드
                    if body:
                        all_texts.append(body)
    return all_texts

def preprocess_data(texts):
    """텍스트 데이터 전처리 및 토큰화"""
    okt = Okt()
    tokenized_texts = []

    for text in texts:
        # 텍스트 정제 (특수문자 제거)
        text = re.sub(r'[^가-힣\s]', '', text)
        text = text.strip()  # 공백 제거
        # 형태소 분석 및 불용어 제거
        tokens = [word for word in okt.morphs(text) if len(word) > 1]  # 길이가 1 이하인 단어 제거
        tokenized_texts.append(tokens)

    return tokenized_texts

def perform_lda(tokenized_texts, num_topics=5, passes=15):
    """LDA 토픽 모델링 수행"""
    # 단어 사전 생성
    dictionary = corpora.Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

    # LDA 모델 학습
    lda_model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=passes)

    # 토픽 출력
    topics = lda_model.print_topics(num_words=5)
    return lda_model, corpus, dictionary, topics

def generate_combined_wordcloud(lda_model, dictionary, num_topics, width=800, height=400):
    """
    모든 토픽의 단어를 결합하여 하나의 워드클라우드를 생성합니다.
    :param lda_model: 학습된 LDA 모델
    :param dictionary: 단어 사전
    :param num_topics: LDA 모델의 토픽 수
    :param width: 워드클라우드 이미지 폭
    :param height: 워드클라우드 이미지 높이
    :return: 워드클라우드 이미지 (BytesIO)
    """
    combined_frequencies = {}

    # 모든 토픽의 단어-가중치 데이터를 결합
    for topic_id in range(num_topics):
        topic_terms = lda_model.show_topic(topic_id, topn=50)  # 각 토픽의 상위 50개 단어
        for term_id, weight in topic_terms:
            try:
                term = dictionary[int(term_id)]  # term_id를 숫자로 처리
            except (ValueError, KeyError):
                term = term_id  # term_id 자체가 단어인 경우
            if term in combined_frequencies:
                combined_frequencies[term] += weight
            else:
                combined_frequencies[term] = weight

    # 워드클라우드 생성
    wordcloud = WordCloud(font_path='/Library/Fonts/AppleGothic.ttf', width=width, height=height, background_color='white').generate_from_frequencies(combined_frequencies)
    
    # 이미지 출력 준비
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return img