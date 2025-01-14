from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import wordnet as wn
from konlpy.tag import Okt
import re

def preprocess_data(texts):
    """
    텍스트 전처리 및 토큰화
    """
    okt = Okt()
    tokenized_texts = []
    for text in texts:
        text = re.sub(r'[^가-힣\s]', '', text).strip()
        tokens = [word for word in okt.morphs(text) if len(word) > 1]
        tokenized_texts.append(tokens)
    return tokenized_texts

def perform_lda(tokenized_texts, num_topics=5, passes=15):
    """
    LDA 모델 학습
    """
    dictionary = corpora.Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
    lda_model = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    topics = lda_model.show_topics(num_topics=num_topics, num_words=5, formatted=True)
    return lda_model, corpus, dictionary, topics

def generate_topic_labels(lda_model, num_topics, topn=5):
    """
    토픽 키워드를 기반으로 주제를 자동 생성합니다.
    :param lda_model: 학습된 LDA 모델
    :param num_topics: 전체 토픽 수
    :param topn: 각 토픽에서 상위 키워드 개수
    :return: 생성된 토픽 주제 리스트
    """
    topic_labels = []

    for topic_id in range(num_topics):
        # 상위 키워드 추출
        topic_terms = lda_model.show_topic(topic_id, topn=topn)
        keywords = [term for term, _ in topic_terms]

        # 키워드를 조합하여 주제 생성
        label = ", ".join(keywords[:3])  # 상위 3개의 키워드 사용
        topic_labels.append(f"Topic {topic_id + 1}: {label}")

    return topic_labels

def generate_topic_labels_with_context(lda_model, num_topics, topn=5, language="kor"):
    """
    WordNet 또는 KorLex를 사용하여 자연스러운 주제를 생성합니다.
    :param lda_model: 학습된 LDA 모델
    :param num_topics: 전체 토픽 수
    :param topn: 각 토픽에서 상위 키워드 개수
    :param language: "eng" 또는 "kor" (언어 선택)
    :return: 생성된 토픽 주제 리스트
    """
    topic_labels = []

    for topic_id in range(num_topics):
        # 상위 키워드 추출
        topic_terms = lda_model.show_topic(topic_id, topn=topn)
        keywords = [term for term, _ in topic_terms]

        if language == "eng":
            # WordNet 기반 주제 생성
            related_words = []
            for keyword in keywords:
                synsets = wn.synsets(keyword)
                if synsets:
                    related_words.append(synsets[0].definition())

            label = f"{keywords[0]} : {', '.join(keywords[1:])}"
            if related_words:
                label += f" ({', '.join(related_words)})"
        else:
            # KorLex 기반 주제 생성
            okt = Okt()
            analyzed_keywords = [" ".join(okt.morphs(keyword)) for keyword in keywords]
            label = f"주제 : {analyzed_keywords[0]}, 키워드: {', '.join(analyzed_keywords[1:])}"

        topic_labels.append(f"{topic_id + 1}. {label}")

    return topic_labels