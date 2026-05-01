# PowerShell setup script for Windows

Write-Host "Setting up Nifty100 Financial Intelligence Platform..." -ForegroundColor Green

# Python setup
Write-Host "Setting up Python environment..." -ForegroundColor Cyan
python -m venv venv
./venv/Scripts/Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt

# Django setup
Write-Host "Setting up Django..." -ForegroundColor Cyan
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

# Node setup
Write-Host "Setting up Node.js environment..." -ForegroundColor Cyan
cd frontend
npm install
cd ..

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To start development:" -ForegroundColor Yellow
Write-Host "  Backend: cd backend && python manage.py runserver" -ForegroundColor White
Write-Host "  Frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host "  Or use: docker-compose up" -ForegroundColor White
