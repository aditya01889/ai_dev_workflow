# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed. Please install Docker and try again."
    exit 1
}

# Check if Docker Compose is installed
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
}

# Default Docker Compose file
$composeFile = "docker-compose.yml"

# Allow specifying a custom Docker Compose file
param (
    [string]$CustomComposeFile
)

if ($CustomComposeFile) {
    $composeFile = $CustomComposeFile
}

# Build and run the Docker Compose setup
try {
    Write-Output "Building and running Docker Compose setup using file: $composeFile"
    docker-compose -f $composeFile up --build -d
    Write-Output "Docker Compose setup completed successfully."
} catch {
    Write-Error "An error occurred while running Docker Compose: $_"
    exit 1
}
