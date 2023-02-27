# How to run local server
**최상위 폴더에서 실행**
```
./scripts/run_local.sh
```

# TODO
[] sqlAlchemy 보다 `SQLModel` 이 훨씬 schema 작성이 편한 듯 ... mig 고려
   - (multiple database alembic handling)[https://stackoverflow.com/questions/41109804/alembic-sqlalchemy-multiple-databases]
[] domain 별 `repository` 생성
   [] Base CRUD 적용 
[] `Black Formatter` 일괄 적용
[] `login` 로직 적용
[] `라이엇 API` 요청 - 적재 로직
   - 서버에 통합?
[] 서버에 **DB 다시 띄우기**
[] 프론트엔드 로컬에 띄우기 쉽게 `Docker`
[] `pip` -> `poetry`
   - `poetry` 안 깔린 사람들 많을 것 같아서 일단 패스
  
# Done
[x] DDD 폴더 구조 개편
[x] DB ORM DTO create
[x] User Basic repo 생성 (get, create)