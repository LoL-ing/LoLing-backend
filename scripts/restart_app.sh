PID=$(ps aux | grep 'port 8000' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
sudo kill -9 $PID
sleep 1
fi
cd /home/ubuntu/LoLing-backend
git switch master
source /home/ubuntu/LoLing-backend/venv/bin/activate
sudo nohup /home/ubuntu/LoLing-backend/venv/bin/python3 -m uvicorn main:app --port 8000 &
