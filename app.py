from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key of your choice

# Load environment variables
load_dotenv()

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Pressure Washing Solutions', os.getenv('MAIL_USERNAME'))

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            msg = Message(subject=f"Message from {name}",
                          recipients=['your-email@gmail.com'])  # Replace with your actual inbox
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            
            mail.send(msg)
            flash('Message sent successfully!', 'success')
            return redirect('/contact')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect('/contact')
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
