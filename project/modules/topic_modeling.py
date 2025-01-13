from gensim import corpora
from gensim.models import LdaModel
from konlpy.tag import Okt
import re
import os
import json

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

