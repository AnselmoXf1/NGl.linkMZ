from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, has_request_context, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message as MailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import hashlib
import uuid
from utils.helpers import get_client_info, generate_unique_link
from mpesa.mpesa_api import MpesaAPI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'deeppianovibes@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'hrgffnyfycnmqamo')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'NGL.MZ <deeppianovibes@gmail.com>')

# M-Pesa Configuration
app.config['MPESA_CONSUMER_KEY'] = os.environ.get('MPESA_CONSUMER_KEY', 'IVOXC05UfvGT3r5MRvX2E4chl3NW30AuY0iCqxf47WAgS6rq')
app.config['MPESA_CONSUMER_SECRET'] = os.environ.get('MPESA_CONSUMER_SECRET', 'AAtRszL0hP5TrWIT5B7jo55ltCbP4vSwRIsYv1HpC6qeQAfMfQuIfstGJc3GoN9i')
app.config['MPESA_SHORTCODE'] = os.environ.get('MPESA_SHORTCODE', '174379')
app.config['MPESA_PASSKEY'] = os.environ.get('MPESA_PASSKEY', 'COLOCA_AQUI_TUA_PASSKEY_DO_LNMO')
app.config['MPESA_ENVIRONMENT'] = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_ip = db.Column(db.String(45), nullable=True)
    sender_browser = db.Column(db.String(200), nullable=True)
    sender_location = db.Column(db.String(200), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_revealed = db.Column(db.Boolean, default=False)
    reveal_payment_id = db.Column(db.String(100), nullable=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='MZN')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    mpesa_receipt = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=True)

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='password_reset_tokens')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('my_profile'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = str(uuid.uuid4())
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # Invalidate any existing tokens for this user
            PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({'used': True})
            
            # Create new token
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            # Send email
            try:
                send_password_reset_email(user.email, token)
                flash('Email de recuperação enviado! Verifique sua caixa de entrada.', 'success')
            except Exception as e:
                flash('Erro ao enviar email. Tente novamente mais tarde.', 'error')
                print(f"Email error: {e}")
        else:
            # Don't reveal if email exists or not for security
            flash('Se o email existir, você receberá um link de recuperação.', 'info')
        
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Find valid token
    reset_token = PasswordResetToken.query.filter_by(
        token=token, 
        used=False
    ).first()
    
    if not reset_token or reset_token.expires_at < datetime.utcnow():
        flash('Link inválido ou expirado. Solicite um novo link.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres!', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update password
        user = User.query.get(reset_token.user_id)
        user.password_hash = generate_password_hash(password)
        
        # Mark token as used
        reset_token.used = True
        
        db.session.commit()
        
        flash('Senha alterada com sucesso! Faça login com sua nova senha.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

def send_password_reset_email(email, token):
    """Send password reset email"""
    # Build reset URL. In tests we may not have a request context, so fall back to
    # a configured BASE_URL or localhost.
    if has_request_context():
        base = request.url_root
    else:
        base = current_app.config.get('BASE_URL', 'http://localhost:5000/')

    reset_url = base.rstrip('/') + f"/reset-password/{token}"

    msg = MailMessage(
        'NGL.MZ - Recuperação de Senha',
        recipients=[email],
        html=f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">🔐 NGL.MZ</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px;">Recuperação de Senha</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 20px;">
                <h2 style="color: #333; margin-top: 0;">Olá!</h2>
                <p style="color: #666; line-height: 1.6;">
                    Você solicitou a recuperação de senha para sua conta NGL.MZ.
                </p>
                <p style="color: #666; line-height: 1.6;">
                    Clique no botão abaixo para definir uma nova senha:
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                        🔑 Redefinir Senha
                    </a>
                </div>
                
                <p style="color: #999; font-size: 14px; margin-top: 30px;">
                    Este link expira em 1 hora por motivos de segurança.
                </p>
                
                <p style="color: #999; font-size: 14px;">
                    Se você não solicitou esta recuperação, ignore este email.
                </p>
            </div>
            
            <div style="text-align: center; color: #999; font-size: 12px;">
                <p>© 2024 NGL.MZ - Plataforma de Mensagens Anônimas</p>
                <p>Anselmo Dora Bistiro Gulane</p>
            </div>
        </body>
        </html>
        """
    )
    
    # mail.send requires an application context; ensure we're in one (tests call this
    # function under app.app_context()).
    mail.send(msg)

@app.route('/u/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    # SEMPRE mostrar apenas formulário de mensagem anônima para visitantes
    # O perfil completo só é acessado através de rota específica
    return render_template('anonymous_message.html', user=user)

@app.route('/profile')
def my_profile():
    """Rota para o perfil do usuário logado"""
    if 'user_id' not in session:
        flash('Please login to view your profile.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/image-generator')
def image_generator():
    """Página para gerar imagens personalizadas para status"""
    if 'user_id' not in session:
        flash('Please login to generate images.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('image_generator.html', user=user)

@app.route('/send_message/<username>', methods=['POST'])
def send_message(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    content = request.form.get('message')
    if not content:
        return jsonify({'error': 'Message content is required'}), 400
    
    # Get client information
    client_info = get_client_info(request)
    
    # Create message
    message = Message(
        content=content,
        sender_ip=client_info['ip'],
        sender_browser=client_info['browser'],
        sender_location=client_info['location'],
        user_id=user.id
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': 'Message sent successfully!'})

@app.route('/inbox')
def inbox():
    if 'user_id' not in session:
        flash('Please login to view your inbox.', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    messages = Message.query.filter_by(user_id=user.id).order_by(Message.created_at.desc()).all()
    
    return render_template('inbox.html', messages=messages)

@app.route('/reveal_message/<int:message_id>')
def reveal_message(message_id):
    if 'user_id' not in session:
        flash('Please login to reveal messages.', 'error')
        return redirect(url_for('login'))
    
    message = Message.query.get_or_404(message_id)
    
    # Check if user owns this message
    if message.user_id != session['user_id']:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('inbox'))
    
    if message.is_revealed:
        flash('Message already revealed!', 'info')
        return redirect(url_for('inbox'))
    
    return render_template('payment.html', message=message)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    message_id = request.form.get('message_id')
    phone_number = request.form.get('phone_number')
    amount = 50.0  # Fixed amount for reveal
    
    message = Message.query.get_or_404(message_id)
    
    # Create payment record
    payment = Payment(
        amount=amount,
        phone_number=phone_number,
        user_id=session['user_id'],
        message_id=message_id
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Initialize M-Pesa API
    mpesa = MpesaAPI()
    
    # Process payment
    result = mpesa.stk_push(phone_number, amount, f"Reveal message {message_id}")
    
    if result['success']:
        payment.mpesa_receipt = result['receipt']
        payment.status = 'completed'
        message.is_revealed = True
        message.reveal_payment_id = result['receipt']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment processed successfully!',
            'receipt': result['receipt']
        })
    else:
        payment.status = 'failed'
        db.session.commit()
        
        return jsonify({
            'success': False,
            'error': result['error']
        })

@app.route('/api/messages/<username>')
def api_messages(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    messages = Message.query.filter_by(user_id=user.id).order_by(Message.created_at.desc()).limit(10).all()
    
    result = []
    for msg in messages:
        result.append({
            'id': msg.id,
            'content': msg.content,
            'created_at': msg.created_at.isoformat(),
            'is_revealed': msg.is_revealed,
            'sender_info': {
                'ip': msg.sender_ip if msg.is_revealed else 'Hidden',
                'browser': msg.sender_browser if msg.is_revealed else 'Hidden',
                'location': msg.sender_location if msg.is_revealed else 'Hidden'
            }
        })
    
    return jsonify(result)

@app.route('/api/message/<int:message_id>')
def api_message(message_id):
    """API para buscar dados de uma mensagem específica"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    message = Message.query.get_or_404(message_id)
    
    # Check if user owns this message
    if message.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify({
        'success': True,
        'message': {
            'id': message.id,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'is_revealed': message.is_revealed,
            'sender_info': {
                'ip': message.sender_ip if message.is_revealed else 'Hidden',
                'browser': message.sender_browser if message.is_revealed else 'Hidden',
                'location': message.sender_location if message.is_revealed else 'Hidden'
            }
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
