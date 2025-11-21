import hashlib
import secrets
import requests
from flask import request

def get_client_info(request):
    """Extract client information from request"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'Unknown'))
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Try to get location from IP (simplified)
    location = get_location_from_ip(client_ip)
    
    return {
        'ip': client_ip,
        'browser': user_agent,
        'location': location
    }

def get_location_from_ip(ip):
    """Get location from IP address using a free service"""
    try:
        if ip == '127.0.0.1' or ip.startswith('192.168.') or ip.startswith('10.'):
            return 'Local Network'
        
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return f"{data['city']}, {data['country']}"
    except:
        pass
    
    return 'Unknown Location'

def generate_unique_link(username):
    """Generate a unique link for a user"""
    return f"/u/{username}"

def hash_content(content):
    """Create a hash of content for verification"""
    return hashlib.sha256(content.encode()).hexdigest()

def generate_secure_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def validate_phone_number(phone):
    """Validate Mozambican phone number format"""
    # Remove all non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    
    # Mozambican phone numbers should be 9 digits starting with 8
    if len(phone) == 9 and phone.startswith('8'):
        return f"258{phone}"
    elif len(phone) == 12 and phone.startswith('258'):
        return phone
    else:
        return None

def format_currency(amount, currency='MZN'):
    """Format currency amount"""
    return f"{amount:.2f} {currency}"
