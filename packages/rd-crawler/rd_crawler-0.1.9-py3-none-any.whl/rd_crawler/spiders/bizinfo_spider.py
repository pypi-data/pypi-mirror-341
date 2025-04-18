import scrapy
import logging
from ..items import RDProjectItem

class BizinfoSpider(scrapy.Spider):
    name = 'bizinfo'
    allowed_domains = ['bizinfo.go.kr']
    start_urls = ['https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do']
    
    # 최대 크롤링할 페이지 수
    max_pages = 5
    current_page = 1
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BizinfoSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 설정에서 최대 페이지 수 가져오기
        spider.max_pages = crawler.settings.getint('MAX_PAGES', 5)
        spider.logger.info(f"스파이더 초기화: 최대 페이지 수 = {spider.max_pages}")
        return spider
    
    def parse(self, response):
        self.logger.info(f"현재 처리 중인 페이지: {response.url}")
        
        # 페이지 내용 디버깅용으로 저장
        with open(f'bizinfo_debug_page_{self.current_page}.html', 'wb') as f:
            f.write(response.body)
        
        # 공고 목록 추출 (테이블 구조로 수정)
        notices = response.css('div.table_Type_1 table tbody tr')
        self.logger.info(f"Found {len(notices)} notices on page {self.current_page}")
        
        for notice in notices:
            # 공고번호 행은 건너뛰기
            if notice.css('th'):
                continue
                
            # 지원사업명 추출
            title_elem = notice.css('td.txt_l a')
            if not title_elem:
                continue
                
            title = title_elem.css('::text').get().strip()
            link = "https://www.bizinfo.go.kr" + title_elem.css('::attr(href)').get('')
            
            # 신청기간 정보 추출
            date_info = notice.css('td:nth-child(4)::text').get()
            date = date_info.strip() if date_info else "날짜 정보 없음"
            
            # 소관부처 정보 추출
            org_info = notice.css('td:nth-child(5)::text').get()
            organization = org_info.strip() if org_info else "기관 정보 없음"
            
            # 아이템 생성
            item = RDProjectItem()
            item['title'] = title
            item['date'] = date
            item['organization'] = organization
            item['link'] = link
            item['source'] = 'bizinfo.go.kr'
            
            yield item
        
        # 다음 페이지 처리 - 수정된 방식
        if self.current_page < self.max_pages:
            self.current_page += 1
            
            # 페이지 번호 링크 찾기
            page_links = response.css('div.paging a')
            next_page_url = None
            
            # 페이지 번호 링크 확인
            for link in page_links:
                page_text = link.css('::text').get().strip()
                if page_text == str(self.current_page):
                    next_page_url = link.css('::attr(href)').get()
                    break
            
            # 페이지 번호를 찾지 못하면 '다음' 링크 확인
            if not next_page_url:
                next_link = response.css('div.paging a:contains("다음")::attr(href)').get()
                if next_link:
                    next_page_url = next_link
            
            # URL이 상대 경로인 경우 전체 URL로 변환
            if next_page_url and not next_page_url.startswith('http'):
                if next_page_url.startswith('/'):
                    next_page_url = f"https://www.bizinfo.go.kr{next_page_url}"
                else:
                    next_page_url = f"https://www.bizinfo.go.kr/{next_page_url}"
            
            # URL이 있으면 요청 생성
            if next_page_url:
                self.logger.info(f"다음 페이지로 이동: {next_page_url}")
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse,
                    dont_filter=True
                )
            else:
                # 직접 URL 파라미터 구성
                next_page_url = f"https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?cpage={self.current_page}"
                self.logger.info(f"직접 구성한 다음 페이지 URL: {next_page_url}")
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse,
                    dont_filter=True
                )