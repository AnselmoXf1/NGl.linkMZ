# 🇲🇿 NGL.MZ — Plataforma de Mensagens Anônimas com Pagamentos

**NGL.MZ** é uma aplicação inspirada no conceito do [ng.link](https://ng.link), desenvolvida em **Flask (Python)**.  
Permite que utilizadores criem **links anônimos** para receber mensagens secretas, com a opção de **pagar para revelar** a identidade (IP, navegador e outros dados) de quem enviou.

## 🚀 Funcionalidades

- ✅ Envio de mensagens anônimas (sem login)
- ✅ Criação de perfis únicos com link pessoal (`/u/teu-nome`)
- ✅ Sistema de login e registo de utilizadores
- ✅ Caixa de entrada de mensagens
- ✅ Função "Reveal" (mostrar quem enviou a mensagem — gratuito nesta versão com animação de 10s)
- 💡 Pagamento/integração M-Pesa foi removida da versão inicial (opcional em futuras versões)
- 💾 Base de dados SQLite leve e simples
- 🔒 Sessões seguras e criptografia de senhas

## 🧩 Estrutura do Projeto

```
📂 nglink_mz/
┣ 📜 app.py                 # Aplicação Flask principal
┣ 📜 config.py              # Configurações da aplicação
┣ 📜 requirements.txt       # Dependências Python
┣ 📂 instance/
┃ ┗ mensagens.db           # Base de dados SQLite
┣ 📂 templates/
┃ ┣ base.html             # Template base
┃ ┣ index.html            # Página inicial
┃ ┣ register.html         # Registo de utilizadores
┃ ┣ login.html            # Login
┃ ┣ profile.html          # Perfil do utilizador
┃ ┣ inbox.html            # Caixa de entrada
┃ ┗ payment.html          # Página de pagamento
┣ 📂 static/
┃ ┣ css/
┃ ┃ ┗ style.css          # Estilos CSS
┃ ┗ js/
┃ ┗ script.js            # JavaScript
┣ 📂 utils/
┃ ┣ __init__.py
┃ ┗ helpers.py           # Funções auxiliares
┣ 📂 mpesa/
┃ ┣ __init__.py
┃ ┗ mpesa_api.py         # Integração M-Pesa
┗ 📂 migrations/
┗ init_db.sql            # Inicialização da BD
```

## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <repository-url>
cd nglink_mz
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# NGl.linkMZ

Projeto Flask para envio de mensagens anônimas, geração de QR Code, integração com pagamentos M-Pesa e recuperação de senha por email.

## Funcionalidades
- Cadastro e login de usuários
- Envio e recebimento de mensagens anônimas
- Geração e download de QR Code para perfil
- Integração com M-Pesa para pagamentos
- Recuperação de senha por email
- Painel de usuário com inbox
- Proteção de rotas e autenticação


### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=your-secret-key-here
## Nota: integração de pagamento (M-Pesa) foi removida nesta versão inicial.
## Se quiser reativar, configure as variáveis abaixo (exemplo):
# MPESA_CONSUMER_KEY=your-mpesa-consumer-key
# MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
# MPESA_SHORTCODE=your-shortcode
# MPESA_PASSKEY=your-passkey
# MPESA_ENVIRONMENT=sandbox
```

### 5. Inicializar a Base de Dados
```bash
python app.py
```
A base de dados será criada automaticamente na primeira execução.

### 6. Executar a Aplicação
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🔧 Configuração M-Pesa

### Sandbox (Desenvolvimento)
1. Registe-se no [M-Pesa Developer Portal](https://developer.safaricom.co.ke/)
## Estrutura do Projeto
```
app.py                # App principal Flask
config.py             # Configurações gerais
requirements.txt      # Dependências Python
static/               # Arquivos estáticos (CSS, JS, imagens)
templates/            # Templates HTML (Jinja2)
mpesa/                # Integração M-Pesa
utils/                # Funções auxiliares
migrations/           # Migrações do banco de dados
instance/             # Configurações sensíveis (.env)
```

2. Obtenha as credenciais de sandbox
3. Configure as variáveis de ambiente

### Produção
1. Complete o processo de certificação
2. Obtenha as credenciais de produção
## Instalação
1. Clone o repositório:
	```
	git clone <repo-url>
	cd NGl.linkMZ-main
	```
2. Crie e configure o arquivo `.env` na pasta `instance/` (veja exemplo em `config_example.py`).
3. Instale as dependências:
	```
	pip install -r requirements.txt
	```
4. Execute as migrações do banco de dados:
	```
	flask db upgrade
	```
5. Inicie o servidor:
	```
	python app.py
	```

3. Altere `MPESA_ENVIRONMENT=production`

## 📱 Como Usar

### Para Utilizadores
## Configuração de Email
- Configure as variáveis de email no arquivo `.env` ou `config_email.py`.
- Exemplo de variáveis:
  ```
  MAIL_SERVER=smtp.gmail.com
  MAIL_PORT=587
  MAIL_USE_TLS=True
  MAIL_USERNAME=seu_email@gmail.com
  MAIL_PASSWORD=sua_senha
  ```

1. **Registe-se** na plataforma
2. **Obtenha seu link** pessoal (`/u/seu-nome`)
3. **Compartilhe** o link para receber mensagens
4. **Visualize** mensagens na caixa de entrada
5. **Pague** para revelar a identidade do remetente

### Para Remetentes
## Testes
- Testes automatizados disponíveis em arquivos `test_*.py`.
- Para rodar todos os testes:
  ```
  python -m unittest discover
  ```

1. **Acesse** o link de um utilizador

## Checklist de Produção
- [x] Estrutura Flask
- [x] Geração de QR Code
- [x] Integração M-Pesa (opcional - removida na versão inicial)
- [x] Recuperação de senha
- [x] Autenticação
- [ ] Documentar uso de integrações opcionais (ex: M-Pesa) no README
- [ ] Dockerfile
- [ ] .env.example
- [ ] Proteção CSRF
- [ ] Testes completos

> **Nota:** A funcionalidade de pagamento (M-Pesa) foi removida da versão inicial. O fluxo de "reveal" é gratuito e mostra o remetente após uma animação de espera de 10 segundos. A integração com pagamentos permanece como melhoria opcional.

- Senhas criptografadas com Werkzeug
- Sessões seguras
- Validação de entrada
- Proteção contra CSRF
- Sanitização de dados

## 🚀 Deploy

### Heroku
```bash
# Instalar Heroku CLI
## Melhorias Sugeridas
- Adicionar Dockerfile para deploy
- Criar arquivo `.env.example`
- Implementar proteção CSRF
- Melhorar cobertura de testes
- Documentar endpoints da API
- Adicionar logs e monitoramento

# Criar Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
```
CMD ["gunicorn", "app:app"]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para suporte, entre em contato:
- Email: suporte@ngl.mz
- GitHub Issues: [Criar Issue](https://github.com/username/ngl-mz/issues)

## 🎯 Roadmap

- [ ] Integração com mais métodos de pagamento
- [ ] API REST completa
- [ ] Aplicação móvel
- [ ] Sistema de notificações
- [ ] Analytics e estatísticas
- [ ] Moderação de conteúdo
- [ ] Temas personalizáveis

---

**anselmo dora bistiro gulane**
