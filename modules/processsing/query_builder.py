# modules/processing/query_builder.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

PERIOD_MAP = {
    '1d': lambda: timedelta(days=1),
    '1m': lambda: relativedelta(months=1),
    '3m': lambda: relativedelta(months=3),
    '1y': lambda: relativedelta(years=1),
    '3y': lambda: relativedelta(years=3)
}

def build_search_query(base_keyword, params):
    # 기본 조건 생성
    end_date = datetime.now()
    period = params.get('period', '3m')
    
    if period in PERIOD_MAP:
        start_date = end_date - PERIOD_MAP[period]()
    else:  # 커스텀 기간
        start_date = params['custom_start']
        end_date = params['custom_end']

    # 키워드 처리
    keywords = [base_keyword, base_keyword.replace(" ", "")]
    if 'AND' in params:
        keywords += params['AND'].split(',')
    if 'OR' in params:
        keywords = [f"({'|'.join(params['OR'].split(','))})"]
    
    return {
        'keywords': keywords,
        'start_date': start_date,
        'end_date': end_date,
        'reject_words': params.get('reject', '').split(',')
    }