from flask import Flask, request, jsonify, session
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'muhammad.bscs4428@iiu.edu.pk'
app.config['MAIL_PASSWORD'] = 'Talha@2299'

mail = Mail(app)

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    # Generate random OTP
    otp = random.randint(1000, 9999)
    
    # Store OTP in session for later verification
    session['otp'] = otp
    
    # Send OTP to user's email
    msg = Message('Your OTP Code', sender='muhammad.bscs4428@iiu.edu.pk', recipients=[email])
    msg.body = f'Your OTP code is {otp}.'
    try:
        mail.send(msg)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    entered_otp = data['otp']
    stored_otp = session.get('otp')
    
    if str(entered_otp) == str(stored_otp):
        # OTP is correct
        return jsonify({'success': True})
    else:
        # OTP is incorrect
        return jsonify({'success': False, 'message': 'Invalid OTP'})

if __name__ == '__main__':
    app.run(debug=True)
