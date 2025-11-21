# NGL.MZ Email Configuration
# Este arquivo contém suas configurações de email

# Configurações de Email - CONFIGURADO
EMAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': 'deeppianovibes@gmail.com',
    'MAIL_PASSWORD': 'hrgffnyfycnmqamo',  # App Password atualizada
    'MAIL_DEFAULT_SENDER': 'NGL.MZ <deeppianovibes@gmail.com>'
}

# Para usar estas configurações, adicione ao app.py:
# from config_email import EMAIL_CONFIG
# app.config.update(EMAIL_CONFIG)
