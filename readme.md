## 로컬에서 실행

1. 가상환경 활성화

`. venv/bin/activate`
`. venv/Scripts/activate`

2. FastAPI app 실행

`uvicorn main:app --port 8000 --host 0.0.0.0 --reload`
--> 사이트에 연결할 수 없다고 떠서 port랑 host지정 빼니까 잘열림 (양여름)

3. Window 에서 mongodb 연결 안될 때 (양여름)
   a. https://blog.minamiland.com/551 --> 해결못함

pip install -r requirements.txt


4. 
pem키 인증
ssh -i "LoLing-backend.pem" ubuntu@ec2-54-165-207-136.compute-1.amazonaws.com
aws 배포 
'./scripts/restart_app.sh' 