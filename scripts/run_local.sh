### 맨 처음 실행 전, 권한 주기 ############
# chmod 700 ./scripts/run_local.sh
#####################################

# 기존 8000번 port 에서 실행되는 프로세스 kill
PID=$(ps aux | grep 'port 8000' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
sudo kill -9 $PID
sleep 1
fi

# 가상환경 열기
. venv/bin/activate || . venv/Scripts/activate

# 의존성 설치
pip install -r requirements.txt

# 로컬 서버 실행
uvicorn main:app --port 8000 --reload