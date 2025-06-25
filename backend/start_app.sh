#!/bin/bash

PORT=10011

PID=$(netstat -tulpn 2>/dev/null | grep :$PORT | awk '{print $7}' | cut -d/ -f1)
if [ -n "$PID" ]; then
    kill -9 $PID
    echo "已终止进程 $PID"
else
    echo "未找到监听端口 $PORT 的进程"
fi

MAX_ATTEMPTS=10
DELAY=2

for ((i=1; i<=MAX_ATTEMPTS; i++)); do
    if netstat -tulpn | grep -q ":$PORT "; then
        echo "第 $i 次检查：端口 $PORT 正在被监听"
        sleep $DELAY
    else
        echo "第 $i 次检查：端口 $PORT 未被监听，等待 $DELAY 秒后重试..."
        nohup python backend/app.py &
        exit 0
    fi
done