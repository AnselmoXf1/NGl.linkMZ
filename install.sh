#!/bin/bash

echo "🇲🇿 NGL.MZ Installation Script"
echo "================================"

echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "📁 Creating directories..."
mkdir -p instance static/css static/js templates utils mpesa migrations

echo ""
echo "🗄️ Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

echo ""
echo "✅ Installation completed!"
echo ""
echo "🚀 To start the application, run:"
echo "   python run.py"
echo ""
echo "📱 The application will be available at: http://localhost:5000"
echo ""

# Make run.py executable
chmod +x run.py
chmod +x test_app.py

echo "🎉 Setup complete! You can now run the application."
