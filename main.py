from flask import Flask, render_template, request, session, make_response, redirect
from flask_login import LoginManager
import datetime
from family import Family , Person, Task
import psql_connector

app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # change this!!

email_login = "admin"
password = "admin"


#@app.route("/home")
@app.route("/")
def home():

    if 'username' in session:
        return redirect("/home")
    else:
        return redirect("/login")



@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    test()

    if request.method == 'POST':
        
        if request.form['email'] != email_login or request.form['password'] != password:
            error = 'Invalid, please try again'
        
        else :
            
            return redirect("/home")

    return render_template("login.html")

def test():
    person_id = psql_connector.add_user("te2st3", "tes11asdsat@email.com","test123")
    print(f"{person_id} - {type(person_id)}" )
    print(psql_connector.create_family(person_id))

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/home")
def main_page():
    #if 'username' not in session:
    
    #    return redirect("/login")
    return render_template("home.html")
    
@app.route("/<path:undefined_path>")
def not_found_page(undefined_path):
    return f"Page not found. Link to login - <a href='http://127.0.0.1:5000/login'>[HERE]</a>"








if __name__ == '__main__':
    app.run(port = 5000, debug = True)
    #task()