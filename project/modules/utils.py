import streamlit as st

def convert_price(price_str):
    """가격 문자열을 정수로 변환"""
    try:
        price_str = price_str.replace(' ', '').replace(',', '')  # 공백과 콤마 제거
        if '억' in price_str:
            parts = price_str.split('억')
            return int(parts[0]) * 100000000 + (int(parts[1]) * 10000 if len(parts) > 1 and parts[1] else 0)
        elif '만' in price_str:
            return int(price_str.split('만')[0]) * 10000
        else:
            return int(price_str)
    except Exception as e:
        st.error(f"가격 변환 오류: {e}")
        return None


def format_price(price):
    """
    숫자를 '억', '천만', '백만' 단위로 변환
    """
    try:
        price = int(price)  # 숫자로 변환
    except ValueError:
        return "알 수 없음"

    if price >= 100000000:  # 억 단위 처리
        billions = price // 100000000
        remainder = price % 100000000
        if remainder >= 10000000:
            tens_of_millions = remainder // 10000000
            return f"{billions}억 {tens_of_millions}천만원"
        return f"{billions}억"
    elif price >= 10000:  # 만원 단위 처리
        tens_of_thousands = price // 10000
        return f"{tens_of_thousands}만원"
    else:  # 만원 미만
        return f"{price}원"

def parse_price(price_str):
    """
    '14억 5000만' 같은 문자열을 숫자로 변환
    """
    if isinstance(price_str, str):
        try:
            # 억과 만을 숫자로 변환
            price_str = price_str.replace(',', '').replace(' ', '')
            if '억' in price_str:
                parts = price_str.split('억')
                billions = int(parts[0]) * 100000000
                millions = int(parts[1]) * 10000 if len(parts) > 1 and parts[1] else 0
                return billions + millions
            elif '만' in price_str:
                return int(price_str.replace('만', '')) * 10000
            else:
                return int(price_str)
        except ValueError:
            return None
    return price_str
