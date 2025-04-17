# 중소기업 R&D 사업 정보 크롤러

이 프로젝트는 다음 세 개의 웹사이트에서 중소기업 R&D 사업 정보를 크롤링하고 특정 키워드로 필터링하는 도구입니다:
- www.bizinfo.go.kr
- srome.keit.re.kr
- www.smtech.go.kr

## 설치 방법

### 일반 설치
```bash
# pip를 이용한 설치
pip install -r requirements.txt
```

### UV를 이용한 설치
```bash
# UV를 이용한 설치 (로컬 패키지)
uv pip install .

# 또는 개발 모드로 설치
uv pip install -e .

# 배포 버전 설치 (배포 후)
uv pip install rd_crawler
```

## 사용 방법

이 크롤러는 명령줄 인터페이스를 통해 실행할 수 있습니다:

```bash
# 모든 사이트 크롤링
rd-crawler --spider all --pages 5

# 특정 사이트만 크롤링
rd-crawler --spider bizinfo --pages 3

# 키워드 파일 지정
rd-crawler --spider all --keywords custom_keywords.txt

# 상세 로그 출력
rd-crawler --verbose
```

## 키워드 파일 형식

키워드 파일은 각 줄에 하나의 키워드가 있는 텍스트 파일입니다:

```
인공지능
AI
로봇
기계장비
생산기술
지역특화
생산장비
```

## 결과물

크롤링 결과는 날짜 기반으로 생성된 엑셀 파일에 저장됩니다:
- 파일명 형식: 중소기업_RD_사업정보_YYYYMMDD.xlsx
