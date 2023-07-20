from flask import Flask, render_template, request
from twilio.rest import Client
import random
import sqlite3
import os

account_sid = os.environ.get('AC72e5e3ed30b51af85e21766d93c8377a')
auth_token = os.environ.get('c5013c70815ed3b889bbbb94b1356d59')
twilio_phone_number = os.environ.get('09610970818')

app = Flask(__name__)

# Twilio API credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'

# Function to send SMS
def send_sms(to_phone_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )
    return message.sid

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    # Retrieve the phone number from the HTML form
    to_phone_number = request.form['phone_number']

    # Generate a random 6-digit authentication code
    authentication_code = str(random.randint(100000, 999999))

    # Compose the SMS message
    sms_message = f'Your verification code is: {authentication_code}'

    # Send the SMS
    send_sms(to_phone_number, sms_message)

    return 'Verification code sent successfully.'

if __name__ == '__main__':
    app.run(debug=True)




