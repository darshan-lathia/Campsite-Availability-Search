#!/bin/bash

# Configuration
APP_DIR="$(pwd)"
GUNICORN_BIN="gunicorn"
PID_FILE="$APP_DIR/gunicorn.pid"
LOG_DIR="$APP_DIR/logs"
ACCESS_LOG="$LOG_DIR/access.log"
ERROR_LOG="$LOG_DIR/error.log"
BIND_ADDRESS="127.0.0.1:5000"

# Ensure log directory exists
mkdir -p $LOG_DIR

# Function to check if the server is running
check_status() {
    if [ -f $PID_FILE ]; then
        pid=$(cat $PID_FILE)
        if ps -p $pid > /dev/null; then
            echo "Server is running (PID: $pid)"
            
            # Calculate uptime
            start_time=$(ps -p $pid -o lstart=)
            current_time=$(date)
            echo "Running since: $start_time"
            
            # Get request count from access log
            if [ -f $ACCESS_LOG ]; then
                requests=$(wc -l < $ACCESS_LOG)
                echo "Total requests served: $requests"
            fi
            
            # Show recent errors if any
            if [ -f $ERROR_LOG ]; then
                echo -e "\nRecent errors (if any):"
                tail -n 5 $ERROR_LOG
            fi
            
            # Show resource usage
            echo -e "\nResource usage:"
            ps -p $pid -o %cpu,%mem,rss
            
            return 0
        fi
    fi
    echo "Server is not running"
    return 1
}

# Start the server
start() {
    if check_status > /dev/null; then
        echo "Server is already running"
    else
        echo "Starting server..."
        cd $APP_DIR
        $GUNICORN_BIN \
            --daemon \
            --pid $PID_FILE \
            --bind $BIND_ADDRESS \
            --workers 3 \
            --access-logfile $ACCESS_LOG \
            --error-logfile $ERROR_LOG \
            --capture-output \
            --reload \
            app:app
        sleep 2
        check_status
    fi
}

# Stop the server
stop() {
    if [ -f $PID_FILE ]; then
        echo "Stopping server..."
        pid=$(cat $PID_FILE)
        kill -TERM $pid
        rm -f $PID_FILE
        echo "Server stopped"
    else
        echo "Server is not running"
    fi
}

# Restart the server
restart() {
    stop
    sleep 2
    start
}

# Show logs
logs() {
    echo "Access log (last 10 lines):"
    tail -n 10 $ACCESS_LOG
    echo -e "\nError log (last 10 lines):"
    tail -n 10 $ERROR_LOG
}

# Main script logic
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        check_status
        ;;
    logs)
        logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac

exit 0 