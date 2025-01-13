import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

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

# Streamlit 앱 구현
st.title("News Crawler App")
st.subheader("Select a category to fetch the latest news articles")

# 카테고리와 sid 매핑
data_categories = {
    "Politics": 100,
    "Economy": 101,
    "Society": 102,
    "Lifestyle": 103,
    "Science": 105,
    "World": 104
}

# 사용자 입력받기
selected_category = st.selectbox("Choose a category", options=list(data_categories.keys()))

if selected_category:
    sid = data_categories[selected_category]
    ajax_url = 'https://news.naver.com/section/template/SECTION_ARTICLE_LIST'
    crawler = NewsCrawler(ajax_url)

    st.write(f"Fetching articles for **{selected_category}**...")
    articles = crawler.fetch_articles(sid=sid, start_page=1, max_pages=2)  # 최대 2페이지만 가져오기

    if articles:
        st.success(f"Fetched {len(articles)} articles from {selected_category}.")
        for idx, article in enumerate(articles, start=1):
            st.markdown(f"**{idx}. [ {article['title']} ]({article['link']})**")
            if idx >= 10:  # 최대 10개의 기사만 표시
                break
    else:
        st.warning("No articles found or failed to fetch articles.")
