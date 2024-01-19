from flask import Flask, render_template, request, session, url_for, make_response, redirect, g
from flask_login import LoginManager
import datetime
from family import Family , Person, Task
import psql_connector #as conn
import helper

app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)

app.secret_key = helper.get_key_to_session()
url = None
email_login = "admin"
password = "admin"
is_head_member = False

#@app.route("/home")
@app.route("/")
def home():

    if 'email' in session:
        return redirect("/home")
    else:
        return redirect("/login")



@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    #test()

    if request.method == 'POST':
        
        if request.form['email'] != email_login or request.form['password'] != password:
            error = 'Invalid, please try again'
        else:
            session['email'] = request.form['email']
            return redirect(url_for('home'))

    return render_template("login.html")

@app.route("/profile/<email>")
def profile(email):
    """
    See profile, family members, your info
    """
    return email

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
    
    task_id1 = psql_connector.create_task(name = "Walk Yumi",date ="2024-01-17",start_time = "00:00:00", end_time = "11:11:11", family_id = family_id)
    task_id2 = psql_connector.create_task(name = "Walk Yumi",date = "2024-01-17",start_time = "11:11:11", end_time = "22:22:22", family_id = family_id)
    psql_connector.assign_task_to_user(task_id1, person_id)
    psql_connector.assign_task_to_user(task_id2, person_id3)
    psql_connector.change_task_complete(task_id2, True)
    psql_connector.unassign_task(task_id1)

    i = psql_connector.get_user_info("....")
    print("\n\n", i)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")
"""
@app.route("/home")
def main_page():
    #if 'username' not in session:
    
    #    return redirect("/login")
    Your_Task_Dict1 = {"Task" : "walk da dog", "Date": "12 Oct 12:00"}
    Your_Task_Dict2 = {"Task" : "wash da dog", "Date": "13 Oct 11:00"}
    Upcomming_Task_Dict = {"Name": "Maya", "Date": "13 Oct 13:00", "Task": "Feed the dog"}
    Available_Task_Dict = {}
    Your_Task_Dict_List=[Your_Task_Dict1, Your_Task_Dict2]
    Upcomming_Task_Dict_List = [Upcomming_Task_Dict]
    Available_Task_Dict_List = [Available_Task_Dict]
    #^ tester code
    # in final code :
    # Get the Your Task Dict List, Upcomming Task Dict List etc
    # Available Task Dict: Task, Date, Button Identifier - a way to update
    return render_template("home.html",  your_tasks = Your_Task_Dict_List, upcoming_tasks = Upcomming_Task_Dict_List, available_tasks= Available_Task_Dict_List)
"""
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(port = 2010, debug = True)
    #task()