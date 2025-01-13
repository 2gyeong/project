from konlpy.tag import Okt
import re
import os
import json
from gensim import corpora
from gensim.models import LdaModel

class TextProcessor:
    def __init__(self, language='korean'):
        self.okt = Okt()
        if language == 'korean':
            self.stop_words = set([
            '그리고', '그', '이', '저', '것', '등', '수', '들', '에서', '이다',
            '있다', '없다', '않다', '할', '를', '은', '는', '이', '가', '으로', '에게', '와', '과',
            '더', '또는', '그러나', '하지만', '그러므로', '때문에', '만약', '즉', '따라서', '그래서',
            '같이', '처럼', '만', '까지', '보다', '다시', '여기', '저기', '거기', '누구', '무엇', 
            '어디', '언제', '어떻게', '왜', '입니다', '그런', '이런', '저런', '합니다', '있습니다', 
            '없습니다', '하게', '하기', '한', '위해', '하고', '부터', '동안', '안', '밖', '위', '아래',
            '앞', '뒤', '옆', '이후', '전에', '현재', '다른', '모든', '각', '일부', '매우', '대부분',
            '조금', '아주', '항상', '자주', '가끔', '모두', '여러', '따로', '각각', '서로', '이미', 
            '안녕', '반갑습니다', '처럼', '정도', '비록', '관련', '결국', '사실', '게다가', '결과적으로',
            '대하여', '대해서', '대해', '한편', '그런데', '현재', '바로', '마침', '대체로', '확실히',
            '종종', '대개', '평소', '언젠가', '얼마나', '거의', '한번', '오히려', '비슷하게', '가령',
            '차라리', '왜냐하면', '그리하여', '그다지', '정말', '심지어', '게다가', '하지만', '반면에', '따르면', 
            '했다', '하는', '있는', '에는', '이라고', '라고', '있다고', '한다고', '했다고', '하지', '한다고', '때문'])

        else:
            self.stop_words = set()  # 기본값: 빈 불용어 목록

    def clean_text(self, text):
        """텍스트 정제: 특수문자 제거"""
        text = re.sub(r'[^가-힣\s]', '', text)  # 한국어와 공백만 남김
        return text.strip()

    def remove_stopwords(self, text):
        """불용어 제거"""
        words = self.okt.morphs(text)  # 형태소 분리
        return ' '.join(word for word in words if word not in self.stop_words)

    def process_text(self, text):
        """텍스트 정제 및 불용어 제거"""
        cleaned_text = self.clean_text(text)
        return self.remove_stopwords(cleaned_text)

def load_data(data_dir):
    """
    지정된 디렉터리에서 모든 JSON 파일을 읽어 텍스트 데이터를 로드합니다.
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
                    body = article.get('processed_body', '')  # 정제된 본문을 로드
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
        # 형태소 분석 및 불용어 제거
        tokens = [word for word in okt.morphs(text) if len(word) > 1]  # 길이가 1 이하인 단어 제거
        tokenized_texts.append(tokens)

    return tokenized_texts


# TextProcessor 초기화
processor = TextProcessor(language='korean')
