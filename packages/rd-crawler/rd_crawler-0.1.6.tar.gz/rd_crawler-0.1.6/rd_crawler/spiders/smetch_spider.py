import scrapy
import re
from ..items import RDProjectItem

class SmtechSpider(scrapy.Spider):
    name = 'smtech'
    allowed_domains = ['smtech.go.kr']
    start_urls = ['https://www.smtech.go.kr/front/ifg/no/notice02_list.do']
    
    # 최대 크롤링할 페이지 수
    max_pages = 5
    current_page = 1
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SmtechSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 설정에서 최대 페이지 수 가져오기
        spider.max_pages = crawler.settings.getint('MAX_PAGES', 5)
        spider.logger.info(f"스파이더 초기화: 최대 페이지 수 = {spider.max_pages}")
        return spider
    
    def parse(self, response):
        self.logger.info(f"페이지 {self.current_page} 파싱 시작")
        
        # 디버깅을 위해 HTML 저장
        with open(f'smtech_debug_page_{self.current_page}.html', 'wb') as f:
            f.write(response.body)
        
        # 정확한 테이블 선택
        notices_table = response.xpath('//table[@class="tbl_base tbl_type01"]')
        if not notices_table:
            self.logger.error("공고 테이블을 찾을 수 없습니다!")
            return
            
        # 테이블 내의 행 선택 (thead 다음의 tbody 내 tr)
        notices = notices_table.xpath('./tbody/tr')
        self.logger.info(f"페이지 {self.current_page}에서 {len(notices)}개의 공고를 찾았습니다.")
        
        if len(notices) == 0:
            self.logger.error("공고 목록이 비어있습니다. 테이블 구조가 변경되었을 수 있습니다.")
            
        # 테이블 헤더 확인 (디버깅용)
        headers = notices_table.xpath('./thead/tr/th/text()').getall()
        self.logger.info(f"테이블 헤더: {headers}")
        
        for i, notice in enumerate(notices):
            # No 추출
            notice_no = notice.xpath('./td[1]/text()').get()
            if notice_no:
                notice_no = notice_no.strip()
                self.logger.info(f"공고 #{i+1}, No: {notice_no}")
            
            # 사업명 추출 (2번째 td)
            business_name = notice.xpath('./td[2]/text()').get()
            if business_name:
                business_name = business_name.strip()
                self.logger.info(f"사업명: {business_name}")
            else:
                business_name = "사업명 없음"
                self.logger.warning(f"공고 #{i+1}의 사업명을 찾을 수 없습니다")
            
            # 제목 추출 (3번째 td의 a 태그)
            title_elem = notice.xpath('./td[3]/a')
            if not title_elem:
                self.logger.warning(f"공고 #{i+1}의 제목 요소를 찾을 수 없습니다")
                continue
                
            title = title_elem.xpath('./text()').get()
            if title:
                title = title.strip()
                self.logger.info(f"제목: {title}")
            else:
                title = "제목 없음"
                self.logger.warning(f"공고 #{i+1}의 제목을 찾을 수 없습니다")
            
            # 링크 추출 - href 속성
            href = title_elem.xpath('./@href').get()
            if href:
                if href.startswith('/'):
                    link = f"https://www.smtech.go.kr{href}"
                else:
                    link = href
                self.logger.info(f"href에서 링크 추출: {link}")
            else:
                link = "링크 추출 실패"
                self.logger.warning(f"공고 #{i+1}의 링크를 추출할 수 없습니다")
            
            # 접수기간 추출 (4번째 td)
            application_period = notice.xpath('./td[4]/text()').get()
            if application_period:
                application_period = application_period.strip()
                self.logger.info(f"접수기간: {application_period}")
            else:
                application_period = "접수기간 정보 없음"
                self.logger.warning(f"공고 #{i+1}의 접수기간을 찾을 수 없습니다")
            
            # 공고일 추출 (5번째 td)
            announcement_date = notice.xpath('./td[5]/text()').get()
            if announcement_date:
                announcement_date = announcement_date.strip()
                self.logger.info(f"공고일: {announcement_date}")
            else:
                announcement_date = "공고일 정보 없음"
                self.logger.warning(f"공고 #{i+1}의 공고일을 찾을 수 없습니다")
            
            # 상태 추출 (6번째 td)
            # 상태는 이미지로 표시되는 경우가 있어 이미지 alt 텍스트도 확인
            status_img = notice.xpath('./td[6]/img/@alt').get()
            if status_img:
                status = status_img
                self.logger.info(f"상태(이미지): {status}")
            else:
                status_text = notice.xpath('./td[6]/text()').get()
                if status_text:
                    status = status_text.strip()
                    self.logger.info(f"상태(텍스트): {status}")
                else:
                    status = "상태 정보 없음"
                    self.logger.warning(f"공고 #{i+1}의 상태를 찾을 수 없습니다")
            
            # 아이템 생성
            item = RDProjectItem()
            item['title'] = f"[{business_name}] {title}"
            item['date'] = f"접수기간: {application_period}, 공고일: {announcement_date}, 상태: {status}"
            item['organization'] = "중소기업기술정보진흥원(TIPA)"
            item['link'] = link
            item['source'] = 'smtech.go.kr'
            
            self.logger.info(f"아이템 생성 완료: {item['title']}")
            yield item
        
        # 다음 페이지 처리
        if self.current_page < self.max_pages:
            self.current_page += 1
            next_page_url = f"https://www.smtech.go.kr/front/ifg/no/notice02_list.do?page={self.current_page}"
            self.logger.info(f"다음 페이지로 이동: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)