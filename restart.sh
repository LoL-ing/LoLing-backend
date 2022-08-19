PID=$(ps aux | grep 'port 8000' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
sudo kill -9 $PID
sleep 1
fi
cd /home/ubuntu/loadit-be
git switch develop
source /home/ubuntu/loadit-be/venv/bin/activate
sudo nohup ./venv/bin/python3 -m uvicorn app:app --port 443 --host 0.0.0.0 --ssl-keyfile=/etc/letsencrypt/live/$DOMAIN/privkey.pem --ssl-certfile=/etc/letsencrypt/live/$DOMAIN/fullchain.pem &
~
