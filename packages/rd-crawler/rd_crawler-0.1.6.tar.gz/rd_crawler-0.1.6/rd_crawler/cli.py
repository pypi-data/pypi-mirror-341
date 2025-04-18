#!/usr/bin/env python
"""
중소기업 R&D 사업공고 크롤러 CLI
"""
import os
import sys
import argparse
import pkg_resources
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
import shutil

# 스파이더 직접 임포트
try:
    from rd_crawler.spiders.bizinfo_spider import BizinfoSpider
    from rd_crawler.spiders.keit_spider import KeitSpider
    from rd_crawler.spiders.smetch_spider import SmtechSpider
except ImportError:
    try:
        # 상대 경로로 시도
        from .spiders.bizinfo_spider import BizinfoSpider
        from .spiders.keit_spider import KeitSpider
        from .spiders.smetch_spider import SmtechSpider
    except ImportError:
        pass  # 로깅은 아래에서 처리

def create_parser():
    """명령줄 인자 파서 생성"""
    parser = argparse.ArgumentParser(
        description='중소기업 R&D 사업정보 수집 크롤러'
    )
    
    parser.add_argument(
        '-s', '--spider',
        choices=['all', 'bizinfo', 'keit', 'smtech'],
        default='all',
        help='실행할 스파이더 이름 (기본값: all - 모든 스파이더 실행)'
    )
    
    parser.add_argument(
        '-p', '--pages',
        type=int,
        default=5,
        help='각 스파이더가 크롤링할 최대 페이지 수 (기본값: 5)'
    )
    
    parser.add_argument(
        '-k', '--keywords',
        type=str,
        default=None,
        help='사용할 키워드 파일 경로 (기본값: 패키지에 포함된 keywords.txt)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='상세 로그 출력'
    )
    
    return parser

def setup_logging(verbose=False):
    """로깅 설정"""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s [%(levelname)s] %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
    )
    
    return logging.getLogger(__name__)

def get_default_keywords_path():
    """패키지에 포함된 기본 키워드 파일 경로 반환"""
    possible_paths = [
        # 1. 현재 작업 디렉토리 (우선순위 높음)
        os.path.join(os.getcwd(), 'keywords.txt'),
    ]
    
    # 패키지 내부 파일 조회 (안전하게 예외 처리)
    try:
        package_path = pkg_resources.resource_filename('rd_crawler', 'keywords.txt')
        if package_path:
            possible_paths.append(package_path)
    except (pkg_resources.DistributionNotFound, TypeError, ValueError, AttributeError):
        logger = logging.getLogger(__name__)
        logger.debug("패키지 내부에서 keywords.txt를 찾을 수 없습니다")
    
    # 추가 검색 경로
    try:
        # 모듈 디렉토리 경로 (모듈의 __file__ 속성이 있는 경우)
        import rd_crawler
        if hasattr(rd_crawler, '__file__') and rd_crawler.__file__:
            module_dir = os.path.dirname(rd_crawler.__file__)
            possible_paths.append(os.path.join(module_dir, 'keywords.txt'))
    except (ImportError, TypeError, AttributeError):
        pass
        
    # 현재 파일의 상대 경로 기반 검색
    try:
        current_dir = os.path.dirname(__file__)
        possible_paths.append(os.path.join(current_dir, 'keywords.txt'))
        possible_paths.append(os.path.join(os.path.dirname(current_dir), 'keywords.txt'))
    except (NameError, TypeError):
        pass
    
    # 가능한 모든 경로에서 파일 검색
    for path in possible_paths:
        if path and os.path.exists(path):
            return path
    
    # 키워드 파일을 찾지 못한 경우 로그로 경로 출력
    logging.error("keywords.txt 파일을 찾을 수 없습니다. 다음 위치를 확인했습니다:")
    for path in possible_paths:
        if path:
            logging.error(f"- {path}")
    
    return None

def main():
    """메인 함수"""
    parser = create_parser()
    args = parser.parse_args()
    
    logger = setup_logging(args.verbose)
    logger.info("크롤링 시작")
    
    # 키워드 파일 처리
    keywords_file_path = os.path.join(os.getcwd(), 'keywords.txt')
    
    if args.keywords:
        # 사용자가 지정한 키워드 파일 사용
        if not os.path.exists(args.keywords):
            logger.error(f"키워드 파일을 찾을 수 없습니다: {args.keywords}")
            return 1
        source_keywords = args.keywords
    else:
        # 패키지 내부의 기본 키워드 파일 사용
        default_keywords = get_default_keywords_path()
        if default_keywords and os.path.exists(default_keywords):
            source_keywords = default_keywords
            logger.info(f"기본 키워드 파일을 사용합니다: {default_keywords}")
        else:
            logger.error("keywords.txt 파일을 찾을 수 없습니다.")
            logger.error("현재 디렉토리 또는 패키지에 keywords.txt 파일을 배치하세요.")
            return 1
    
    # 키워드 파일 복사가 필요한 경우만 실행
    if os.path.abspath(source_keywords) != os.path.abspath(keywords_file_path):
        try:
            # 기존 파일이 있으면 백업 생성
            if os.path.exists(keywords_file_path):
                backup_name = f"keywords.txt.bak_{os.urandom(4).hex()}"
                os.rename(keywords_file_path, backup_name)
                logger.info(f"기존 키워드 파일 백업: {backup_name}")
            
            # 새 키워드 파일 복사
            shutil.copy2(source_keywords, keywords_file_path)
            logger.info(f"키워드 파일 설정: {source_keywords} -> {keywords_file_path}")
        except Exception as e:
            logger.error(f"키워드 파일 설정 중 오류: {e}")
            return 1
    else:
        logger.info(f"현재 디렉토리의 keywords.txt 파일을 사용합니다: {keywords_file_path}")
    
    # Scrapy 설정 로드
    settings = get_project_settings()
    
    # 최대 페이지 수 설정
    if args.pages > 0:
        settings.set('MAX_PAGES', args.pages)
    
    # 크롤러 프로세스 생성
    process = CrawlerProcess(settings)
    
    # 스파이더 클래스 가져오기 - 임포트 오류 처리
    spider_loaded = {
        'bizinfo': 'BizinfoSpider' in globals(),
        'keit': 'KeitSpider' in globals(),
        'smtech': 'SmtechSpider' in globals()
    }
    
    # 스파이더 실행
    if args.spider in ['all', 'bizinfo']:
        logger.info("Bizinfo 스파이더 등록")
        if spider_loaded['bizinfo']:
            process.crawl(BizinfoSpider)
        else:
            try:
                # 이름으로 등록 시도
                process.crawl('bizinfo')
                logger.info("이름으로 Bizinfo 스파이더 등록 성공")
            except KeyError:
                logger.error("Bizinfo 스파이더를 로드할 수 없습니다")
    
    if args.spider in ['all', 'keit']:
        logger.info("KEIT 스파이더 등록")
        if spider_loaded['keit']:
            process.crawl(KeitSpider)
        else:
            try:
                process.crawl('keit')
                logger.info("이름으로 KEIT 스파이더 등록 성공")
            except KeyError:
                logger.error("KEIT 스파이더를 로드할 수 없습니다")
    
    if args.spider in ['all', 'smtech']:
        logger.info("SMTECH 스파이더 등록")
        if spider_loaded['smtech']:
            process.crawl(SmtechSpider)
        else:
            try:
                process.crawl('smtech')
                logger.info("이름으로 SMTECH 스파이더 등록 성공")
            except KeyError:
                logger.error("SMTECH 스파이더를 로드할 수 없습니다")
    
    # 크롤러 시작
    logger.info("크롤링 시작...")
    process.start()
    logger.info("크롤링 완료!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())