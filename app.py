from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


# Function to validate user credentials and return the role

def validate_user(username_or_email, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Check if the input is an email or username
    if '@' in username_or_email:  # Assuming email addresses have '@'
        query = "SELECT username, usertype FROM employees WHERE email=? AND password=?"
    else:
        query = "SELECT username, usertype FROM employees WHERE username=? AND password=?"

    cursor.execute(query, (username_or_email, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None





def getEmployees():
  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM employees')
  employees = cursor.fetchall()
  conn.close()
  return employees







def getName():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM employees')
    name = cursor.fetchall()
    conn.close()
    return name[0] if name else None



@app.route('/index', methods=['POST'])
def index():
    
    username = request.form['username']
    password = request.form['password']

    user = validate_user(username, password)
    
    if user:
        username, usertype = user
          # Access 'username' at index 2
        
    if usertype == 'admin':
            user_id = username, password
            employees = getEmployees()
           
            if user_id:
                return render_template('admin.html', username=username, usertype=usertype, employees=employees)
    elif usertype == 'employee':
             return render_template('user.html', username=username, usertype=usertype)
    
    return render_template('index.html', login_failed=True)


@app.route('/register')
def register():
    return render_template('registeruser.html')

@app.route('/register', methods=['POST'])
def register_submit():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    name = request.form['name']
    age = int(request.form['age'])
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    dateOfBirth = request.form['date_of_birth']
    # Convert the date string to a datetime object
    dateOfBirth = datetime.strptime(dateOfBirth, '%Y-%d-%m').date()

     # Check if the username or email already exists in the database
    cursor.execute("SELECT * FROM employees WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return redirect(url_for('registration_failed', reason='Username or email already exists'))
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Insert the data into the 'users' table
    cursor.execute("INSERT INTO employees (name, age, email, username, password, dateOfBirth, usertype) VALUES (?, ?, ?, ?, ?, ?, 'employee')",
               (name, age, email, username, password, dateOfBirth))

    conn.commit()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    

    return render_template('success.html')

@app.route('/registration_failed')
def registration_failed():
    reason = request.args.get('reason', 'Unknown error')
    return render_template('registration_failed.html', reason=reason)


#for logout purposes
@app.route('/')
def index_page():
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)