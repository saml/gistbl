#!/bin/bash

if (( $# < 1 ))
then
    echo "Usage: $0 status|start|stop|reload"
    exit 1
fi

nginx_cmd="${2:-nginx}"

pid_path="logs/nginx.pid"
conf_path="conf/nginx.conf"

nginx_status() {
    if [[ -f "$pid_path" ]] 
    then
        echo "Started."
    else
        echo "Stopped."
    fi
}

nginx_stop() {
    if [[ -f "$pid_path" ]]
    then
        "$nginx_cmd" -p "${PWD}/" -s stop
    fi
}

nginx_start() {
    "$nginx_cmd" -p "${PWD}/" -c "$conf_path"
}

nginx_reload() {
    kill -HUP "$(cat $pid_path)"
}

case "$1" in
    status)
        nginx_status
        ;;
    start)
        nginx_stop
        nginx_start
        ;;
    stop)
        nginx_stop
        ;;
    reload)
        nginx_reload
        ;;
esac
