from flask import Flask, render_template, request, session, make_response, redirect
from flask_login import LoginManager
import datetime
from family import Family 

app = Flask(__name__)
login_manager = LoginManager()

isSignedIn = True # later will be some cookie thing

@app.route("/")
def home():
   if isSignedIn:
    path = request.args
    print(path)
    return render_template("home.html")
   else:
    return redirect("/login")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    return render_template("login.html")

def test():
    


if __name__ == '__main__':
    #app.run(port = 5000, debug = True)
    test()