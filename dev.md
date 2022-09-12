# 06-27
1. .env 설정
2. rds 구현
3. 프론트에서 받는 거 확인 (python dict - js obj json 으로 교환)

# 09-04
## 변경 전
1. 로그인(프론트) -> (아이디, 비밀번호) 백엔드로 전송
2. 토큰 {signin_id, 하나의 lol_name} 발행 후 프론트에 return
3. 프론트에서 recoil state 에 저장

*문제점*
   1. recoil state 에 token 을 두어서 component 밖에서 hook call 을 할 수 없었음. api 요청 시 불러오기 불가능 / 번잡
   2. 프론트에서 로그인 후 백엔드에 요청 시, 로그인 한 유저의 lol_name 을 알 수 없었음.

## 변경 후
1. 로그인(프론트) -> (아이디, 비밀번호) 백엔드로 전송
2. 토큰 {signin_id, 하나의 lol_name} 발행 후 프론트에 return
3. 프론트에서 **AsyncStorage** (Web 의 Local Storage 와 동일) 에 저장함

4. 프론트에서 백엔드에 api 요청 시, 항상, 자동으로 header 에 token 을 탑재시켜 보냄. 
   4-1. **AsyncStorage** 에 토큰이 있는지 없는지 여부도 판별 가능하기 때문에, 후에 접근성 관련하여 발전 가능

```js
/* axios interceptors - request */
axiosInstance.interceptors.request.use(
  async (request) => {
    /* 로컬 스토리지에 저장한 토큰 가져오기 */

    const authToken = await AsyncStorage.getItem('token');
    // 저장된 token이 있으면 불러와서 request에 Authorization token 첨부
    if (authToken) request.headers.Authorization = `Bearer ${authToken}`
    return request

  },
    (error) => Promise.reject(error)
  ,
)
```

5. 백엔드에서 header 에 있는 token 을 받아, decoding 시킬 수 있게 만듦.

```py
def auth_required(Authorization: str = Header(None, title="JWT")) -> dict:
    try:
        if not Authorization:
            raise Exception

        token = Authorization[7:]
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)

        return decoded_token

    except (IndexError, jwt.PyJWTError):
        raise Exception
```

위의 코드를 아래와 같이, **Depends** 를 활용하여 사용할 수 있음.

```py
@router.get("")
def route_get_profile(user_info: dict = Depends(auth_required)):
    lol_name = user_info.get("lol_name")
    return get_profile(lol_name=lol_name)
```

## 고쳐야 할 점
1. **AsyncStorage** 가 곧 deprecated 됨. 

`'@react-native-async-storage/async-storage' instead of 'react-native'. See https://github.com/react-native-async-storage/async-storage`

로 수정 해야 함.

2. **지금은 `/profile` 만 테스트로 진행해 보았음. 나머지 lol_name 이 하드코딩 되어있는 것들 도 현재 형태로 바꾸어야 함.**
   2-1. 프론트의 더미데이터에 필요한 정보 자체는 똑같이 맞추었으나, 프론트의 데이터 양식과 백엔드에서 실제로 보내주는 양식에 차이가 있음. 
       이를 맞추면서 바꿔야 함. 

## 추가적으로 해야할 일
1. **lol_account 솔랭 자랭 tier 나누기**
~~2. 자랭 솔랭 정보 mart table 생성해서 넣어두기 (라인, 챔피언 정보들 넣기)~~
3. **FACT 쿼리 어디서 돌릴지 정하기**
   1. ods 에서 fact 돌린건지 아닌지 `fact_yn` 인자 추가하기 
   -> 쿼리문도 수정해야함
   - fact 돌린 후 ods 의 `fact_yn` 'Y' 로 바꾸는 update 문 추가하기
   - fact 돌릴 때, `fact_yn` 이 'N' 인 것만 insert 하기
4. **정보 갱신 로직 설정하기**
   1. `match_id` 들 받아오기
   2. `match_id` 에 대한 매치 정보 받기 (ODS)
   3. ODS 정보 바탕으로 각 게임 참여자 정보 뽑기 (FACT)
   4. 3 번 정보를 바탕으로, 각 유저별 - 라인 kda, 승률 - 챔피언 kda, 승률 뽑기 (MART)
   -> 어디서, 언제, 어떻게 (자동 갱신 - 수동 갱신 로직) 할지 정해야 함.
5. 회원가입 시 라이엇 아이디 비밀번호 인증 로직 추가하기 (아이콘으로 할 것인지, selenium 활용한 로직으로 할 것인지)
6. user info api 요청 했을 때, 랭크별로, 아무 게임도 안돌린 사람은 빈값으로 나옴 -> 예외 처리 필요
7. DB timezone 한국시간으로
8. api 에서 주는 line 이 none 인 경우
9.  매칭 할 때 돌릴 수 있는 티어 구분해서 주기 
10. 백엔드 라우트, 쿼리 주석달기
11. DB 컬럼네임 대문자로 바꾸고 백엔드도 수정하기
12. db connection 더늦기전에 인자 빼기

## 내가 생각하기에 다음 주에 해야할 일
1. token 활용한 프론트 - 백 왔다갔다 하는 로직 구현했으니, 지금 사용하고 있는 api 모두 이런 형식으로 바꾸기
   1. 데이터 형식도 맞춰야 해서 프론트 - 백 하는 사람 같이 붙어서 해보기
2. 채팅 DB + 백엔드 구상
3. FAQ / 공지사항 DB + 백엔드


# 09-12 김민규
## 문제점
1. profile 가져올 때, 총 3번의 트랜잭션이 필요함.
2. 친구가 많아지면 각 친구의 profile 가져올 때, 친구 수 * 3 의 트랜잭션이 일어나므로 서버 다운 가능
3. LOL_ACCOUNT TABLE 에 축약해둔 정보를 모두 넣어둬서, LOL_ACCOUNT TABLE 자체가 PROFILE 이 될 수 있게끔 하자. (C)
4. 아래와 같은 형태의 `JSON` 이 테이블에 들어가서, PROFILE 가져오는 것을 하나의 SELECT 로 할 수 있게끔 하자 
  [
   {
      "CHAMP_KDA":9.1111,
      "CHAMP_NAME":"Katarina",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":18,
      "CHAMP_WIN_RATE":0.4444
   },
   {
      "CHAMP_KDA":9.6667,
      "CHAMP_NAME":"Kayn",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":3,
      "CHAMP_WIN_RATE":0.3333
   },
   {
      "CHAMP_KDA":15.6667,
      "CHAMP_NAME":"Zed",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":3,
      "CHAMP_WIN_RATE":0.3333
   },
   {
      "CHAMP_KDA":6.5,
      "CHAMP_NAME":"Malphite",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":2,
      "CHAMP_WIN_RATE":0.5
   },
   {
      "CHAMP_KDA":19.0,
      "CHAMP_NAME":"Blitzcrank",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":1,
      "CHAMP_WIN_RATE":1.0
   },
   {
      "CHAMP_KDA":23.0,
      "CHAMP_NAME":"Kassadin",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":1,
      "CHAMP_WIN_RATE":1.0
   },
   {
      "CHAMP_KDA":0.0,
      "CHAMP_NAME":"Viktor",
      "QUEUE_TYPE":"N/A",
      "CHAMP_COUNT":1,
      "CHAMP_WIN_RATE":0.0
   }
]