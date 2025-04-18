import scrapy
import re
from ..items import RDProjectItem

class KeitSpider(scrapy.Spider):
    name = 'keit'
    allowed_domains = ['srome.keit.re.kr']
    start_urls = ['https://srome.keit.re.kr/srome/biz/perform/opnnPrpsl/retrieveTaskAnncmListView.do?prgmId=XPG201040000&rcveStatus=A']
    
    # 최대 크롤링할 페이지 수
    max_pages = 5
    current_page = 1
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KeitSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 설정에서 최대 페이지 수 가져오기
        spider.max_pages = crawler.settings.getint('MAX_PAGES', 5)
        spider.logger.info(f"스파이더 초기화: 최대 페이지 수 = {spider.max_pages}")
        return spider
    
    def parse(self, response):
        self.logger.info(f"현재 처리 중인 페이지: {response.url}")
        
        # 페이지 내용 디버깅용으로 저장
        with open(f'keit_debug_page_{self.current_page}.html', 'wb') as f:
            f.write(response.body)
            
        # 공고 목록 추출 - 리스트 항목으로 표시된 공고들
        notices = response.css('ul.task_list li')
        self.logger.info(f"발견된 공고 목록 (ul.task_list li): {len(notices)}개")
        
        if len(notices) == 0:
            # 리스트 형태가 아닌 경우 다른 형태로 시도
            notices = response.css('.bbs_list tbody tr')
            self.logger.info(f"발견된 공고 목록 (.bbs_list tbody tr): {len(notices)}개")
        
        # 그래도 없으면 다른 선택자 시도
        if len(notices) == 0:
            notices = response.css('li:contains("신규지원"), li:contains("공고")')
            self.logger.info(f"발견된 공고 목록 (li:contains('신규지원')): {len(notices)}개")
        
        # 직접 제목 텍스트 추출 시도
        titles = response.xpath('//text()[contains(., "신규지원") and contains(., "공고")]').getall()
        self.logger.info(f"텍스트 검색으로 발견된 제목: {len(titles)}개")
        
        # 제목 텍스트를 직접 찾아 아이템 생성
        if titles:
            for title_text in titles:
                title = title_text.strip()
                if len(title) > 10:  # 짧은 텍스트는 제외
                    self.logger.info(f"발견한 제목: {title}")
                    
                    # 아이템 생성
                    item = RDProjectItem()
                    item['title'] = title
                    item['date'] = "접수기간 정보 확인 필요"  # 상세 페이지에서 확인 필요
                    item['organization'] = "KEIT(한국산업기술평가관리원)"
                    item['link'] = response.url  # 기본 URL
                    item['source'] = 'srome.keit.re.kr'
                    
                    yield item
        
        # 공고 리스트에서 정보 추출
        for i, notice in enumerate(notices):
            # 제목 추출 시도
            title = None
            
            # 1. 직접 텍스트 추출 시도
            title_text = notice.css('::text').get()
            if title_text and len(title_text.strip()) > 10:
                title = title_text.strip()
            
            # 2. 특정 요소에서 추출 시도
            if not title:
                title_selectors = [
                    'a::text', 
                    'strong::text',
                    'p::text',
                    'span::text',
                    'td:nth-child(2)::text'
                ]
                
                for selector in title_selectors:
                    title_text = notice.css(selector).get()
                    if title_text and len(title_text.strip()) > 10:
                        title = title_text.strip()
                        break
            
            if not title:
                continue
                
            self.logger.info(f"발견한 공고 제목 {i+1}: {title}")
            
            # 링크 추출 시도
            link = notice.css('a::attr(href)').get()
            if link:
                if not link.startswith('http'):
                    if link.startswith('/'):
                        link = f"https://srome.keit.re.kr{link}"
                    else:
                        link = f"https://srome.keit.re.kr/{link}"
            else:
                link = response.url  # 링크가 없으면 현재 페이지 URL 사용
            
            # 아이템 생성
            item = RDProjectItem()
            item['title'] = title
            item['date'] = "접수기간 정보 확인 필요"  # 상세 페이지에서 확인해야 할 수 있음
            item['organization'] = "KEIT(한국산업기술평가관리원)"
            item['link'] = link
            item['source'] = 'srome.keit.re.kr'
            
            yield item
            
        # 다음 페이지 처리 - 페이지가 여러 개인 경우
        if self.current_page < self.max_pages:
            next_page_link = response.css('a.next::attr(href), a:contains("다음")::attr(href)').get()
            
            if next_page_link:
                self.current_page += 1
                self.logger.info(f"다음 페이지로 이동: {next_page_link}")
                yield response.follow(next_page_link, callback=self.parse)
            else:
                # 다음 페이지 링크가 없으면 직접 URL 구성
                self.current_page += 1
                next_page_url = f"{response.url}&pageIndex={self.current_page}"
                self.logger.info(f"직접 구성한 다음 페이지 URL: {next_page_url}")
                yield scrapy.Request(next_page_url, callback=self.parse)