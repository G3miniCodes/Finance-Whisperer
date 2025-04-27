from flask import Flask, render_template, request, redirect, session, url_for, jsonify,send_file
from flask_session import Session
from reccom import generate_recommendations
from reccom import get_user_data
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from ocr import ocr
import os
from datetime import datetime
import sqlite3
import io
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a3f1b4c7d9e8f6a1b2c3d4e5f6789012'

# Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

DATABASE = "user.db"

# 🔹 Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Create tables in SQLite
def create_tables():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income INTEGER NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spending (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

create_tables()  # Ensure tables are created when the app starts

# 🔹 Middleware to check login status
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/signup')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match!")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('signup.html', error="Email already registered!")
        inc = 0
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, email, password, income) VALUES (?, ?, ?, ?)", 
                       (username, email, hashed_password, inc))
        conn.commit()
        conn.close()
        
        return redirect('/signin')

    return render_template('signup.html')


@app.route('/download', methods=['GET'])
def download():
    # Connect to the database
    conn = sqlite3.connect('user.db')
    df = pd.read_sql_query("SELECT * FROM spending", conn)
    conn.close()

    # Create a BytesIO buffer to hold the CSV data
    buffer = io.BytesIO()
    
    # Write the DataFrame to the buffer in CSV format
    df.to_csv(buffer, index=False)
    
    # Seek back to the beginning of the buffer
    buffer.seek(0)

    # Send the file as a download response
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='transactions.csv'
    )


@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session['user_id'] = user["id"]
            session['username'] = user["username"]
            return redirect('/')

        return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    amount = request.form['amount']
    date = request.form['date']
    category = request.form['category']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO spending (user_id, amount, date, category) VALUES (?, ?, ?, ?)",
                   (session['user_id'], amount, date, category))
    conn.commit()
    conn.close()
    return redirect('/analysis')

# UPLOAD_FOLDER = "static/uploads"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_user_financials(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT income FROM users WHERE id = ?", (user_id,))
    income_row = cursor.fetchone()
    total_income = income_row["income"] if income_row and "income" in income_row.keys() else 0.0

    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute("""
        SELECT SUM(amount) AS total_expense FROM spending 
        WHERE user_id = ? AND date LIKE ?
    """, (user_id, f"{current_month}%"))
    expense_row = cursor.fetchone()
    total_expense = expense_row["total_expense"] if expense_row and expense_row["total_expense"] else 0.0

    amount_left = total_income - total_expense
    return total_income, total_expense, amount_left



@app.route("/run-ocr", methods=["POST"])
def run_ocr():
    if "image" not in request.files:
        return redirect("/")
    file = request.files["image"]
    if file.filename == "":
        return redirect("/")

    result = ocr(file)

    # 🟢 Also fetch total_income, total_expense, and amount_left again
    user_id = session['user_id']
    total_income, total_expense, amount_left = get_user_financials(session['user_id'])

    return render_template("analysis.html", 
                           result=result, 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           amount_left=amount_left)


@app.route('/spending_data')
@login_required
def spending_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category, amount, date FROM spending WHERE user_id = ?", (session['user_id'],))
        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return jsonify({"error": "No data found"}), 404

        data = [{"category": row["category"], "amount": row["amount"], "date": row["date"]} for row in rows]
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/monthly')
@login_required
def monthly():
    return render_template('monthly.html')


@app.route('/analysis')
@login_required
def analysis():
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Get Total Income
    cursor.execute("SELECT income FROM users WHERE id = ?", (user_id,))
    total_income, total_expense, amount_left = get_user_financials(session['user_id'])

    return render_template('analysis.html', 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           amount_left=amount_left)


@app.route('/update_income', methods=['POST'])
@login_required
def update_income():
    user_id = session['user_id']
    new_income = request.form.get('income')

    if not new_income:
        return jsonify({"status": "error", "message": "Invalid income value"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET income = ? WHERE id = ?", (new_income, user_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "total_income": new_income})



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signup')

@app.route('/rec', methods=['GET'])
def rec():
    user_spending = get_user_data()
    recc = generate_recommendations(user_spending)
    print(recc)
    recommendations = [recc]
    print(len(recc))
    return render_template('rec.html', recommendations=recc)

if __name__ == '__main__':
    app.run(debug=True)
