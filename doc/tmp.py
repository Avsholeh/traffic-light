from datetime import datetime
import time

db_server = {'date-modified': str(datetime.now())}
time.sleep(2)
db_client = {'date-modified': str(datetime.now())}


server = datetime.strptime(db_server['date-modified'],
"%Y-%m-%d %H:%M:%S.%f")
client = datetime.strptime(db_client['date-modified'],
"%Y-%m-%d %H:%M:%S.%f")

print db_server
