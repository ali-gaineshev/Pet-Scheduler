from family import Family, Task, Person
import psql_connector as conn
from datetime import datetime
import re

key_path = "./secret/session_secret.txt"
def get_key_to_session():
    key = ""
    with open(key_path) as f:
        key = f.readline()
    return key

def to_json(person: Person):
    json_dict = vars(person)
    json_dict.pop('password')
    return json_dict

def from_json(json_dict: dict):
    return Person(json_dict['person_id'], json_dict['name'], json_dict['email'])

def get_user_info(email = None, password = None, person_id = None):
    error = None
    if person_id is None: #login as email
        user_info = conn.get_user_info(email=email)
        
        if(user_info is None or password != user_info[3]):
            error = "Incorrect email/password or no such user found"
            return None, error
    else:
        user_info = conn.get_user_info(email=None, person_id=person_id)
        if(user_info is None):
            error = "Something went wrong"
            return None, error

    return Person(user_info[0], user_info[1], user_info[2], user_info[3]), error
    
def find_family_by_person_id(person_id):

    family_id = conn.find_family_by_person_id(person_id = person_id)
    return family_id

def get_family_info(family_id):
    """ member_ids is a list of tuples of single element (id)

    Args:
        family_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    head_member_id, member_ids = conn.get_family_info(family_id=family_id)
    members = [head_member_id]
    for member_tuple in member_ids:
        member_id = member_tuple[0]
        if(head_member_id != member_id):
            members.append(member_id)
    return members

def assign_task(task_id, person_id):
    conn.assign_task_to_user(task_id, person_id)

def unassign_task(task_id):
    conn.unassign_task(task_id)

def change_task_complete(task_id, complete):
    conn.change_task_complete(task_id,complete)

def create_new_task(task: Task, family_id):
    """

    Args:
        family_id (_type_): _description_
    """
    error = None
    task_id = conn.create_task(task.name, task.date, task.start_time, task.end_time, family_id)
    if task_id is None:
        error = "Error with creating a task"
        return None, error
    return task_id, error



def get_family_tasks(family_id, person_id):
    """_summary_

    Args:
        family_id (_type_): _description_

    Returns:
        _type_: sorted in ascending order of start time list of tasks
    """
    all_tasks = []
    your_tasks = []
    available_tasks = []
    upcoming_tasks = []
    raw_tasks = conn.get_family_tasks(family_id=family_id)
    if(len(raw_tasks) == 0):
        return [],[],[]
    
    for raw_task in raw_tasks:
        task_id = raw_task[1]
        cur_person_id = raw_task[2]
        completed = raw_task[3]
    
        task_info = conn.get_task_info(task_id=task_id)
        filled_task = Task(task_info[1],task_info[2], task_info[3],task_info[4])
        filled_task.change_id(task_id)

        if completed == True:
            filled_task.change_completed(True)
            all_tasks.append(filled_task)
            continue

        if cur_person_id is not None:
            name = get_user_info(person_id=cur_person_id)[0].name
            filled_task.assign_task(cur_person_id, name)

            if(cur_person_id == person_id):
                your_tasks.append(filled_task)
            else:
                upcoming_tasks.append(filled_task)
        else:
            available_tasks.append(filled_task)

        all_tasks.append(filled_task)
        
    return get_formatted_task_lists(all_tasks,your_tasks, upcoming_tasks, available_tasks)

def get_formatted_task_lists(all_tasks,your_tasks, upcoming_tasks, available_tasks):


    sorted_your_tasks = sorted(your_tasks, key=sort_by_date_time)
    formatted_your_tasks = format_time_in_task(sorted_your_tasks)

    sorted_upcoming_tasks = sorted(upcoming_tasks, key=sort_by_date_time)
    formatted_upcoming_tasks = format_time_in_task(sorted_upcoming_tasks)

    sorted_available_tasks = sorted(available_tasks, key=sort_by_date_time)
    formatted_available_tasks = format_time_in_task(sorted_available_tasks)

    return (
        formatted_your_tasks,
        formatted_upcoming_tasks,
        formatted_available_tasks
    )


def format_time_in_task(tasks):
    for task in tasks:
        date= task.date
        start_time = task.start_time
        end_time = task.end_time

        formatted_date = date.strftime("%d/%m/%y")
        start_am_pm = start_time.strftime('%I:%M %p')
        end_am_pm = end_time.strftime('%I:%M %p')

        task.edit_date(formatted_date, start_am_pm, end_am_pm)
    return tasks
    
def sort_by_date_time(task):
    date_str = task.date
    time_str = task.start_time
    full_date_str = f"{date_str} {time_str}"
    return datetime.strptime(full_date_str, "%Y-%m-%d %H:%M:%S")

def is_valid_date(date, start_time, end_time):
    error = None
    cur_time = datetime.now()
    full_date_format = '%Y-%m-%d %H:%M:%S'

    try:
        start_date = datetime.strptime(f"{date} {start_time}:00", full_date_format) 
        end_date = datetime.strptime(f"{date} {end_time}:00", full_date_format)

    except Exception as e:
        error = "Incorrect date format, should be: \"YEAR-MONTH-DAY HOUR:MINUTE\" "
        return error , None, None

    if start_date > end_date:
        error = "Starting time should be earlier than end time"

    if start_date < cur_time:
        error = "The task you are trying to add is in the past"
    return error

def sign_up_user(email, password, name, family_id):
    
    if(len(email) == len(email.strip())):
        try:
            email.index('@') < email.index('.')
        except Exception as e:
            return f"Incorrect email type. Please use a different one. {e}"
    else:
        return "Please remove whitespaces"
    
    person_id = conn.add_user(name, email, password)
    if(person_id is None):#already taken or error
        return "Email is already taken. Please use a different one"
    
    if(family_id is None):#no family was created before
        family_id = conn.create_family(person_id)
    else:
        conn.add_user_to_family(person_id, family_id)
    
    return "Success!"


