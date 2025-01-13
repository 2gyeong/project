from konlpy.tag import Okt
import re

class TextProcessor:
    def __init__(self, language='korean'):
        self.okt = Okt()
        if language == 'korean':
            self.stop_words = set(['그리고', '그', '이', '저', '것', '등', '수', '들', '에서', '이다',
                                   '있다', '없다', '않다', '할', '를', '은', '는', '이', '가', '으로', '에게', '와', '과'])
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

# 초기화
processor = TextProcessor(language='korean')
