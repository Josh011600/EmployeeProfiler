from flask import Blueprint 

views = Blueprint('views', __name__)



@views.route('/')
def index_page():
    return render_template('index.html')





@views.route('/index', methods=['POST'])
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



@views.route('/admin.html')
def admin_dashboard():

    # Add the logic for the admin dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('admin.html', username=username)

@views.route('/user.html')
def user_dashboard():

    # Add the logic for the user dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('user.html', username=username)

@views.route('/register')
def register():
    return render_template('registeruser.html')

@views.route('/register', methods=['POST'])
def register_submit():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
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

    return redirect(url_for('success'))

@views.route('/success')
def success():
    

    return render_template('success.html')

@views.route('/registration_failed')
def registration_failed():
    reason = request.args.get('reason', 'Unknown error')
    return render_template('registration_failed.html', reason=reason)