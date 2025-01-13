import requests
from bs4 import BeautifulSoup
import time

base_url = 'https://news.naver.com'
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
                print(f"Failed to fetch page {page_no} for sid {sid}: HTTP {response.status_code}")
                break

            try:
                data = response.json()
                html_content = data.get("renderedComponent", {}).get("SECTION_ARTICLE_LIST", "")
                soup = BeautifulSoup(html_content, 'html.parser')


                for item in soup.select('.sa_list li.sa_item'):
                    title_tag = item.select_one('.sa_text a')
                    title = title_tag.get_text(strip=True) if title_tag else "No title"

                    # Generate the full URL using oid and aid
                    oid = item.get('data-oid')  # 데이터 키 확인 필요
                    aid = item.get('data-aid')  # 데이터 키 확인 필요

                    link = f"{base_url}{title_tag['href']}" if title_tag and 'href' in title_tag.attrs else "No link"
                    articles.append({'title': title, 'link': link})

                next_cursor_tag = soup.select_one('div[data-cursor]')
                next_value = next_cursor_tag.get('data-cursor') if next_cursor_tag else None

                if not next_value:
                    print(f"No more pages to fetch for sid {sid}.")
                    break
            except Exception as e:
                print(f"Error parsing response for page {page_no} and sid {sid}: {e}")
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
            print(f"Error parsing article content: {e}")
            return None
