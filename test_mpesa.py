#!/usr/bin/env python3
"""
Teste da Configuração M-Pesa
Este script testa se a configuração do M-Pesa está funcionando corretamente
"""

import os
import sys
from app import app
from mpesa.mpesa_api import MpesaAPI

def test_mpesa_config():
    """Testa a configuração do M-Pesa"""
    print("📱 Testando Configuração M-Pesa")
    print("=" * 40)
    
    with app.app_context():
        # Verificar configurações
        print("🔧 Configurações atuais:")
        print(f"   Consumer Key: {app.config.get('MPESA_CONSUMER_KEY')}")
        print(f"   Consumer Secret: {app.config.get('MPESA_CONSUMER_SECRET')}")
        print(f"   Shortcode: {app.config.get('MPESA_SHORTCODE')}")
        print(f"   Passkey: {app.config.get('MPESA_PASSKEY')}")
        print(f"   Environment: {app.config.get('MPESA_ENVIRONMENT')}")
        
        # Testar inicialização da API
        try:
            mpesa = MpesaAPI()
            print("\n✅ M-Pesa API inicializada com sucesso!")
            
            # Testar obtenção de access token
            print("\n🔑 Testando obtenção de access token...")
            access_token = mpesa.get_access_token()
            
            if access_token:
                print(f"✅ Access token obtido: {access_token[:20]}...")
                
                # Testar STK Push (simulado)
                print("\n💳 Testando STK Push...")
                result = mpesa.stk_push("258841234567", 50.0, "TEST123")
                
                if result['success']:
                    print("✅ STK Push configurado corretamente!")
                    print(f"   Receipt: {result.get('receipt')}")
                else:
                    print(f"❌ Erro no STK Push: {result.get('error')}")
            else:
                print("❌ Falha ao obter access token")
                print("   Verifique suas credenciais do M-Pesa")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar M-Pesa API: {e}")

def test_mpesa_sandbox():
    """Testa especificamente o ambiente sandbox"""
    print("\n🏖️ Testando Ambiente Sandbox")
    print("=" * 30)
    
    with app.app_context():
        mpesa = MpesaAPI()
        
        # Verificar se está usando sandbox
        if mpesa.environment == 'sandbox':
            print("✅ Ambiente sandbox configurado")
            print(f"   Base URL: {mpesa.base_url}")
        else:
            print("⚠️ Ambiente não é sandbox")
            print(f"   Environment: {mpesa.environment}")
            print(f"   Base URL: {mpesa.base_url}")

def show_mpesa_info():
    """Mostra informações sobre o M-Pesa"""
    print("\n📋 Informações M-Pesa")
    print("=" * 25)
    print("🔑 Consumer Key: S50TdhlpQu7zMn48P9Ue74K0koO2CTK6")
    print("🏪 Shortcode: 174379 (Sandbox)")
    print("🌍 Environment: Sandbox")
    print("📱 Para testar, use números de telefone no formato:")
    print("   - 258841234567 (com código do país)")
    print("   - 841234567 (apenas o número)")
    print("   - 0841234567 (com zero inicial)")

def main():
    """Menu principal"""
    while True:
        print("\n📱 TESTE M-PESA")
        print("=" * 20)
        print("1. Testar configuração")
        print("2. Testar ambiente sandbox")
        print("3. Mostrar informações")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == '1':
            test_mpesa_config()
        elif choice == '2':
            test_mpesa_sandbox()
        elif choice == '3':
            show_mpesa_info()
        elif choice == '4':
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    main()
