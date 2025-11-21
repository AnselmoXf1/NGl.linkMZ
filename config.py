import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mensagens.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # M-Pesa Configuration
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY') or 'S50TdhlpQu7zMn48P9Ue74K0koO2CTK6'
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET') or 'your-consumer-secret'
    MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE') or '174379'  # Sandbox shortcode
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY') or 'your-passkey'
    MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT') or 'sandbox'  # sandbox or production
    
    # Payment Configuration
    REVEAL_PRICE = 50.0  # Price in MZN to reveal sender information
    CURRENCY = 'MZN'
    
    # Security
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/mensagens.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mensagens.db'
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
