# 2023-02-15 
[] DB schema 구분해서 table dto 생성하기
   - (공식문서)[https://docs.sqlalchemy.org/en/20/changelog/migration_11.html#multi-tenancy-schema-translation-for-table-objects]
# 2022-07-02 토

## 한 일

1. fastapi 생성
2. friends dummy data api 생성해서 프론트에서 데이터 확인
3. 프론트에서 recoil 사용해서 api 로 받아온 데이터 상태 관리
4. rdb 테이블 스키마 작성 및 테이블 생성
5. mysql 연결 / insert select delete 구조 확립

## TODO

1. mongodb connection 할 때, window 버전 문제 / ssl 문제 해결
2. 백엔드 배포하기
3. 프론트에서 데이터 들어가나 확인하기
4. pydantic 모델 만들기
5. 프론트에서 필요한 데이터에 적합하게 쿼리문 작성
6. 폴더 구조를 세분화하기 (query 폴더 /)

# 2022-07-23 토

## 한 일

0. 카카오 developer에 loling 등록
1. 카카오 로그인 인가 코드, 토큰 받기 완료
2. 웹뷰 -> 웹으로 로그인 화면 구현 예정

## 할 일

1. 사용자 정보 가져오기 기능
2. 디비 사용자 정보 저장 방식 고민
3. 사용자 정보 조회/작성 query 작성
4. 프론트엔드 웹뷰 코딩
   https://hazel-developer.tistory.com/84

# 2022-07-24 일

## 한 일

1. 토큰으로 카카오에서 사용자 id 불러오기
2. 디비에 kakao_id 컬럼 추가
3. 사용자 정보 조회/작성 query 작성 중

## issue

1. USER 테이블 pk 고민 (kakao_id)
2. 웹뷰

# 2022-08-07

## 한 일

백엔드 구조 개편

## ISSUE

3. 라우트를 기능별로 나눠야 할듯/ USER처럼 이름이 애매모호한 경우 어떤 기능까지 포함시킬지 정해야함
4. encryption도 따로 calss를 두면 좋을듯
5. 모든 router에서 model 지정하기
