#!/usr/bin/env bash
cd /home/hopson/apps/usr/webserver/dbops
export "PYTHONUNBUFFERED"="1" 
export "PYTHONPATH"="/home/hopson/apps/usr/webserver/dbops"
export "PYTHON_HOME"="/usr/local/python3.6"
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
nohup ${PYTHON_HOME}/bin/python3 -u /home/hopson/apps/usr/webserver/dbops/web/task/run_task.py &>>task.log &
