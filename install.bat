@echo off
echo 🇲🇿 NGL.MZ Installation Script
echo ================================

echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 📁 Creating directories...
if not exist "instance" mkdir instance
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates
if not exist "utils" mkdir utils
if not exist "mpesa" mkdir mpesa
if not exist "migrations" mkdir migrations

echo.
echo 🗄️ Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

echo.
echo ✅ Installation completed!
echo.
echo 🚀 To start the application, run:
echo    python run.py
echo.
echo 📱 The application will be available at: http://localhost:5000
echo.
pause
