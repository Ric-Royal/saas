# PowerShell script to manage virtual environments for all services

$services = @(
    "churn-prediction",
    "civilbot",
    "billbot",
    "agri-insights",
    "tech-blog"
)

function Create-VirtualEnv {
    param (
        [string]$serviceName
    )
    
    $venvPath = "services/$serviceName/venv"
    
    Write-Host "Creating virtual environment for $serviceName..."
    
    # Create virtual environment
    python -m venv $venvPath
    
    # Activate virtual environment and install dependencies
    $activateScript = "services/$serviceName/venv/Scripts/Activate.ps1"
    . $activateScript
    
    # Install dependencies based on service type
    if (Test-Path "services/$serviceName/requirements.txt") {
        Write-Host "Installing Python dependencies..."
        pip install -r "services/$serviceName/requirements.txt"
    }
    elseif (Test-Path "services/$serviceName/package.json") {
        Write-Host "Installing Node.js dependencies..."
        npm install --prefix "services/$serviceName"
    }
    
    # Deactivate virtual environment
    deactivate
}

function Remove-VirtualEnv {
    param (
        [string]$serviceName
    )
    
    $venvPath = "services/$serviceName/venv"
    
    if (Test-Path $venvPath) {
        Write-Host "Removing virtual environment for $serviceName..."
        Remove-Item -Path $venvPath -Recurse -Force
    }
}

function Update-Dependencies {
    param (
        [string]$serviceName
    )
    
    Write-Host "Updating dependencies for $serviceName..."
    
    # Activate virtual environment
    $activateScript = "services/$serviceName/venv/Scripts/Activate.ps1"
    if (Test-Path $activateScript) {
        . $activateScript
        
        if (Test-Path "services/$serviceName/requirements.txt") {
            pip install -r "services/$serviceName/requirements.txt" --upgrade
        }
        elseif (Test-Path "services/$serviceName/package.json") {
            npm update --prefix "services/$serviceName"
        }
        
        deactivate
    }
    else {
        Write-Host "Virtual environment not found for $serviceName. Creating new one..."
        Create-VirtualEnv -serviceName $serviceName
    }
}

# Parse command line arguments
param (
    [Parameter(Mandatory=$true)]
    [ValidateSet('create', 'remove', 'update', 'create-all', 'remove-all', 'update-all')]
    [string]$action,
    
    [Parameter(Mandatory=$false)]
    [string]$service
)

switch ($action) {
    'create' {
        if ($service) {
            Create-VirtualEnv -serviceName $service
        }
        else {
            Write-Host "Please specify a service name"
        }
    }
    'remove' {
        if ($service) {
            Remove-VirtualEnv -serviceName $service
        }
        else {
            Write-Host "Please specify a service name"
        }
    }
    'update' {
        if ($service) {
            Update-Dependencies -serviceName $service
        }
        else {
            Write-Host "Please specify a service name"
        }
    }
    'create-all' {
        foreach ($svc in $services) {
            Create-VirtualEnv -serviceName $svc
        }
    }
    'remove-all' {
        foreach ($svc in $services) {
            Remove-VirtualEnv -serviceName $svc
        }
    }
    'update-all' {
        foreach ($svc in $services) {
            Update-Dependencies -serviceName $svc
        }
    }
} 