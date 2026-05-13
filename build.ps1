$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $projectRoot

try {
    Write-Host "Syncing Python dependencies..."
    uv sync

    Write-Host "Installing npm dependencies..."
    npm.cmd install

    Write-Host "Checking Python syntax..."
    uv run python -m compileall src

    Write-Host "Building Flet web app..."
    $env:PYTHONIOENCODING = "utf-8"
    $env:PYTHONUTF8 = "1"
    uv run flet build web . --route-url-strategy path --base-url /

    Write-Host "Build complete: build/web"
}
finally {
    Pop-Location
}
