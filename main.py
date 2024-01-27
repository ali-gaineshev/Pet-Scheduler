from flask import Flask, render_template, request, session, url_for, make_response, redirect
from datetime import datetime, timedelta
from family import Family , Person, Task
import helper

app = Flask(__name__)

app.secret_key = helper.get_key_to_session()
URL = "http://64.23.162.130/"


@app.before_request
def before_request():
    """
    Process this before each requiest. 
    """
    # Check if the user is logged in and fetch user info
    if 'person' not in session and (request.endpoint == '' or request.endpoint == 'home' or request.endpoint == 'profile'):
        return redirect(url_for("login"))
    
    if request.endpoint == 'login' or request.endpoint == 'signup':
        if 'person' in session:#don't let user go to login/signup
            return redirect(url_for('home'))



@app.route("/home")
@app.route("/", methods = ['GET', 'POST'])
def home():
    """
    Main home page of the website
    """
    if 'person' not in session:#extra check if @before_request fails
        return redirect(url_for('login'))
    
    person: Person = helper.from_json(session['person'])#guaranteed to be in the session

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

    #some are saved for future
    family_id, members,is_head_member = get_session_info(person)

    #Retrieve tasks
    result = helper.get_family_tasks(family_id=family_id, person_id=person.person_id)
    your_tasks, upcoming_tasks, available_tasks = result[0], result[1], result[2]
    
    return render_template("home.html", person = person, your_tasks = your_tasks,
                           upcoming_tasks = upcoming_tasks,available_tasks = available_tasks)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    """ 
    Page for users to log in. Test login is available. Redirect to home if login is successfull
    """
    error = None
    if request.method == 'POST':
        
        #login with test account
        if 'test_button' in request.form:
            request_email = 'admin'
            request_password = 'admin123'
        else:
            request_email = request.form['email'].lower()
            request_password = request.form['password']
        person, error = helper.get_user_info(request_email, request_password, None)

        if error is None:
            session["person"] = helper.to_json(person)#save json dict to session, since class instances are not allow
            return redirect(url_for('home'))

    return render_template("login.html", error = error)


@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    """
    See profile, family members, your info
    """

    person: Person = helper.from_json(session['person'])
    if('family_id' not in session):
        family_id = helper.find_family_by_person_id(person.person_id)
    else:
        family_id = session['family_id']

    if(request.method == 'POST'):
        error = sign_up_user(family_id=family_id)
        return make_response(render_template('profile.html', person = person, error_message = error))


    if(request.args.get('task_date') and request.args.get('task_start_time') and request.args.get('task_end_time')):
        name: str = request.args.get('task_name_input')
        date: str = request.args.get('task_date')
        start_time: str = request.args.get('task_start_time')
        end_time: str = request.args.get('task_end_time')
        repeat: str = request.args.get('repeat_7_days')

        error: any = helper.is_valid_date(date, start_time, end_time)
    
        if(error is None): #no error, just check if name is correct
            if(len(name) >= 0 and len(name) <= 3):
                error = "The name of the task is too short"

            elif(len(name) > 30):
                error = "Please make the name shorter"

        range_value = 4 if repeat else 1 #repeat every 7 days if checkbox is marked
        
        if(error is None):
            for i in range(range_value):#4times if checkbox is marked, otherwise only once
                date_to_give = datetime.strptime(date, "%Y-%m-%d") + timedelta(i * 7)
                task = Task(name, date_to_give, start_time, end_time)
                task_id, error = helper.create_new_task(task, family_id)   
                

        response = make_response(render_template('profile.html', person = person, error_message = error))

        #cookies
        expires = datetime.now() + timedelta(days=1)
        response.set_cookie('task_date', date, expires=expires, samesite = 'None')
        response.set_cookie('task_start_time', start_time, expires=expires, samesite = 'None')
        response.set_cookie('task_end_time', end_time, expires=expires, samesite = 'None')
        
        
        return response
    
    return render_template('profile.html', person = person)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    """ 
    Sign up page for user
    """
    error = None
    if(request.method == 'POST'):
        error = sign_up_user(family_id=None)
    
    return render_template("signup.html", error_message = error)

def sign_up_user(family_id = None):
    """ 
    sign up function, which actually does all of the work. Reads info from <input>
    if family_id is None then creates new family
        otherwise adds a new member to a family
    """
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


@app.errorhandler(Exception)
def handle_exception(error):
    return f"""It seems like something wrong happened.\n{error}"""


def get_session_info(person: Person):
    """Gets additional information about family from person!

    Args:
        person (Person): person that is in the session

    Returns:
        family_id: int
        members: list[Person] - list of members
        is_head_member: bool
    """
    family_id:int
    members: list[Person]
    if 'family_id' not in session:
        family_id = helper.find_family_by_person_id(person.person_id)
        members = helper.get_family_info(family_id)
        session['members'] = members
    else:
        family_id = session['family_id']
        members = session['members']

    is_head_member: bool = True if person.person_id == members[0] else False
    return family_id, members,is_head_member


if __name__ == '__main__':
    app.run(port = 5000)


