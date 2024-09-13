from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import sqlite3 
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'egmpjosh@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'Eclipse0116@'  # Replace with your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


# Serializer to generate unique tokens
s = URLSafeTimedSerializer('ThisIsASecret!')

# Token expiration time (in seconds)
TOKEN_EXPIRATION = 3600  # 1 hour



# Function to validate user credentials and return the role
def validate_user(username, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Replace 'users' with the actual table name in your database
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None





@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index():
    username = request.form['username']
    password = request.form['password']

    user = validate_user(username, password)
    
    if user:
        username, role = user
          # Access 'username' at index 2
        role = user[1]  # Access 'role' at index 4
        if role == 'admin':
            # Add the logic for admin login (e.g., session management, redirect to admin dashboard)
            return render_template('admin.html', username=username, role=role)
        elif role == 'user':
            # Add the logic for user login (e.g., session management, redirect to user dashboard)
            return render_template('user.html', username=username, role=role)
    
    # Add the logic for failed login (e.g., display an error message)
    return "Invalid credentials. Please try again."



@app.route('/admin.html')
def admin_dashboard():

    # Add the logic for the admin dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('admin.html', username=username)

@app.route('/user.html')
def user_dashboard():

    # Add the logic for the user dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('user.html', username=username)

@app.route('/register')
def register():
    return render_template('registeruser.html')

@app.route('/register', methods=['POST'])
def register_submit():

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    # Build the URL with the token
    link = url_for('confirm_email', token=token, _external=True)

    # Send the email with the confirmation link
    msg = Message('Confirm Your Email', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your link to confirm your email is: {link}'
    mail.send(msg)
    
    name = request.form['name']
    age = int(request.form['age'])
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    date_of_birth = request.form['date_of_birth']
    # Convert the date string to a datetime object
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

     # Check if the username or email already exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return redirect(url_for('registration_failed', reason='Username or email already exists'))
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Insert the data into the 'users' table
    cursor.execute("INSERT INTO users (name, email, age, username, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, ?, 'user')",
               (name, email, age, username, password, date_of_birth))

    conn.commit()

    # Generate the token
    token = s.dumps(email, salt='email-confirm')
    # Send confirmation email
    msg = Message('Confirm Your Email', sender='egmpjosh@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = f'Your link to confirm your email is: {link}'
    mail.send(msg)
    
    return 'A confirmation email has been sent to your email address.'+redirect(url_for('success'))




@app.route('/success')
def success():
    

    return render_template('success.html')

@app.route('/registration_failed')
def registration_failed():
    reason = request.args.get('reason', 'Unknown error')
    return render_template('registration_failed.html', reason=reason)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=TOKEN_EXPIRATION)
    except SignatureExpired:
        return '<h1>The token has expired!</h1>'

    # Update the database to mark the email as confirmed
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email_confirmed = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return '<h1>Email confirmed! You can now log in.</h1>'
