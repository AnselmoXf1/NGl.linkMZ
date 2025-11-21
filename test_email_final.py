#!/usr/bin/env python3
"""
Teste Final de Email - NGL.MZ
Execute este script após configurar sua App Password
"""

from flask import Flask
from flask_mail import Mail, Message
import os

# Configuração de email
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'deeppianovibes@gmail.com'
app.config['MAIL_PASSWORD'] = 'hrgffnyfycnmqamo'  # Nova App Password configurada
app.config['MAIL_DEFAULT_SENDER'] = 'NGL.MZ <deeppianovibes@gmail.com>'

mail = Mail(app)

def test_email():
    """Teste o envio de email"""
    try:
        with app.app_context():
            msg = Message(
                '🧪 Teste de Email - NGL.MZ',
                recipients=['deeppianovibes@gmail.com'],
                body='Este é um teste de email do NGL.MZ. Se você recebeu este email, a configuração está funcionando!'
            )
            mail.send(msg)
            print("✅ SUCESSO: Email enviado com sucesso!")
            print("📧 Verifique sua caixa de entrada: deeppianovibes@gmail.com")
            return True
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print("\n🔧 SOLUÇÃO:")
        print("1. Verifique se a verificação em 2 etapas está ativada")
        print("2. Gere uma nova App Password no Google")
        print("3. Substitua 'COLE_SUA_APP_PASSWORD_AQUI' pela senha gerada")
        return False

if __name__ == '__main__':
    print("🧪 Testando configuração de email...")
    print("=" * 50)
    
    if app.config['MAIL_PASSWORD'] == 'COLE_SUA_APP_PASSWORD_AQUI':
        print("⚠️ ATENÇÃO: Você precisa configurar sua App Password primeiro!")
        print("📝 Edite o arquivo test_email_final.py e substitua 'COLE_SUA_APP_PASSWORD_AQUI'")
        print("🔗 Gere uma App Password em: https://myaccount.google.com/apppasswords")
    else:
        test_email()
