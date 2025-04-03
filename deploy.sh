#!/bin/bash
# Deployment script for the Flask application

# Exit on error
set -e

# Display help message
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -e, --env ENV     Specify environment (dev, test, prod) [default: prod]"
    echo "  -b, --build       Build Docker images"
    echo "  -d, --down        Stop and remove containers before deploying"
    echo "  -m, --migrate     Run database migrations"
    echo "  -h, --help        Show this help message"
    exit 0
}

# Default values
ENV="prod"
BUILD=false
DOWN=false
MIGRATE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -d|--down)
            DOWN=true
            shift
            ;;
        -m|--migrate)
            MIGRATE=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Validate environment
if [[ "$ENV" != "dev" && "$ENV" != "test" && "$ENV" != "prod" ]]; then
    echo "Invalid environment: $ENV"
    echo "Valid environments are: dev, test, prod"
    exit 1
fi

# Set environment-specific variables
if [[ "$ENV" == "dev" ]]; then
    COMPOSE_FILE="docker-compose.yml"
    ENV_FILE=".env.development"
elif [[ "$ENV" == "test" ]]; then
    COMPOSE_FILE="docker-compose.yml"
    ENV_FILE=".env.testing"
else
    COMPOSE_FILE="docker-compose.yml"
    ENV_FILE=".env.production"
fi

# Check if environment file exists
if [[ ! -f "$ENV_FILE" ]]; then
    echo "Environment file $ENV_FILE not found!"
    echo "Please create it from the example file: cp ${ENV_FILE}.example ${ENV_FILE}"
    exit 1
fi

# Stop and remove containers if requested
if [[ "$DOWN" == true ]]; then
    echo "Stopping and removing containers..."
    docker-compose -f "$COMPOSE_FILE" down
fi

# Build Docker images if requested
if [[ "$BUILD" == true ]]; then
    echo "Building Docker images..."
    docker-compose -f "$COMPOSE_FILE" build
fi

# Start the application
echo "Starting the application in $ENV environment..."
docker-compose -f "$COMPOSE_FILE" up -d

# Run database migrations if requested
if [[ "$MIGRATE" == true ]]; then
    echo "Running database migrations..."
    docker-compose -f "$COMPOSE_FILE" exec web flask db upgrade
fi

echo "Deployment completed successfully!"
echo "The application is now running in $ENV environment."
