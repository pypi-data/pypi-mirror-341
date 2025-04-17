import pandas as pd
from datetime import datetime
import os
import re

class ExcelPipeline:
    def __init__(self):
        self.items = []
        self.keywords = []
        self.all_items = []  # 모든 항목 저장(필터링 전)
        self.keyword_matches = {}  # 각 키워드별 매칭 결과 저장
        
        # 키워드 파일 읽기
        try:
            with open('keywords.txt', 'r', encoding='utf-8') as f:
                self.keywords = [line.strip() for line in f if line.strip()]
                print(f"키워드 로드 성공: {self.keywords}")
                # 키워드별 매칭 카운터 초기화
                for keyword in self.keywords:
                    self.keyword_matches[keyword] = 0
        except Exception as e:
            print(f"키워드 파일 읽기 실패: {e}")
            # 기본 키워드 설정
            self.keywords = ["인공지능", "AI", "머신러닝", "빅데이터", "IoT", "스마트팩토리"]
            print(f"기본 키워드 설정: {self.keywords}")
            for keyword in self.keywords:
                self.keyword_matches[keyword] = 0
    
    def check_keyword_match(self, text):
        """키워드 매칭 확인 - 매칭된 키워드 목록 반환"""
        if not text:
            return [], False
        
        # 대소문자 구분 없이 매칭
        text_lower = text.lower()
        found = False
        matched_keywords = []
        
        for keyword in self.keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in text_lower:
                print(f"키워드 매칭 성공: '{keyword}' in '{text}'")
                self.keyword_matches[keyword] += 1
                matched_keywords.append(keyword)
                found = True
        
        return matched_keywords, found
    
    def process_item(self, item, spider):
        # 모든 항목 저장
        item_dict = dict(item)
        self.all_items.append(item_dict)
        
        # 키워드 필터링 - 제목 전체에서 검색 (사업명 포함)
        matched_keywords, is_matched = self.check_keyword_match(item_dict['title'])
        
        if is_matched:
            # 매치된 키워드 정보 추가
            item_dict['matched_keywords'] = ', '.join(matched_keywords)
            print(f"필터링 통과: {item_dict['title']} (키워드: {item_dict['matched_keywords']})")
            self.items.append(item_dict)
        else:
            item_dict['matched_keywords'] = ''
            print(f"필터링 제외: {item_dict['title']}")
        
        return item
    
    def close_spider(self, spider):
        print(f"스파이더 종료: 총 {len(self.all_items)}개 항목 중 {len(self.items)}개 필터링됨")
        
        # 키워드 매칭 결과 출력
        print("키워드별 매칭 결과:")
        for keyword, count in self.keyword_matches.items():
            print(f"- '{keyword}': {count}개 항목 매칭됨")
        
        # 키워드 필터링 결과 확인
        if not self.items and self.all_items:
            print("키워드와 일치하는 공고가 없어 모든 항목을 저장합니다.")
            # 모든 항목에 빈 매치 키워드 추가
            for item in self.all_items:
                if 'matched_keywords' not in item:
                    item['matched_keywords'] = '(전체 항목)'
            self.items = self.all_items
            
        # 그래도 결과가 없으면 종료
        if not self.items:
            print("크롤링된 항목이 없습니다.")
            return
            
        # 엑셀 파일 저장
        today = datetime.now().strftime('%Y%m%d')
        filename = f"중소기업_RD_사업정보_{today}.xlsx"
        
        # 파일이 이미 존재하는지 확인
        if os.path.exists(filename):
            # 기존 파일에 데이터 추가
            try:
                # 기존 엑셀 파일 읽기
                existing_df = pd.read_excel(filename)
                print(f"기존 파일 '{filename}' 읽기 성공: {len(existing_df)}개 항목 포함")
                
                # 기존 파일에 matched_keywords 컬럼이 없으면 추가
                if 'matched_keywords' not in existing_df.columns:
                    existing_df['matched_keywords'] = '(기존 항목)'
                
                # 새 데이터 프레임 생성
                new_df = pd.DataFrame(self.items)
                
                # 중복 데이터 제거를 위해 title과 source를 기준으로 병합
                combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['title', 'source'], keep='first')
                
                # 파일 저장
                combined_df.to_excel(filename, index=False, engine='openpyxl')
                print(f"{filename} 파일에 데이터가 추가되었습니다. 총 {len(combined_df)}개의 프로젝트가 저장되었습니다.")
                print(f"이번에 추가된 프로젝트: {len(self.items)}개, 중복 제외 최종 추가: {len(combined_df) - len(existing_df)}개")
                
            except Exception as e:
                print(f"기존 파일에 데이터 추가 중 오류 발생: {e}")
                # 오류 발생 시 새 파일로 저장
                df = pd.DataFrame(self.items)
                backup_filename = f"{filename}.{datetime.now().strftime('%H%M%S')}.new"
                df.to_excel(backup_filename, index=False, engine='openpyxl')
                print(f"오류로 인해 {backup_filename} 파일로 저장되었습니다. 총 {len(self.items)}개의 프로젝트가 저장되었습니다.")
        else:
            # 새 파일 생성
            df = pd.DataFrame(self.items)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"{filename} 파일이 새로 생성되었습니다. 총 {len(self.items)}개의 프로젝트가 저장되었습니다.")