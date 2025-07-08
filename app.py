
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
users = {}  # this is like a notebook storing users
# This will load users from users.txt when app starts
def load_users():
    try:
        with open("users.txt", "r") as file:
            for line in file:

                if line.strip() == "":
                    continue
                email, password = line.strip().split(",")
                users[email] = password
        print("Users loaded from file:", users)        
    except FileNotFoundError:
        # If file doesn't exist yet, skip it
        pass
load_users()
@app.route('/')
def home():
    return '''
    <h2>Welcome!</h2>
    <a href="/signup"><button>Sign Up</button></a>
    <a href="/login"><button>Log In</button></a>
'''
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users[email] = password
        with open("users.txt", "a") as file:
            file.write(f"{email},{password}\n")
        print("All users:", users)

        return  f"user {email} Signup Successfu! Go to <a href='/login'>login"
    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if users.get(email) == password:
            return f"Welcome back, {email}!"
        else:
            return "Wrong email or password"
    return render_template("login.html")
@app.route("/admin")
def admin():
    try:
        with open("users.txt", "r") as f:
            lines = f.readlines()
            users = [line.split(',')[0] for line in lines]  # show only email
    except FileNotFoundError:
        users = []

    return render_template("admin.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
