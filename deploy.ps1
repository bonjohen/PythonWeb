# PowerShell deployment script for the Flask application

# Function to display help message
function Show-Help {
    Write-Host "Usage: .\deploy.ps1 [options]"
    Write-Host "Options:"
    Write-Host "  -Env ENV        Specify environment (dev, test, prod) [default: prod]"
    Write-Host "  -Build          Build Docker images"
    Write-Host "  -Down           Stop and remove containers before deploying"
    Write-Host "  -Migrate        Run database migrations"
    Write-Host "  -Help           Show this help message"
    exit 0
}

# Parse arguments
param(
    [string]$Env = "prod",
    [switch]$Build = $false,
    [switch]$Down = $false,
    [switch]$Migrate = $false,
    [switch]$Help = $false
)

# Show help if requested
if ($Help) {
    Show-Help
}

# Validate environment
if ($Env -notin @("dev", "test", "prod")) {
    Write-Host "Invalid environment: $Env"
    Write-Host "Valid environments are: dev, test, prod"
    exit 1
}

# Set environment-specific variables
if ($Env -eq "dev") {
    $ComposeFile = "docker-compose.yml"
    $EnvFile = ".env.development"
}
elseif ($Env -eq "test") {
    $ComposeFile = "docker-compose.yml"
    $EnvFile = ".env.testing"
}
else {
    $ComposeFile = "docker-compose.yml"
    $EnvFile = ".env.production"
}

# Check if environment file exists
if (-not (Test-Path $EnvFile)) {
    Write-Host "Environment file $EnvFile not found!"
    Write-Host "Please create it from the example file: Copy-Item ${EnvFile}.example ${EnvFile}"
    exit 1
}

# Stop and remove containers if requested
if ($Down) {
    Write-Host "Stopping and removing containers..."
    docker-compose -f $ComposeFile down
}

# Build Docker images if requested
if ($Build) {
    Write-Host "Building Docker images..."
    docker-compose -f $ComposeFile build
}

# Start the application
Write-Host "Starting the application in $Env environment..."
docker-compose -f $ComposeFile up -d

# Run database migrations if requested
if ($Migrate) {
    Write-Host "Running database migrations..."
    docker-compose -f $ComposeFile exec web flask db upgrade
}

Write-Host "Deployment completed successfully!"
Write-Host "The application is now running in $Env environment."
