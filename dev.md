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

2. 지금은 `/profile` 만 테스트로 진행해 보았음. 나머지 lol_name 이 하드코딩 되어있는 것들 도 현재 형태로 바꾸어야 함.
   2-1. 프론트의 더미데이터에 필요한 정보 자체는 똑같이 맞추었으나, 프론트의 데이터 양식과 백엔드에서 실제로 보내주는 양식에 차이가 있음. 
       이를 맞추면서 바꿔야 함. 