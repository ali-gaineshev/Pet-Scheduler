from family import Family, Task, Person
import psql_connector as conn
from datetime import datetime

key_path = "./secret/session_secret.txt"
def get_key_to_session():
    key = ""
    with open(key_path) as f:
        key = f.readline()
    return key

def validate_user(email, password):
    """_summary_

    Args:
        email (_type_): _description_
        password (_type_): _description_

    Returns:
        int: id of the person
        string or None: error 
    """
    error = None
    user_info = conn.get_user_info(email=email)
    if(user_info is None or password != user_info[3]):
        print(user_info)
        error = "Incorrect email/password or no such user found"
        return None, error
    return user_info[0], error

def get_user_info(person_id):

    user_info = conn.get_user_info(email=None , person_id=person_id)
    if(user_info is None):
        return None
    return Person(user_info[0], user_info[1], user_info[2], user_info[3])
    
def find_family_by_person_id(person_id):

    family_id = conn.get_user_info(email = None, person_id = person_id)[0]
    return family_id

def get_family_info(family_id):
    """ member_ids is a list of tuples of single element (id)

    Args:
        family_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    head_member_id, member_ids = conn.get_family_info(family_id=family_id)
    print(member_ids)
    members = [head_member_id]
    for member_tuple in member_ids:
        member_id = member_tuple[0]
        if(head_member_id != member_id):
            members.append(member_id)
    return members

def assign_task(task_id, person_id):
    conn.assign_task_to_user(task_id, person_id)

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
        return [],[],[],[]
    
    for raw_task in raw_tasks:
        task_id = raw_task[1]
        cur_person_id = raw_task[2]
        completed = raw_task[3]
    
        task_info = conn.get_task_info(task_id=task_id)
        filled_task = Task(task_id, task_info[1],task_info[2], task_info[3],task_info[4])

        if completed == True:
            filled_task.change_completed(True)
        
        if cur_person_id is not None:
            name = get_user_info(cur_person_id).name
            filled_task.assign_task(cur_person_id, name)

            if(cur_person_id == person_id):
                your_tasks.append(filled_task)
            else:
                upcoming_tasks.append(filled_task)
        else:
            available_tasks.append(filled_task)

        all_tasks.append(filled_task)
        
    return get_formatted_task_lists(your_tasks, upcoming_tasks, available_tasks)

def get_formatted_task_lists(your_tasks, upcoming_tasks, available_tasks):

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

    

    
