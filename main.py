"""
ASAAC ESG Platform Main Execution Module
"""
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 모듈 임포트
from modules.auth.google_oauth import verify_google_token
from modules.crawler.news_crawler import UnifiedNewsCrawler
from modules.processing.advanced_dedupe import deduplicate_articles
# from modules.processing.sentiment import analyze_sentiment
# from modules.processing.esg_categorize import categorize_esg
# from modules.analysis.risk_scoring import calculate_risk_score
# from modules.analysis.report_generator import generate_esg_report

# 환경변수 로드
load_dotenv()

def calculate_period(period):
    """주어진 기간 문자열을 기준으로 시작일과 종료일 계산"""
    end_date = datetime.today()
    if period == '1d':
        start_date = end_date - timedelta(days=1)
    elif period == '1w':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1m':
        start_date = end_date - timedelta(days=30)
    elif period == '3m':
        start_date = end_date - timedelta(days=90)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    elif period == '3y':
        start_date = end_date - timedelta(days=3*365)
    else:
        raise ValueError("지원하지 않는 기간 형식입니다.")
    return start_date, end_date

def main():
    """사용자 시나리오 기반 메인 실행 흐름"""
    
    # # 0단계: 사용자 인증
    # try:
    #     user_token = input("Google 로그인 토큰 입력: ")
    #     user_info = verify_google_token(user_token)
    #     if not user_info:
    #         raise ValueError("잘못된 인증 토큰")
    #     print(f"\n✅ {user_info['email']}님 환영합니다")
    # except Exception as e:
    #     print(f"❌ 로그인 실패: {str(e)}")
    #     return

    # 1단계: 기업 검색 조건 생성
    company = input("\n🔍 분석할 기업명 입력 (예: OCI 홀딩스): ").strip()

    # 기본 검색 조건
    search_params = {
        'base_keyword': company,
        'period': '1d',  # 기본 1개개월
        'reject_words': [],
        'esg_standard': 'ecovadis'
    }

    # 기간 계산
    start_date, end_date = calculate_period(search_params['period'])
    search_params['start_date'] = start_date.strftime("%Y-%m-%d")
    search_params['end_date'] = end_date.strftime("%Y-%m-%d")

    
    # # 1-1단계: 세부 검색 조건 적용
    # advanced_search = input("\n세부 검색을 사용하시겠습니까? (y/n): ").lower()
    # if advanced_search == 'y':
    #     search_params.update(get_advanced_search_params())

    # 2단계: 크롤링 실행
    print(f"\n📰 {company} 관련 뉴스 수집 시작...")
    crawler = UnifiedNewsCrawler()
    raw_articles = crawler.fetch(search_params)
    print(f"- 수집된 원본 기사: {len(raw_articles)}건")

    # # 3단계: 중복 제거
    # print("\n🧹 중복 기사 제거 진행...")
    # unique_articles = deduplicate_articles(raw_articles)
    
    # # 4단계: 감성 분석
    # print("\n🧠 감성 분석 수행 중...")
    # for article in unique_articles:
    #     article['sentiment'] = analyze_sentiment(article['content'])
    
    # # 5단계: ESG 카테고리 분류
    # print("\n🏷️ ESG 카테고리 태깅 중...")
    # for article in unique_articles:
    #     article['esg_category'] = categorize_esg(article['content'])
    
    # # 6단계: 리스크 점수 계산
    # print("\�⚠️ 리스크 평가 진행...")
    # for article in unique_articles:
    #     article['risk_score'] = calculate_risk_score(article)
    
    # # 최종 리포트 생성
    # print("\n📊 종합 리포트 생성 중...")
    # report = generate_esg_report(unique_articles, search_params)
    
    # # 결과 출력
    # print("\n" + "="*50)
    # print(f"{company} ESG 분석 리포트".center(50))
    # print("="*50)
    # print_report(report)

def get_advanced_search_params():
    """세부 검색 파라미터 입력 UI"""
    params = {}
    
    # 기간 설정
    print("\n[세부 검색 설정]")
    print("1. 기간 선택 (1d/1m/3m/1y/3y/custom): ", end="")
    period = input().strip()
    if period == 'custom':
        params['custom_start'] = datetime.strptime(
            input("시작일(YYYY-MM-DD): "), "%Y-%m-%d")
        params['custom_end'] = datetime.strptime(
            input("종료일(YYYY-MM-DD): "), "%Y-%m-%d")
    else:
        params['period'] = period
    
    # 키워드 조건
    print("2. AND 조건 키워드 (쉼표 구분): ", end="")
    if and_keys := input().strip():
        params['AND'] = and_keys
    
    print("3. OR 조건 키워드 (쉼표 구분): ", end="")
    if or_keys := input().strip():
        params['OR'] = or_keys
    
    # 제외 키워드
    print("4. 제외할 키워드 (쉼표 구분): ", end="")
    if reject := input().strip():
        params['reject_words'] = reject.split(',')
    
    # ESG 기준
    print("5. ESG 기준 선택 (ecovadis/sasb/gri): ", end="")
    if standard := input().strip():
        params['esg_standard'] = standard
    
    return params

def print_report(report):
    """리포트 출력 핸들러"""
    print(f"\n📈 감성 분포")
    print(f"- 긍정: {report['sentiment_counts']['positive']}건")
    print(f"- 중립: {report['sentiment_counts']['neutral']}건")
    print(f"- 부정: {report['sentiment_counts']['negative']}건")
    
    print("\n🚨 상위 리스크 기사")
    for idx, article in enumerate(report['top_risks'][:5], 1):
        print(f"{idx}. [{article['risk_score']}/10] {article['title'][:30]}...")
    
    print("\n🌟 상위 긍정 기사")
    for idx, article in enumerate(report['top_positives'][:5], 1):
        print(f"{idx}. [{article['risk_score']}/10] {article['title'][:30]}...")
    
    print("\n📌 ESG 평가 결과")
    print(f"- 환경(E): {report['esg_scores']['environment']:.1f}/10")
    print(f"- 사회(S): {report['esg_scores']['social']:.1f}/10")
    print(f"- 지배구조(G): {report['esg_scores']['governance']:.1f}/10")
    
    print("\n🔍 개선 필요 분야")
    for weakness in report['improvement_points']:
        print(f"- {weakness}")

if __name__ == "__main__":
    main()