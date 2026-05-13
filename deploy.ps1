$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $projectRoot

try {
    Write-Host "Building app before deploy..."
    & (Join-Path $projectRoot "build.ps1")

    Write-Host "Deploying to Cloudflare..."
    npx.cmd wrangler deploy
}
finally {
    Pop-Location
}
