#!/usr/bin/env python3
"""
NGL.MZ Application Startup Script
Run this script to start the NGL.MZ application
"""

import os
import sys
from app import app, db

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['instance', 'static/css', 'static/js', 'templates', 'utils', 'mpesa', 'migrations']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def initialize_database():
    """Initialize the database with tables"""
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def main():
    """Main function to start the application"""
    print("🇲🇿 Starting NGL.MZ Application...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    # Start the application
    print("\n🚀 Application is starting...")
    print("📱 Access the application at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
