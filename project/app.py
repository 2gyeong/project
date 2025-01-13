import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import os
import json
from modules.text_processing import TextProcessor
from modules.topic_modeling import preprocess_data, perform_lda
from modules.visualization import generate_combined_wordcloud
# test
class NewsCrawler:
    def __init__(self, ajax_url):
        self.ajax_url = ajax_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9',
        }

    def fetch_articles(self, sid, start_page=1, max_pages=5):
        articles = []
        next_value = None
        for page_no in range(start_page, start_page + max_pages):
            params = {
                'sid': sid,
                'sid2': '',
                'cluid': '',
                'pageNo': page_no,
                'date': '',
                'next': next_value,
                '_': int(time.time() * 1000),
            }
            response = requests.get(self.ajax_url, params=params, headers=self.headers)

            if response.status_code != 200:
                st.warning(f"Failed to fetch page {page_no} for sid {sid}: HTTP {response.status_code}")
                break

            try:
                data = response.json()
                html_content = data.get("renderedComponent", {}).get("SECTION_ARTICLE_LIST", "")
                soup = BeautifulSoup(html_content, 'html.parser')

                for item in soup.select('.sa_list li.sa_item'):
                    title_tag = item.select_one('.sa_text a')
                    title = title_tag.get_text(strip=True) if title_tag else "No title"
                    link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else "No link"
                    articles.append({'title': title, 'link': link})

                next_cursor_tag = soup.select_one('div[data-cursor]')
                next_value = next_cursor_tag.get('data-cursor') if next_cursor_tag else None

                if not next_value:
                    st.info(f"No more pages to fetch for sid {sid}.")
                    break
            except Exception as e:
                st.error(f"Error parsing response for page {page_no} and sid {sid}: {e}")
                break

        return articles
    
    def fetch_article_content(self, url):
        """개별 기사 페이지에서 제목과 본문 크롤링"""
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            title = soup.select_one('.media_end_head_headline').get_text(strip=True)
            body = soup.select_one('#dic_area').get_text(strip=True)
            return {'title': title, 'body': body}
        except Exception as e:
            return None

# 데이터 저장 경로 설정
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Streamlit 앱 구현
st.title("네이버 뉴스")

# 카테고리와 sid 매핑
data_categories = {
    "정치": 100,
    "경제": 101,
    "사회": 102,
    "생활/문화": 103,
    "IT/과학": 105,
    "세계": 104
}

# TextProcessor 초기화 (한국어 처리)
processor = TextProcessor()

# 사용자 입력받기 (탭으로 구현)
tabs = st.tabs(list(data_categories.keys()))

for tab, (category, sid) in zip(tabs, data_categories.items()):
    with tab:
        ajax_url = 'https://news.naver.com/section/template/SECTION_ARTICLE_LIST'
        crawler = NewsCrawler(ajax_url)

        articles = crawler.fetch_articles(sid=sid, start_page=1, max_pages=2)  # 최대 2페이지만 가져오기

        if articles:
            detailed_articles = []
            category_texts = []

            for article in articles:
                if 'link' not in article or not article['link']:
                    st.warning(f"Skipping article without a valid link: {article.get('title', 'No title')}")
                    continue  # 링크가 없는 기사 건너뛰기

                content = crawler.fetch_article_content(article['link'])
                if content:
                    # 텍스트 정제 및 불용어 제거 수행
                    processed_body = processor.process_text(content['body'])
                    content['processed_body'] = processed_body
                    detailed_articles.append(content)
                    category_texts.append(processed_body)

            # JSON 파일로 저장
            sanitized_category = category.replace("/", "_")
            file_path = os.path.join(data_dir, f"{sanitized_category}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(detailed_articles, f, ensure_ascii=False, indent=4)

            # 기사 출력
            max_display = st.slider(
                f"{category} 표시할 기사 수 선택",
                min_value=1,
                max_value=min(len(detailed_articles), 72),
                value=10,
                key=f"slider_{category}"
            )

            for idx, article in enumerate(detailed_articles, start=1):
                title = article.get('title', 'No title')
                link = article.get('link', '#')  # 링크가 없는 경우 기본값으로 설정
                st.markdown(f"**{idx}. [ {title} ]({link})**")
                if idx >= max_display:
                    break

            # LDA 토픽 모델링 실행
            if st.button(f"{category} 토픽 모델링 실행"):
                st.markdown(f"### {category} 카테고리의 토픽 모델링 결과")
                tokenized_texts = preprocess_data(category_texts)
                lda_model, corpus, dictionary, topics = perform_lda(tokenized_texts, num_topics=5, passes=15)

                # 토픽 출력
                for idx, topic in enumerate(topics, start=1):
                    st.markdown(f"**Topic {idx}:** {topic[1]}")

                # 워드클라우드 생성 및 출력
                st.markdown(f"### {category} 카테고리의 워드클라우드")
                category_wc_image = generate_combined_wordcloud(lda_model, dictionary, num_topics=5)
                st.image(category_wc_image, caption=f"{category} 카테고리 워드클라우드")
        else:
            st.warning(f"No articles found for {category}.")
