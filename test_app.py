#!/usr/bin/env python3
"""
NGL.MZ Application Test Script
Simple tests to verify the application is working correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Message, Payment
from werkzeug.security import generate_password_hash

def test_database_connection():
    """Test database connection and table creation"""
    print("🔍 Testing database connection...")
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_creation():
    """Test user creation and authentication"""
    print("👤 Testing user creation...")
    try:
        with app.app_context():
            # Create test user
            test_user = User(
                username='testuser',
                email='test@ngl.mz',
                password_hash=generate_password_hash('testpassword')
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            # Verify user was created
            user = User.query.filter_by(username='testuser').first()
            if user:
                print("✅ User creation successful!")
                return True
            else:
                print("❌ User creation failed!")
                return False
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return False

def test_message_creation():
    """Test message creation"""
    print("💬 Testing message creation...")
    try:
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            if not user:
                print("❌ Test user not found!")
                return False
            
            # Create test message
            test_message = Message(
                content='Esta é uma mensagem de teste!',
                sender_ip='192.168.1.1',
                sender_browser='Mozilla/5.0 (Test Browser)',
                sender_location='Maputo, Moçambique',
                user_id=user.id
            )
            
            db.session.add(test_message)
            db.session.commit()
            
            # Verify message was created
            message = Message.query.filter_by(content='Esta é uma mensagem de teste!').first()
            if message:
                print("✅ Message creation successful!")
                return True
            else:
                print("❌ Message creation failed!")
                return False
    except Exception as e:
        print(f"❌ Message creation failed: {e}")
        return False

def test_flask_routes():
    """Test Flask routes"""
    print("🌐 Testing Flask routes...")
    try:
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page accessible!")
            else:
                print(f"❌ Home page failed: {response.status_code}")
                return False
            
            # Test register page
            response = client.get('/register')
            if response.status_code == 200:
                print("✅ Register page accessible!")
            else:
                print(f"❌ Register page failed: {response.status_code}")
                return False
            
            # Test login page
            response = client.get('/login')
            if response.status_code == 200:
                print("✅ Login page accessible!")
            else:
                print(f"❌ Login page failed: {response.status_code}")
                return False
            
            return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("🧹 Cleaning up test data...")
    try:
        with app.app_context():
            # Delete test messages
            Message.query.filter_by(content='Esta é uma mensagem de teste!').delete()
            
            # Delete test user
            User.query.filter_by(username='testuser').delete()
            
            db.session.commit()
            print("✅ Test data cleaned up!")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

def main():
    """Run all tests"""
    print("🧪 NGL.MZ Application Tests")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_user_creation,
        test_message_creation,
        test_flask_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Cleanup
    cleanup_test_data()
    
    # Results
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
