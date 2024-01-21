from flask import Flask, render_template, request, session, url_for, make_response, redirect, g
from flask_login import LoginManager
import datetime
from family import Family , Person, Task
import psql_connector #as conn
import helper

app = Flask(__name__)

app.secret_key = helper.get_key_to_session()
URL = None



@app.before_request
def before_request():
    # Check if the user is logged in and fetch user info
    if 'person_id' not in session and request.endpoint != 'login':
        print("\nSession items: ", session, "\n")
        return redirect("/login")
    
    if request.endpoint == 'login' or request.endpoint == 'signup':
        if 'person_id' in session:
            return redirect(url_for('home'))



@app.route("/home")
@app.route("/")
def home():
    if 'person_id' not in session:
        return redirect(url_for('/login'))
    
    #retrieve general information
    person = helper.get_user_info(session['person_id'])

    if 'family_id' not in session:
        family_id = helper.find_family_by_person_id(person.person_id)
        members = helper.get_family_info(family_id)
        add_info_to_session(members, person.person_id)
    else:
        family_id = session['family_id']
        members = session['members']

    is_head_member = session['is_head_member'] 
    
    result = helper.get_family_tasks(family_id=family_id, person_id=person.person_id)
    your_tasks, upcoming_tasks, available_tasks = result[0], result[1], result[2]
    
    return render_template("home.html", person = person, your_tasks = your_tasks,upcoming_tasks = upcoming_tasks,available_tasks = available_tasks)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        test()
        person_id, error = helper.validate_user(request.form['email'].lower(), request.form['password'])
        if error is None:
            session['person_id'] = person_id
            return redirect(url_for('home'))

    return render_template("login.html", error = error)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/profile/<email>")
def profile(email):
    """
    See profile, family members, your info
    """
    return email

@app.route('/logout')
def logout():
    """
    Remove the user from the session
    """
    session.pop('family_id', None)
    session.pop('person_id', None)
    session.pop('members', None)
    session.pop('is_head_member', None)
    return redirect(url_for('login'))

def test():
    person_id = psql_connector.add_user("Test person","test@example.com","test")

    family_id = 1
    psql_connector.add_user_to_family(person_id, family_id)
    
    
    task_id1 = psql_connector.create_task(name = "Walk Yumi",date ="2024-01-17",start_time = "00:00:00", end_time = "10:10:11", family_id = family_id)
    task_id2 = psql_connector.create_task(name = "Walk Yumid sadsadasdasdasd",date = "2024-01-17",start_time = "11:11:11", end_time = "22:22:22", family_id = family_id)
    task_id3 = psql_connector.create_task(name = "Walk Yumi, walk YYYYYYYYYYYUMASDA",date = "2024-01-17",start_time = "12:11:11", end_time = "22:22:22", family_id = family_id)
    task_id4 = psql_connector.create_task(name = "Walk Yumi aSDsadas ",date = "2024-01-17",start_time = "1:11:11", end_time = "22:22:22", family_id = family_id)
    task_id5 = psql_connector.create_task(name = "Walk Yumi asdasdasdasdas ",date = "2024-01-17",start_time = "17:11:11", end_time = "23:22:22", family_id = family_id)
    psql_connector.assign_task_to_user(task_id1, 1)
    psql_connector.assign_task_to_user(task_id2, person_id)
    psql_connector.assign_task_to_user(task_id3, 1)
    psql_connector.assign_task_to_user(task_id4, 1)
    
    psql_connector.change_task_complete(task_id2, True)
    #psql_connector.unassign_task(task_id1)


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


#@app.errorhandler(Exception)
#def handle_exception(error):
    return f"""It seems like something wrong happened.\n{error}"""


def add_info_to_session(members, person_id):
    if(person_id == members[0]):
        session['is_head_member'] = True

    session['members'] = members

if __name__ == '__main__':
    app.run(port = 2010, debug = True)
    #task()