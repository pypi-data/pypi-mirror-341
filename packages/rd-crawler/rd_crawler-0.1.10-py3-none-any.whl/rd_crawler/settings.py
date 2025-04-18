BOT_NAME = 'rd_crawler'

SPIDER_MODULES = ['rd_crawler.spiders']
NEWSPIDER_MODULE = 'rd_crawler.spiders'

# 사용자 에이전트 설정
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# 동시 요청 제한
CONCURRENT_REQUESTS = 1

# 다운로드 딜레이 설정 (초)
DOWNLOAD_DELAY = 2

# 파이프라인 설정
ITEM_PIPELINES = {
    'rd_crawler.pipelines.ExcelPipeline': 300,
}

# 쿠키 비활성화
COOKIES_ENABLED = False

# 재시도 활성화
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 로깅 설정
LOG_LEVEL = 'INFO'