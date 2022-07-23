from urllib import response
from fastapi import FastAPI, Request
import requests
from starlette.responses import RedirectResponse

REST_API_KEY = 'fea04d110f5bcad28342dc2f41563a09'
REDIRECT_URI = 'http://localhost:8000/callback'

# 인가 코드 받기
def get_kakao_auth():

    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        REST_API_KEY, REDIRECT_URI)
    return RedirectResponse(url)
    
# 토큰 받기
""" 불필요한 고통의 연속...
 괴로움의 구렁텅이..."""
def get_kakao_token(code):

    kauth_response = requests.post("https://kauth.kakao.com/oauth/token",
   
        data = {
            "grant_type" : "authorization_code",
            "client_id": REST_API_KEY,
            "redirect_uri" : REDIRECT_URI,
            "code" : code,
        }
    )

    print(kauth_response.json())
    return

   