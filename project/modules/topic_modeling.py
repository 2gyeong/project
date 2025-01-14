from gensim import corpora
from gensim.models import LdaModel
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
