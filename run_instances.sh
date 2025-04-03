#!/bin/bash
# Script to run multiple instances of the Flask application with different ports

# Colors for terminal output
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Default ports
DEV_PORT=5000
TEST_PORT=5001
CUSTOM_PORT=5002

# Process IDs for cleanup
PIDS=()

# Function to start an instance
start_instance() {
    local config=$1
    local port=$2
    local name=$3

    echo -e "${GREEN}Starting ${name} instance on port ${port}...${NC}"

    # Export environment variables
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export FLASK_CONFIG=$config
    export FLASK_INSTANCE=$name
    export SERVER_PORT=$port

    # Start the Flask application in the background
    python run.py &

    # Store the process ID
    local pid=$!
    PIDS+=($pid)

    echo -e "${BLUE}Instance started with PID: ${pid}${NC}"
    echo -e "${YELLOW}Access at: http://localhost:${port}${NC}"
    echo ""
}

# Function to clean up processes
cleanup() {
    echo -e "\n${RED}Terminating all instances...${NC}"
    for pid in "${PIDS[@]}"; do
        if ps -p $pid > /dev/null; then
            echo -e "${YELLOW}Stopping process with PID: ${pid}${NC}"
            kill $pid
        fi
    done
    echo -e "${GREEN}All instances terminated.${NC}"
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dev-port)
            DEV_PORT="$2"
            shift 2
            ;;
        --test-port)
            TEST_PORT="$2"
            shift 2
            ;;
        --custom-port)
            CUSTOM_PORT="$2"
            shift 2
            ;;
        --dev-only)
            DEV_ONLY=true
            shift
            ;;
        --test-only)
            TEST_ONLY=true
            shift
            ;;
        --custom-only)
            CUSTOM_ONLY=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --dev-port PORT    Set development instance port (default: 5000)"
            echo "  --test-port PORT   Set test instance port (default: 5001)"
            echo "  --custom-port PORT Set custom instance port (default: 5002)"
            echo "  --dev-only         Start only the development instance"
            echo "  --test-only        Start only the test instance"
            echo "  --custom-only      Start only the custom instance"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Start instances based on flags
if [[ -n "$DEV_ONLY" ]]; then
    start_instance "development" "$DEV_PORT" "dev"
elif [[ -n "$TEST_ONLY" ]]; then
    start_instance "testing" "$TEST_PORT" "test"
elif [[ -n "$CUSTOM_ONLY" ]]; then
    start_instance "development" "$CUSTOM_PORT" "custom"
else
    # Start all instances by default
    start_instance "development" "$DEV_PORT" "dev"
    start_instance "testing" "$TEST_PORT" "test"
fi

echo -e "${GREEN}All requested instances are running.${NC}"
echo -e "${YELLOW}Press Ctrl+C to terminate all instances.${NC}"

# Keep the script running
while true; do
    sleep 1
done
