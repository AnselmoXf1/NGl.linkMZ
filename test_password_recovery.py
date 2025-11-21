#!/usr/bin/env python3
"""
Teste do Sistema de Recuperação de Senha
Este script testa se o sistema aceita emails de todos os usuários registrados
"""

import os
import sys
from app import app, db, User, PasswordResetToken, send_password_reset_email
from datetime import datetime, timedelta
import uuid

def test_password_recovery():
    """Testa o sistema de recuperação de senha"""
    print("🔐 Testando Sistema de Recuperação de Senha")
    print("=" * 50)
    
    with app.app_context():
        # Listar todos os usuários registrados
        users = User.query.all()
        
        if not users:
            print("❌ Nenhum usuário encontrado no banco de dados!")
            print("   Registre alguns usuários primeiro para testar.")
            return
        
        print(f"📊 Encontrados {len(users)} usuários registrados:")
        print("-" * 30)
        
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.username} - {user.email}")
        
        print("\n🧪 Testando recuperação de senha para cada usuário:")
        print("-" * 50)
        
        success_count = 0
        error_count = 0
        
        for user in users:
            try:
                print(f"\n📧 Testando para: {user.username} ({user.email})")
                
                # Gerar token de reset
                token = str(uuid.uuid4())
                expires_at = datetime.utcnow() + timedelta(hours=1)
                
                # Invalidar tokens existentes
                PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({'used': True})
                
                # Criar novo token
                reset_token = PasswordResetToken(
                    user_id=user.id,
                    token=token,
                    expires_at=expires_at
                )
                
                db.session.add(reset_token)
                db.session.commit()
                
                # Tentar enviar email
                try:
                    send_password_reset_email(user.email, token)
                    print(f"   ✅ Email enviado com sucesso!")
                    success_count += 1
                except Exception as e:
                    print(f"   ❌ Erro ao enviar email: {e}")
                    error_count += 1
                
            except Exception as e:
                print(f"   ❌ Erro geral: {e}")
                error_count += 1
        
        print("\n" + "=" * 50)
        print("📊 RESUMO DOS TESTES:")
        print(f"✅ Sucessos: {success_count}")
        print(f"❌ Erros: {error_count}")
        print(f"📧 Total testado: {len(users)}")
        
        if success_count == len(users):
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("   O sistema aceita emails de todos os usuários registrados.")
        elif success_count > 0:
            print(f"\n⚠️  PARCIALMENTE FUNCIONAL")
            print(f"   {success_count}/{len(users)} usuários conseguiram receber emails.")
        else:
            print("\n❌ SISTEMA COM PROBLEMAS")
            print("   Nenhum email foi enviado com sucesso.")
            print("   Verifique as configurações de email.")

def test_specific_user():
    """Testa recuperação para um usuário específico"""
    print("\n🔍 Teste para Usuário Específico")
    print("=" * 30)
    
    email = input("Digite o email do usuário para testar: ").strip()
    
    if not email:
        print("❌ Email não fornecido!")
        return
    
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuário com email '{email}' não encontrado!")
            return
        
        print(f"✅ Usuário encontrado: {user.username}")
        
        try:
            # Gerar token
            token = str(uuid.uuid4())
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # Invalidar tokens existentes
            PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({'used': True})
            
            # Criar novo token
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            # Enviar email
            send_password_reset_email(user.email, token)
            print(f"✅ Email de recuperação enviado para {user.email}")
            print(f"🔗 Token gerado: {token}")
            print(f"⏰ Expira em: {expires_at}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")

def show_user_list():
    """Mostra lista de usuários registrados"""
    print("\n👥 Usuários Registrados:")
    print("=" * 30)
    
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("❌ Nenhum usuário encontrado!")
            return
        
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.username} - {user.email}")

def main():
    """Menu principal"""
    while True:
        print("\n🔐 TESTE DE RECUPERAÇÃO DE SENHA")
        print("=" * 40)
        print("1. Testar todos os usuários")
        print("2. Testar usuário específico")
        print("3. Listar usuários registrados")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == '1':
            test_password_recovery()
        elif choice == '2':
            test_specific_user()
        elif choice == '3':
            show_user_list()
        elif choice == '4':
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    main()

