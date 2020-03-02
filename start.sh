#!/usr/bin/env bash
cd /home/hopson/apps/usr/webserver/dbops
export "PYTHONUNBUFFERED"="1" 
export "PYTHONPATH"="/home/hopson/apps/usr/webserver/dbops"
export "PYTHON_HOME"="/home/hopson/apps/usr/webserver/dba/python3.6.0"
export LD_LIBRARY_PATH=${PYTHON3_HOME}/lib
nohup ${PPYTHON_HOME}/bin/python3 -u /home/hopson/apps/usr/webserver/dbops/web/controller/server.py ${1:-8200} &
