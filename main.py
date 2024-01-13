from flask import Flask, render_template, request, session, make_response, redirect
from flask_login import LoginManager
import datetime
from family import Family , Person, Task

app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # change this!!

@app.route("/")
def home():
   if 'username' in session:
    return redirect("/home")
   else:
    return redirect("/login")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/home")
def main_page():
    return render_template("home.html")
    
if __name__ == '__main__':
    app.run(port = 5000, debug = True)
    #task()