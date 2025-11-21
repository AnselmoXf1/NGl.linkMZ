#!/usr/bin/env python3
"""
Teste de Email - NGL.MZ
Script para testar se o envio de email está funcionando
"""

from app import app, mail
from flask_mail import Message

def test_email():
    """Teste o envio de email"""
    try:
        with app.app_context():
            # Criar mensagem de teste
            msg = Message(
                subject='🧪 Teste de Email - NGL.MZ',
                recipients=['deeppianovibes@gmail.com'],
                html="""
                <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 28px;">🧪 NGL.MZ</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px;">Teste de Email</p>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 20px;">
                        <h2 style="color: #333; margin-top: 0;">✅ Email funcionando!</h2>
                        <p style="color: #666; line-height: 1.6;">
                            Se você recebeu este email, significa que a configuração de email está funcionando perfeitamente!
                        </p>
                        <p style="color: #666; line-height: 1.6;">
                            O sistema de recuperação de senha está pronto para uso.
                        </p>
                    </div>
                    
                    <div style="text-align: center; color: #999; font-size: 12px;">
                        <p>© 2024 NGL.MZ - Plataforma de Mensagens Anônimas</p>
                        <p>anselmo dora bistiro gulane</p>
                    </div>
                </body>
                </html>
                """
            )
            
            # Enviar email
            mail.send(msg)
            print("✅ Email de teste enviado com sucesso!")
            print("📧 Verifique sua caixa de entrada: deeppianovibes@gmail.com")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Testando configuração de email...")
    print("=" * 50)
    
    success = test_email()
    
    if success:
        print("\n🎉 Configuração de email funcionando perfeitamente!")
        print("📱 Agora você pode usar o sistema de recuperação de senha.")
    else:
        print("\n⚠️ Problema na configuração de email.")
        print("🔧 Verifique suas credenciais e configurações.")
