DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

NEWS_SOURCES = {
    'google': {'endpoint': 'https://news.google.com/rss'},
    'naver': {'endpoint': 'https://openapi.naver.com/v1/search/news.json'},
    'daum': {'endpoint': 'https://dapi.kakao.com/v2/search/web'}
}

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
}