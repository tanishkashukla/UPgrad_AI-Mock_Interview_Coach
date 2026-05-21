$Root = $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    .\.venv\Scripts\pip install -r backend\requirements.txt
}
if (-not (Test-Path "frontend\node_modules")) {
    npm install --prefix frontend
}
if (-not (Test-Path ".env")) { Copy-Item .env.example .env }

$env:PYTHONPATH = $Root
$env:MOCK_LLM = "true"

Write-Host "Backend -> http://127.0.0.1:8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; `$env:PYTHONPATH='$Root'; `$env:MOCK_LLM='true'; .\.venv\Scripts\uvicorn.exe backend.main:app --reload --host 127.0.0.1 --port 8000"
Start-Sleep -Seconds 2
Write-Host "Frontend -> http://localhost:3000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\frontend'; `$env:NEXT_PUBLIC_API_URL='http://127.0.0.1:8000'; npm run dev"
