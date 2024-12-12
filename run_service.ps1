# PowerShell script to run services with their virtual environments

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet('churn-prediction', 'civilbot', 'billbot', 'agri-insights', 'tech-blog')]
    [string]$service,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'prod')]
    [string]$environment = 'dev'
)

function Start-PythonService {
    param (
        [string]$serviceName,
        [string]$env
    )
    
    $venvPath = "services/$serviceName/venv"
    $activateScript = "$venvPath/Scripts/Activate.ps1"
    
    if (-not (Test-Path $activateScript)) {
        Write-Host "Virtual environment not found. Creating one..."
        . ./manage_venv.ps1 -action create -service $serviceName
    }
    
    # Activate virtual environment
    . $activateScript
    
    # Set environment variables
    if (Test-Path "services/$serviceName/.env.$env") {
        Get-Content "services/$serviceName/.env.$env" | ForEach-Object {
            $name, $value = $_.split('=')
            Set-Item -Path "env:$name" -Value $value
        }
    }
    
    # Start the service based on the environment
    if ($env -eq 'dev') {
        uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
    }
    else {
        uvicorn app.main:app --port 8000 --host 0.0.0.0 --workers 4
    }
    
    # Deactivate virtual environment when done
    deactivate
}

function Start-NodeService {
    param (
        [string]$serviceName,
        [string]$env
    )
    
    $packagePath = "services/$serviceName/package.json"
    
    if (-not (Test-Path $packagePath)) {
        Write-Host "package.json not found for $serviceName"
        return
    }
    
    # Set environment variables
    if (Test-Path "services/$serviceName/.env.$env") {
        Get-Content "services/$serviceName/.env.$env" | ForEach-Object {
            $name, $value = $_.split('=')
            Set-Item -Path "env:$name" -Value $value
        }
    }
    
    # Start the service based on the environment
    Set-Location "services/$serviceName"
    if ($env -eq 'dev') {
        npm run dev
    }
    else {
        npm run start
    }
    Set-Location ../..
}

# Main execution
Write-Host "Starting $service in $environment mode..."

# Determine service type and start accordingly
if (Test-Path "services/$service/requirements.txt") {
    Start-PythonService -serviceName $service -env $environment
}
elseif (Test-Path "services/$service/package.json") {
    Start-NodeService -serviceName $service -env $environment
}
else {
    Write-Host "Unknown service type for $service"
} 