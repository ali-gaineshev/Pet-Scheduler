from flask import Flask, render_template, request, session, url_for, make_response, redirect, g
import datetime
from family import Family , Person, Task
import helper

app = Flask(__name__)

app.secret_key = helper.get_key_to_session()
URL = "http://64.23.162.130/"



@app.before_request
def before_request():
    # Check if the user is logged in and fetch user info
    if 'person_id' not in session and request.endpoint != 'login' and request.endpoint != 'signup':
        return redirect("/login")
    
    if request.endpoint == 'login' or request.endpoint == 'signup':
        if 'person_id' in session:
            return redirect(url_for('home'))



@app.route("/home")
@app.route("/", methods = ['GET', 'POST'])
def home():
    if 'person_id' not in session:
        return redirect(url_for('/login'))
    

    #retrieve general information
    person = helper.get_user_info(session['person_id'])

    if request.method == 'POST':
        if('take_task_button' in request.form):
            taken_task_id = request.form['take_task_button']
            helper.assign_task(taken_task_id, person.person_id) 

        if('complete_task_btn' in request.form):
            complete_task_id = request.form['complete_task_btn']
            helper.change_task_complete(complete_task_id, True)

        if('unassign_task_btn' in request.form):
            unassign_task_id = request.form['unassign_task_btn']
            helper.unassign_task(unassign_task_id)


    family_id, members,is_head_member = get_session_info(person)

    result = helper.get_family_tasks(family_id=family_id, person_id=person.person_id)
    your_tasks, upcoming_tasks, available_tasks = result[0], result[1], result[2]
    
    return render_template("home.html", person = person, your_tasks = your_tasks,upcoming_tasks = upcoming_tasks,available_tasks = available_tasks)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #test()
        if 'test_button' in request.form:
            request_email = 'admin'
            request_password = 'test123'
        else:
            request_email = request.form['email'].lower()
            request_password = request.form['password']
        person_id, error = helper.validate_user(request_email, request_password)
        if error is None:
            session['person_id'] = person_id
            return redirect(url_for('home'))

    return render_template("login.html", error = error)


@app.route("/profile")
def profile():
    """
    See profile, family members, your info
    """
    person = helper.get_user_info(session['person_id'])

    #if request.method == 'POST':
                

    return render_template('profile.html', person = person)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")


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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(Exception)
def handle_exception(error):
    return f"""It seems like something wrong happened.\n{error}"""


def get_session_info(person):
    if 'family_id' not in session:
        family_id = helper.find_family_by_person_id(person.person_id)
        members = helper.get_family_info(family_id)
        add_info_to_session(members, person.person_id)
    else:
        family_id = session['family_id']
        members = session['members']

    is_head_member = session['is_head_member'] 
    return family_id, members,is_head_member

def add_info_to_session(members, person_id):
    session['is_head_member'] = True if person_id == members[0] else False
    session['members'] = members

if __name__ == '__main__':
    app.run(port = 5000)
    #task()
