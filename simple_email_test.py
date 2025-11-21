# Simple Email Test
from app import app, mail
from flask_mail import Message

def test_simple_email():
    try:
        with app.app_context():
            msg = Message(
                'Test Email - NGL.MZ',
                recipients=['deeppianovibes@gmail.com'],
                body='This is a test email from NGL.MZ. If you receive this, email is working!'
            )
            mail.send(msg)
            print("SUCCESS: Email sent!")
            return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == '__main__':
    test_simple_email()
