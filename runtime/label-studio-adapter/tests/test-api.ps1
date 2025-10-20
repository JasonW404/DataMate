# Label Studio Adapter API Test Script
# Test Label Studio Adapter API and JWT token flow

# Set encoding for proper display
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== Label Studio Adapter API Test ===" -ForegroundColor Cyan

# Test Adapter API - Create Dataset Mapping
Write-Host "`n1. Testing Adapter Create Dataset Mapping..." -ForegroundColor Yellow
$uri = "http://localhost:8000/datasets/create"
$headers = @{ "Content-Type" = "application/json" }
$body = @{
    source_dataset_uuid = "97ea6bf8-f4a2-4cd9-a48d-7e0ad81d918e"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $uri -Method POST -Headers $headers -Body $body -TimeoutSec 30
    Write-Host "Adapter API Request Successful!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Adapter API Request Failed:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response Body: $responseBody" -ForegroundColor Yellow
        } catch {
            Write-Host "Cannot read error response" -ForegroundColor Gray
        }
    }
}

Write-Host "`n=== Test Completed ===" -ForegroundColor Cyan
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")