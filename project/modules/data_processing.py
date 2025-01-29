import pandas as pd
from modules.utils import convert_price

def filter_apartments_by_area(apartments, area_range):
    min_area, max_area = map(float, area_range.split('~'))
    return [apt for apt in apartments if min_area <= float(apt['area'] or 0) < max_area]

def process_apartments(apartments, area_range, transaction_type):
    filtered_apartments = filter_apartments_by_area(apartments, area_range)
    df = pd.DataFrame(filtered_apartments)
    df = df[df['transaction_type'] == transaction_type]
    df['가격'] = df['price'].apply(lambda x: convert_price(x))
    df.sort_values(by='가격', inplace=True)
    return df
