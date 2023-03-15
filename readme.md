# How to run local server
**최상위 폴더에서 실행**
```
./scripts/run_local.sh
```

# TODO
[] school 지역 column 추가
1. MATCH HISTORIES 의 통계 내기
[] SQLModel async 적용
[] `Black Formatter` 일괄 적용
[] `login` 로직 적용
[] `라이엇 API` 요청 - 적재 로직
   - 서버에 통합?
[] 프론트엔드 로컬에 띄우기 쉽게 `Docker`
  
## 2023/03/15
[x] COMMON data 적재
[x] pure sql 실행 함수
[x] MOST_LINE, CHAMP_SUMMARIES TABLE 생성
[x] runes id 업데이트
[x] MOST_LINE, CHAMP SUMMARIES 통계 내기
   1. MATCH_HiSTORIES 통계 내기
   2. CURRENT_SEASON_SUMMARIES 삽입
   3. MOST_LINE, CHAMP 에 삽입
---
[] match history 받아오는 로직 바로 잡기 (천천히...)
[] create_user 시, `last_update_at` column 업데이트 로직 단도리하기
[] **router 작성 요령**
   - 전체적인 구조를 설명해놓기
     - 치훈이가 공부하려고 했는데, 어디부터가 시작인지를 모름
   - DB 쿼리 날리는 법 등...
[] **프론트가 쓸 수 있게 이쁜 라우트를 만들어보자**

# Done
[x] sqlAlchemy 보다 `SQLModel` 이 훨씬 schema 작성이 편한 듯 ... mig 고려
   - (multiple database alembic handling)[https://stackoverflow.com/questions/41109804/alembic-sqlalchemy-multiple-databases]
[x] alembic 적용
[x] domain 별 `crud` 생성
   [x] Base CRUD 적용 
[x] 서버에 **DB 다시 띄우기**
[x] `pip` -> `poetry`
   - `poetry` 안 깔린 사람들 많을 것 같아서 일단 패스
[x] DDD 폴더 구조 개편
[x] DB ORM DTO create
[x] User Basic repo 생성 (get, create)