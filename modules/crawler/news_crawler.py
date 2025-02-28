# modules/crawler/news_crawler.py
import requests
import logging
from datetime import datetime, timedelta
import time
from config import settings
from bs4 import BeautifulSoup

class UnifiedNewsCrawler:
    def __init__(self):
        self.sources = {
            'google': self._fetch_google,
            'naver': self._fetch_naver,
            'daum': self._fetch_daum
        }

    def fetch(self, query, sources=['naver', 'google', 'daum']):
        all_articles = []
        for source in sources:
            try:
                articles = self.sources[source](query)
                all_articles.extend(articles)
            except Exception as e:
                print(f"{source} 크롤링 실패: {str(e)}")
        return all_articles

    def convert_relative_date(self, relative_date):
        if "일 전" in relative_date:
            days_ago = int(relative_date.split("일 전")[0].strip())
            return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        elif "시간 전" in relative_date:
            hours_ago = int(relative_date.split("시간 전")[0].strip())
            return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d')
        # 필요하다면 분, 주 등 추가 처리
        return datetime.now().strftime('%Y-%m-%d')

    def _fetch_naver(self, query):
        # 네이버 검색을 통한 크롤링
        print(query)
        # 네이버 크롤링 코드
        all_news_list = []  # 전체 결과를 저장할 리스트
        news_list = []  # 모든 매체의 결과를 저장할 리스트
        page = 1  # 각 매체에 대해 페이지를 1로 초기화
        print(query['base_keyword'])
        while True:
        # 매체별 URL 생성
            url = (f"https://search.naver.com/search.naver?where=news&query={query['base_keyword']}"
                f"&sm=tab_pge&sort=0&photo=0&field=1&pd=3&ds={query['start_date']}&de={query['end_date']}"
                f"&docid=&related=0&mynews=1&office_type=2&office_section_code=8"
                f"&nso=so:r,p:from{query['start_date'].replace('.', '')}to{query['end_date'].replace('.', '')}"
                f"&start={page}")

            response = requests.get(url)

            if response.status_code != 200:
                logging.error(f"Failed to fetch URL")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".news_wrap")

            if not items:
                logging.info(f"No more news articles found for media")
                break

            for item in items:
                title = item.select_one(".news_tit").text
                link = item.select_one(".news_tit")["href"]
                summary = item.select_one(".news_dsc").text if item.select_one(".news_dsc") else "No summary"
                date_element = item.select_one(".info_group .info")
                date = self.convert_relative_date(date_element.text.strip()) if date_element else "날짜 없음"
                media_name = item.select_one(".info_group .press").text.strip()

                news_list.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "date": date,
                    "media_name": media_name
                })
            print(item)
            # 다음 페이지로 넘어가기
            page += 10
            time.sleep(0.5)  # 서버 과부하 방지를 위해 잠시 대기

        # 매체별 결과를 전체 리스트에 추가
        all_news_list.extend(news_list)
        
        print(all_news_list)


        # all_news.extend(news_list)
        # fetched_news_dict[section] = all_news
        # print(fetched_news_dict)
        # print(type(fetched_news_dict))
            
        # return fetched_news_dict

    def _fetch_google(self, query):
        # Google News RSS 구현
        pass
    
    def _fetch_daum(self, query):
        # Daum Open API 구현
        pass

