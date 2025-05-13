#!/bin/bash

echo "Starting Barbeque Nation Chatbot..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in your PATH."
    echo "Please install Python 3.8 or newer and try again."
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "Go is not installed or not in your PATH."
    echo "Please install Go 1.16 or newer and try again."
    exit 1
fi

echo "Starting the Python API server on port 8000..."
python3 server.py &
PYTHON_PID=$!

echo "Starting the Go web server on port 8080..."
cd chatbot
echo "Please visit http://localhost:8080/ to access the chatbot."
go run server.go &
GO_PID=$!

echo "Both servers started. Press Ctrl+C to stop."

# Handle shutdown gracefully
trap "kill $PYTHON_PID $GO_PID; exit" INT TERM
wait 