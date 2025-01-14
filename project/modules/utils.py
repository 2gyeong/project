def convert_price(price_str):
    """가격 문자열을 정수로 변환"""
    price_str = price_str.replace(' ', '')
    if '억' in price_str:
        main, sub = price_str.split('억')[0], price_str.split('억')[1].split('만')[0] if '만' in price_str else 0
        return int(main) * 100000000 + int(sub) * 10000
    elif '만' in price_str:
        return int(price_str.split('만')[0]) * 10000
    return int(price_str.replace(',', ''))

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
