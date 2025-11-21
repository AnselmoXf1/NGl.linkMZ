import requests
import base64
import json
from datetime import datetime
from flask import current_app

class MpesaAPI:
    def __init__(self):
        self.consumer_key = current_app.config.get('MPESA_CONSUMER_KEY')
        self.consumer_secret = current_app.config.get('MPESA_CONSUMER_SECRET')
        self.shortcode = current_app.config.get('MPESA_SHORTCODE')
        self.passkey = current_app.config.get('MPESA_PASSKEY')
        self.environment = current_app.config.get('MPESA_ENVIRONMENT', 'sandbox')
        
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        """Get M-Pesa access token"""
        try:
            # Create auth string
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
            else:
                print(f"Error getting access token: {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception getting access token: {str(e)}")
            return None
    
    def stk_push(self, phone_number, amount, account_reference):
        """Initiate STK Push payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to get access token'}
            
            # Format phone number
            if not phone_number.startswith('258'):
                if phone_number.startswith('8'):
                    phone_number = f"258{phone_number}"
                elif phone_number.startswith('0'):
                    phone_number = f"258{phone_number[1:]}"
            
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Generate password
            password_string = f"{self.shortcode}{self.passkey}{timestamp}"
            password_bytes = password_string.encode('ascii')
            password_b64 = base64.b64encode(password_bytes).decode('ascii')
            
            # Prepare request data
            data = {
                "BusinessShortCode": self.shortcode,
                "Password": password_b64,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://your-domain.com/callback",  # Update with your domain
                "AccountReference": account_reference,
                "TransactionDesc": "NGL.MZ Message Reveal"
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ResponseCode') == '0':
                    return {
                        'success': True,
                        'receipt': result.get('CheckoutRequestID'),
                        'message': 'Payment request sent successfully'
                    }
                else:
                    return {
                        'success': False,
                        'error': result.get('ResponseDescription', 'Payment failed')
                    }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Exception: {str(e)}'
            }
    
    def query_stk_status(self, checkout_request_id):
        """Query STK Push status"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to get access token'}
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password_string = f"{self.shortcode}{self.passkey}{timestamp}"
            password_bytes = password_string.encode('ascii')
            password_b64 = base64.b64encode(password_bytes).decode('ascii')
            
            data = {
                "BusinessShortCode": self.shortcode,
                "Password": password_b64,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'status': result.get('ResultDesc'),
                    'result_code': result.get('ResultCode')
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Exception: {str(e)}'
            }
