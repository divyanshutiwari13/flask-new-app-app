from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change to a secure key in production

# Dummy user database
users = {}

@app.route("/")
def home():
    return redirect(url_for("signup"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not all([first_name, last_name, email, password, confirm_password]):
            flash("All fields are required!", "error")
        elif password != confirm_password:
            flash("Passwords do not match!", "error")
        elif email in users:
            flash("Email already registered!", "error")
        else:
            users[email] = {"first_name": first_name, "last_name": last_name, "password": password}
            flash("You have successfully signed up!", "success")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.get(email)
        if user and user["password"] == password:
            flash("You have successfully logged in!", "success")
            return redirect(url_for("signup"))
        else:
            flash("Invalid email or password!", "error")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    name = request.args.get("name", "User")
    return render_template("dashboard.html", name=name)


if __name__ == "__main__":
    app.run()

