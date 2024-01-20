from family import Family, Task, Person
import psql_connector as conn

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
    members = [head_member_id]
    for member_tuple in member_ids:
        member_id = member_tuple[0]
        if(head_member_id != member_id):
            members.append(member_id)
    return members

def get_family_tasks(family_id):
    """_summary_

    Args:
        family_id (_type_): _description_

    Returns:
        _type_: sorted in ascending order of start time list of tasks
    """
    tasks = []
    raw_tasks = conn.get_family_tasks(family_id=family_id)
    for raw_task in raw_tasks:
        task_id = raw_task[1]
        task_info = conn.get_task_info(task_id=task_id)
        filled_task = Task(task_id, task_info[1],task_info[2], task_info[3],task_info[4])
        if raw_task[3] == True: #raw_task[3] - completed:bool
            filled_task.change_completed(True)
        
        if raw_task[2] is not None:#raw_task[2] - person_id : int
            filled_task.assign_task(raw_task[2])

        tasks.append(filled_task)
        return sorted(tasks, key = lambda filled_task: filled_task[3])
    
