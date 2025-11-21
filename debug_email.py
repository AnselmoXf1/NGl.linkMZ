#!/usr/bin/env python3
"""
Debug Email - NGL.MZ
Script para debugar problemas de email
"""

from flask import Flask
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'deeppianovibes@gmail.com'
app.config['MAIL_PASSWORD'] = 'hrgffnyfycnmqamo'
app.config['MAIL_DEFAULT_SENDER'] = 'NGL.MZ <deeppianovibes@gmail.com>'

mail = Mail(app)

def test_smtp_connection():
    """Teste direto de conexão SMTP"""
    try:
        print("🔍 Testando conexão SMTP direta...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('deeppianovibes@gmail.com', 'hrgffnyfycnmqamo')
        print("✅ Conexão SMTP direta funcionando!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Erro na conexão SMTP: {e}")
        return False

def test_flask_mail():
    """Teste com Flask-Mail"""
    try:
        print("🔍 Testando Flask-Mail...")
        with app.app_context():
            msg = Message(
                'Teste Flask-Mail',
                recipients=['deeppianovibes@gmail.com'],
                body='Teste de email com Flask-Mail'
            )
            mail.send(msg)
            print("✅ Flask-Mail funcionando!")
            return True
    except Exception as e:
        print(f"❌ Erro no Flask-Mail: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Debug de Email - NGL.MZ")
    print("=" * 50)
    
    # Teste 1: Conexão SMTP direta
    smtp_ok = test_smtp_connection()
    
    # Teste 2: Flask-Mail
    flask_ok = test_flask_mail()
    
    print("\n📊 Resultados:")
    print(f"SMTP Direto: {'✅' if smtp_ok else '❌'}")
    print(f"Flask-Mail: {'✅' if flask_ok else '❌'}")
    
    if smtp_ok and flask_ok:
        print("\n🎉 Todos os testes passaram! Email funcionando.")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique as configurações.")
