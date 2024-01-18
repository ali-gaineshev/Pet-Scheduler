from flask import Flask, render_template, request, session, make_response, redirect, g
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
    person_id = psql_connector.add_user("head","test1","test")
    family_id = psql_connector.create_family(person_id)
    person_id1 = psql_connector.add_user("p1","test2","test")
    person_id2 = psql_connector.add_user("p2","test3","test")
    person_id3 = psql_connector.add_user("p3","test4","test")

    psql_connector.add_user_to_family(person_id1, family_id)
    psql_connector.add_user_to_family(person_id2, family_id)
    psql_connector.add_user_to_family(person_id3, family_id)

    head_member_id, member_ids = psql_connector.get_family_info(family_id)
    
    psql_connector.create_task(name = "Walk Yumi",date ="2024-01-17",start_time = 00:00:00, end_time = 11:11:11, family_id = family_id)
    psql_connector.create_task(name = "Walk Yumi",date = "2024-01-17",start_time = 11:11:11, end_time = 22:22:22, family_id = family_id)

    print("\nHEAD: ", head_member_id)
    print(member_ids,"\n")

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