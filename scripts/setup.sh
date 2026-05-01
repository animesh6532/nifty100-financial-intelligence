#!/bin/bash
# Setup script for development environment

echo "Setting up Nifty100 Financial Intelligence Platform..."

# Python setup
echo "Setting up Python environment..."
python -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Django setup
echo "Setting up Django..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

# Node setup
echo "Setting up Node.js environment..."
cd frontend
npm install
cd ..

echo "Setup complete!"
echo "To start development:"
echo "  Backend: cd backend && python manage.py runserver"
echo "  Frontend: cd frontend && npm run dev"
echo "  Or use: docker-compose up"
