# Test multilingual normalization
Write-Host "`n=== Testing Multilingual Normalization ===" -ForegroundColor Cyan

# Test 1: Hinglish query
Write-Host "`n1. Testing Hinglish query..." -ForegroundColor Yellow
$body1 = @{
    query = "Bhai async await kab use karte hai?"
} | ConvertTo-Json

$response1 = Invoke-RestMethod -Uri "http://localhost:8001/normalize" -Method POST -ContentType "application/json" -Body $body1
Write-Host "Original: $($response1.original_query)" -ForegroundColor Green
Write-Host "Normalized: $($response1.normalized_query)" -ForegroundColor Green
Write-Host "Language: $($response1.detected_language)" -ForegroundColor Green
Write-Host "Style: $($response1.explanation_style)" -ForegroundColor Green

# Test 2: Hindi query
Write-Host "`n2. Testing Hindi query..." -ForegroundColor Yellow
$body2 = @{
    query = "React hydration error kaise fix kare?"
} | ConvertTo-Json

$response2 = Invoke-RestMethod -Uri "http://localhost:8001/normalize" -Method POST -ContentType "application/json" -Body $body2
Write-Host "Original: $($response2.original_query)" -ForegroundColor Green
Write-Host "Normalized: $($response2.normalized_query)" -ForegroundColor Green
Write-Host "Language: $($response2.detected_language)" -ForegroundColor Green
Write-Host "Style: $($response2.explanation_style)" -ForegroundColor Green

# Test 3: English query
Write-Host "`n3. Testing English query..." -ForegroundColor Yellow
$body3 = @{
    query = "Explain binary search for beginners"
} | ConvertTo-Json

$response3 = Invoke-RestMethod -Uri "http://localhost:8001/normalize" -Method POST -ContentType "application/json" -Body $body3
Write-Host "Original: $($response3.original_query)" -ForegroundColor Green
Write-Host "Normalized: $($response3.normalized_query)" -ForegroundColor Green
Write-Host "Language: $($response3.detected_language)" -ForegroundColor Green
Write-Host "Style: $($response3.explanation_style)" -ForegroundColor Green

Write-Host "`n=== All tests completed! ===" -ForegroundColor Cyan
