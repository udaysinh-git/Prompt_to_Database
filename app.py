from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        root_password = request.form.get('root_password')
        # For demo, assume any non-empty password is accepted.
        if root_password:
            session['root_password'] = root_password
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard showing two options
@app.route('/dashboard')
def dashboard():
    if 'root_password' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# View all databases route
@app.route('/view_databases')
def view_databases():
    if 'root_password' not in session:
        return redirect(url_for('login'))
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=session['root_password']
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
    except Exception as e:
        databases = []
    return render_template('view_databases.html', databases=databases)

# Create database route
@app.route('/create_database', methods=['GET', 'POST'])
def create_database():
    if 'root_password' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        example_schema = request.form.get('example_schema')
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=session['root_password']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name};")
            conn.commit()
        except Exception as e:
            pass
        return redirect(url_for('dashboard'))
    return render_template('create_database.html')

if __name__ == '__main__':
    app.run(debug=True)