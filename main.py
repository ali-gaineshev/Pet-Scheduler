from flask import Flask, render_template, request, session, url_for, make_response, redirect, g
from datetime import datetime, timedelta
from family import Family , Person, Task
import helper

app = Flask(__name__)

app.secret_key = helper.get_key_to_session()
URL = "http://64.23.162.130/"



@app.before_request
def before_request():
    # Check if the user is logged in and fetch user info
    if 'person' not in session and (request.endpoint == '' or request.endpoint == 'home' or request.endpoint == 'profile'):
        return redirect(url_for("login"))
    
    if request.endpoint == 'login' or request.endpoint == 'signup':
        if 'person' in session:
            return redirect(url_for('home'))



@app.route("/home")
@app.route("/", methods = ['GET', 'POST'])
def home():
    if 'person' not in session:
        return redirect(url_for('login'))
    
    person = helper.from_json(session['person'])

    #retrieve general information
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

    #some for future
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
            request_password = 'admin123'
        else:
            request_email = request.form['email'].lower()
            request_password = request.form['password']
        person, error = helper.get_user_info(request_email, request_password, None)

        if error is None:
            session["person"] = helper.to_json(person)
            return redirect(url_for('home'))

    return render_template("login.html", error = error)


@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    """
    See profile, family members, your info
    """
    person = helper.from_json(session['person'])
    if('family_id' not in session):
        family_id = helper.find_family_by_person_id(person.person_id)
    else:
        family_id = session['family_id']

    if(request.method == 'POST'):
        error = sign_up_user(family_id=family_id)
        return make_response(render_template('profile.html', person = person, error_message = error))


    if(request.args.get('task_date') and request.args.get('task_start_time') and request.args.get('task_end_time')):
        name = request.args.get('task_name_input')
        date = request.args.get('task_date')
        start_time = request.args.get('task_start_time')
        end_time = request.args.get('task_end_time')
        repeat = request.args.get('repeat_7_days')

        error = helper.is_valid_date(date, start_time, end_time)
    
        if(error is None): #not error
            if(len(name) >= 0 and len(name) <= 3):
                error = "The name of the task is too short"

            elif(len(name) > 30):
                error = "Please make the name shorter"

        range_value = 4 if repeat else 1
        
        if(error is None):
            for i in range(range_value):#4times
                date_to_give = datetime.strptime(date, "%Y-%m-%d") + timedelta(i * 7)
                task = Task(name, date_to_give, start_time, end_time)
                task_id, error = helper.create_new_task(task, family_id)   
                

        response = make_response(render_template('profile.html', person = person, error_message = error))

        expires = datetime.now() + timedelta(days=365)
        response.set_cookie('task_date', date, expires=expires, samesite = 'None')
        response.set_cookie('task_start_time', start_time, expires=expires, samesite = 'None')
        response.set_cookie('task_end_time', end_time, expires=expires, samesite = 'None')
        
        
        return response
    
    return render_template('profile.html', person = person)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    error = None
    if(request.method == 'POST'):
        error = sign_up_user(family_id=None)
    
    return render_template("signup.html", error_message = error)

def sign_up_user(family_id = None):
    needed = ["new_email_input", "new_password_input", "new_name_input" ]
    error = None
    if(all(el in needed for el in request.form )):
        error = helper.sign_up_user(request.form["new_email_input"], request.form['new_password_input'], 
                            request.form['new_name_input'],family_id=family_id)
    return error

@app.route('/logout')
def logout():
    """
    Remove the user from the session
    """
    
    session.pop('family_id', None)
    session.pop('person', None)
    session.pop('members', None)
    session.pop('is_head_member', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


#@app.errorhandler(Exception)
#def handle_exception(error):
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
    app.run(port = 5000, debug = True)
    #task()


