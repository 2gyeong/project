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
    """가격을 '억', '만', '천' 단위로 포맷팅"""
    # 이미 '억', '만' 단위가 포함된 경우 그대로 반환
    if isinstance(price, str) and ('억' in price or '만' in price or '천' in price):
        return price

    try:
        price = int(price)  # 정수로 변환
    except ValueError:
        raise ValueError(f"Invalid price format: {price}")

    if price >= 100000000:
        return f"{price // 100000000}억"
    elif price >= 10000:
        return f"{price // 10000}만"
    elif price >= 1000:
        return f"{price // 1000}천"
    else:
        return f"{price}원"
