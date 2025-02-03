SENTIMENT_PROMPT = """다음 뉴스 내용의 감성을 분석해주세요. 반드시 다음 형식으로 응답:
{
    "sentiment": "positive|neutral|negative",
    "reason": "한국어 이유 설명"
}
내용: {content}"""

ESG_CATEGORY_PROMPT = """다음 내용을 Ecovadis ESG 기준에 따라 분류:
[가능한 분류] Environment, Social, Governance, N/A
응답 형식: 
{
    "category": "분류결과",
    "keywords": ["관련키워드1", "관련키워드2"]
}
내용: {content}"""