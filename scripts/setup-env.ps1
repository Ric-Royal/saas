#!/usr/bin/env pwsh

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('development', 'production', 'staging')]
    [string]$Environment = 'development'
)

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Initialize logging
function Write-Log {
    param($Message)
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $Message"
}

# Verify prerequisites
function Test-Prerequisites {
    Write-Log "Checking prerequisites..."
    
    $requirements = @{
        "Python" = "python --version"
        "Node.js" = "node --version"
        "Docker" = "docker --version"
        "Git" = "git --version"
    }

    foreach ($req in $requirements.GetEnumerator()) {
        try {
            $version = Invoke-Expression $req.Value
            Write-Log "✓ $($req.Key) found: $version"
        }
        catch {
            Write-Log "✗ $($req.Key) not found. Please install it and try again."
            exit 1
        }
    }
}

# Merge environment files
function Merge-EnvFiles {
    Write-Log "Merging environment files..."
    
    # Read template and example files
    $templatePath = ".env.template"
    $examplePath = ".env.example"
    $outputPath = ".env"
    
    if (!(Test-Path $templatePath) -or !(Test-Path $examplePath)) {
        Write-Log "Error: Required environment template files not found"
        exit 1
    }
    
    # Merge the files
    $template = Get-Content $templatePath
    $example = Get-Content $examplePath
    
    # Create sections from both files
    $merged = @"
# =========================================
# Unified Environment Configuration
# Generated on: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Environment: $Environment
# =========================================

# Global Configuration
NODE_ENV=$Environment
DEBUG=$(if ($Environment -eq 'development') { 'true' } else { 'false' })

# Service Ports
PORT_PUBLIC_PARTICIPATION=8000
PORT_CIVILBOT=8001
PORT_BILLBOT=8002
PORT_AGRI_INSIGHTS=8003
PORT_TECH_BLOG=3004

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changeme
POSTGRES_DB_PUBLIC_PARTICIPATION=public_participation
POSTGRES_DB_BILLBOT=billbot
POSTGRES_DB_AGRI_INSIGHTS=agri_insights

# MongoDB Configuration
MONGODB_URI_CIVILBOT=mongodb://localhost:27017/civilbot
MONGODB_URI_TECH_BLOG=mongodb://localhost:27017/tech-blog

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=changeme

# JWT Configuration
JWT_SECRET=your-secret-key-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Service URLs
API_BASE_URL=http://localhost:3000
FRONTEND_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeme

# AWS Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# Security Settings
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
SSL_CERT_PATH=/etc/nginx/ssl/fullchain.pem
SSL_KEY_PATH=/etc/nginx/ssl/privkey.pem

# Monitoring Configuration
ENABLE_METRICS=true
METRICS_PORT=9090
GRAFANA_PORT=3000
KIBANA_PORT=5601
JAEGER_PORT=16686
LOG_LEVEL=info

# Backup Configuration
BACKUP_RETENTION_DAYS=30
BACKUP_TIME=00:00
"@

    # Write merged configuration
    $merged | Set-Content $outputPath
    Write-Log "✓ Environment files merged successfully"
}

# Initialize Python virtual environments
function Initialize-PythonServices {
    Write-Log "Initializing Python services..."
    
    $pythonServices = @(
        "services/public-participation",
        "services/civilbot",
        "services/billbot",
        "services/agri-insights"
    )
    
    foreach ($service in $pythonServices) {
        Write-Log "Setting up $service..."
        Push-Location $service
        
        # Create and activate virtual environment
        python -m venv venv
        & ./venv/Scripts/Activate.ps1
        
        # Install requirements
        pip install -r requirements.txt
        
        # Deactivate and return
        deactivate
        Pop-Location
    }
}

# Initialize Node.js services
function Initialize-NodeServices {
    Write-Log "Initializing Node.js services..."
    
    $nodeServices = @(
        "services/tech-blog",
        "frontend"
    )
    
    foreach ($service in $nodeServices) {
        Write-Log "Setting up $service..."
        Push-Location $service
        npm install
        Pop-Location
    }
}

# Main execution
try {
    Write-Log "Starting unified setup for $Environment environment"
    
    # Run setup steps
    Test-Prerequisites
    Merge-EnvFiles
    Initialize-PythonServices
    Initialize-NodeServices
    
    Write-Log "Setup completed successfully!"
    Write-Log "You can now start the services using: docker-compose up -d"
}
catch {
    Write-Log "Error during setup: $_"
    exit 1
} 