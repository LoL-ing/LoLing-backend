# TODO: python 미설치자 지원

####### 맨 처음 실행 전, 권한 주기 #######
###### 윈도우는 필요 없을지도... #########
# chmod 700 ./scripts/run_local.sh
#####################################

# 기존 8000번 port 에서 실행되는 프로세스 kill
PID=$(ps aux | grep 'port 8000' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
sudo kill -9 $PID
sleep 1
fi

cd app

# 가상환경 없다면 생성
if (ls | grep venv)
then
echo "venv exists"
else
python3 -m venv venv
echo "venv created"
sleep 1
fi

# 가상환경 열기
if(. venv/Scripts/activate)
then
echo "venv activated by . app/venv/Scripts/activate"
else
. venv/bin/activate
echo "venv activated by . app/venv/bin/activate "
fi 


# 의존성 설치
pip install -r requirements.txt

cd ../

# 로컬 서버 실행
uvicorn app.main:app --port 8000 --reload