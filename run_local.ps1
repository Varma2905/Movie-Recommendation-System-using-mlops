# Run All Movie Recommendation Services Locally (Windows)
# This script starts the ML Service, Backend, and Frontend in separate processes.

$ProjectRoot = Get-Location

# 1. Start ML Service (Port 8001)
Write-Host "🚀 Starting ML Service on port 8001..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\ml-service'; ..\venv\Scripts\python -m uvicorn main:app --port 8001"

# 2. Start Backend (Port 8000)
Write-Host "🚀 Starting Backend on port 8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\backend'; ..\venv\Scripts\python -m uvicorn main:app --port 8000"

# 3. Start Frontend (Standard React Dev Port)
Write-Host "🚀 Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\frontend'; npm start"

Write-Host "`nAll services are starting in separate windows!" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend: http://localhost:8000"
Write-Host "ML Service: http://localhost:8001"
