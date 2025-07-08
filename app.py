from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to your MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12788903",
        password="28L4t89b5c",  # <-- PUT YOUR PASSWORD HERE
        database="sql12788903"
    )

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        cursor.close()
        conn.close()

        return f"User {email} signed up successfully! Go to /login"
    return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return f"Welcome back, {email}!"
        else:
            return "Invalid email or password."

    return render_template("login.html")

# Admin route to view all users
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users")
    users = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return render_template("admin.html", users=users)
@app.route("/")
def home():
    return "Welcome! Go to /signup, /login, or /admin"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
    
