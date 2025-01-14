import requests
import time
import random

def fetch_apartments(url):
    """
    주어진 URL로 아파트 데이터를 가져옵니다.
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        raise Exception(f"오류 발생: {response.status_code} - {response.text}")
    return response.json()

def get_apartments(selected_dong, dong_options, max_pages=15):
    """
    선택된 동의 아파트 데이터를 가져옵니다.
    """
    url_template = (
        'https://m.land.naver.com/cluster/ajax/articleList?rletTpCd=APT'
        '&tradTpCd=A1%3AB1&z={z}&lat={lat}&lon={lon}&btm={btm}&lft={lft}'
        '&top={top}&rgt={rgt}&spcMin=66&spcMax=132&showR0=&totCnt={totCnt}'
        '&cortarNo={cortarNo}&sort=rank&page={page}'
    )
    apartments = []
    seen_ids = set()  # 중복 제거를 위한 ID 저장소

    for page in range(1, max_pages + 1):
        url = url_template.format(**dong_options[selected_dong], page=page)
        try:
            data = fetch_apartments(url)
            if not data.get('body'):
                print(f"페이지 {page}: 데이터 없음.")
                break

            for item in data['body']:
                # 고유 ID를 기준으로 중복 검사
                apt_id = item.get('atclNo')  # 고유 ID
                if apt_id and apt_id not in seen_ids:
                    seen_ids.add(apt_id)
                    apartments.append({
                        'name': item.get('atclNm', '알 수 없음'),
                        'price': item.get('hanPrc', '정보 없음'),
                        'transaction_type': item.get('tradTpNm', '알 수 없음'),
                        'area': item.get('spc2', '정보 없음'),
                        'floor': item.get('flrInfo', '정보 없음')
                    })

            print(f"페이지 {page}: {len(data['body'])}개의 데이터 수집 완료.")
            time.sleep(random.uniform(1, 2))  # 요청 간 간격 두기

        except Exception as e:
            print(f"오류 발생: {e}")
            break

    print(f"총 {len(apartments)}개의 아파트 데이터 수집 완료.")
    return apartments
