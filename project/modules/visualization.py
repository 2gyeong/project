from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io


def generate_combined_wordcloud(lda_model, dictionary, num_topics, min_weight=0.01, width=800, height=400):
    """
    모든 토픽의 단어를 결합하여 하나의 워드클라우드를 생성합니다.
    :param lda_model: 학습된 LDA 모델
    :param dictionary: 단어 사전
    :param num_topics: LDA 모델의 토픽 수
    :param min_weight: 단어 필터링을 위한 최소 가중치
    :param width: 워드클라우드 이미지 폭
    :param height: 워드클라우드 이미지 높이
    :return: 워드클라우드 이미지 (BytesIO)
    """
    combined_frequencies = {}

    # 모든 토픽의 단어-가중치 데이터를 결합
    for topic_id in range(num_topics):
        topic_terms = lda_model.show_topic(topic_id, topn=50)  # 각 토픽의 상위 50개 단어
        for term_id, weight in topic_terms:
            if weight < min_weight:  # 최소 가중치 이하 단어 제거
                continue
            try:
                term = dictionary[int(term_id)]  # term_id를 숫자로 처리
            except (ValueError, KeyError):
                term = term_id  # term_id 자체가 단어인 경우
            if term in combined_frequencies:
                combined_frequencies[term] += weight
            else:
                combined_frequencies[term] = weight

    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path='/Library/Fonts/AppleGothic.ttf',
        width=width,
        height=height,
        background_color='white',
        min_font_size=5  # 최소 글자 크기 설정
    ).generate_from_frequencies(combined_frequencies)
    
    # 이미지 출력 준비
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return img
