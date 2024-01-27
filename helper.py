from family import Family, Task, Person
import psql_connector as conn
from datetime import datetime
from typing import Optional

key_path = "./secret/session_secret.txt"

def get_key_to_session():
    """ 
    secret for security reasons
    """
    key = ""
    with open(key_path) as f:
        key = f.readline()
    return key

def to_json(person: Person):
    """Converts person instance to json

    Args:
        person (Person): 

    Returns:
        dict: some variables of person instance
    """
    json_dict = vars(person)
    json_dict.pop('password')
    return json_dict

def from_json(json_dict: dict):
    """Convert json fomrat to Person. Now complete, password is removed

    Args:
        json_dict (dict)

    Returns:
        Person(): person from json
    """
    return Person(json_dict['person_id'], json_dict['name'], json_dict['email'])

def get_user_info(email: Optional[str] = None, password:Optional[str] = None, person_id:Optional[str] = None):
    """Gets user info from the db

    Args:
        email (string, optional): Defaults to None.
        password (string, optional): Defaults to None.
        person_id (string, optional): Defaults to None.

    Returns:
        any: 1) person instance either None or type Person
        any: 2) error either None or string
    """
    error: Optional[str] = None
    user_info: tuple
    if person_id is None: #login with email
        user_info = conn.get_user_info(email=email)
        
        if(user_info is None or password != user_info[3]):
            error = "Incorrect email/password or no such user found"
            return None, error
        
    elif(person_id is not None):#retrieve info with person_id
        user_info = conn.get_user_info(email=None, person_id=person_id)
        if(user_info is None):
            error = "Something went wrong"
            return None, error
    else:
        return None, "Something went wrong"
    return Person(user_info[0], user_info[1], user_info[2], user_info[3]), error
    
def find_family_by_person_id(person_id: int):
    """ 
    Get family id from person_id
    """
    family_id = conn.find_family_by_person_id(person_id = person_id)
    return family_id

def get_family_info(family_id: int):
    """ 
    Get list of family members' ids where first id in the list is the head members
    Args:
        family_id (int)

    Returns:
        list[int]]: ids of ther members in the family
    """
    head_member_id, member_ids = conn.get_family_info(family_id=family_id)
    # Note: member_ids is a list of tuples of single element (id)
    members = [head_member_id]
    #add more members beside the head member
    for member_tuple in member_ids:
        member_id = member_tuple[0]
        if(head_member_id != member_id):
            members.append(member_id)
    return members

def assign_task(task_id:int , person_id: int):
    """ 
    Assign task to a specific member in family ! Create task first, then assign
    """
    conn.assign_task_to_user(task_id, person_id)

def unassign_task(task_id:int):
    """ 
    Unassign task, doesn't mean it removes it, just puts in the 'available tasks'
    """
    conn.unassign_task(task_id)

def change_task_complete(task_id:int , complete:bool):
    """ 
    Complete the task. it will be removed from every list
    """
    conn.change_task_complete(task_id,complete)

def create_new_task(task: Task, family_id: int):
    """ Creates a new task in the db

    Args:
        task (Task): make task instance in the main, then use it here
        family_id: int

    Returns:
        task_id: int - id of the new task
        error: any - None if no error.
    """
    error: Optional[str] = None #Union[str, None]
    task_id:int = conn.create_task(task.name, task.date, task.start_time, task.end_time, family_id)
    if task_id is None:
        error:str = "Error with creating a task"
        return None, error
    return task_id, error



def get_family_tasks(family_id: int, person_id:int):
    """ Gets all family tasks from the family in db. Returns 3 lists

    Args:
        family_id (int):
        person_id (int):

    Returns:
        3 lists (Task): sorted in ascending order of start time list of tasks, where
            1 - user's tasks
            2 - upcoming tasks (other users in family)
            3 - available tasks
    """
    all_tasks: list[Task] = []
    your_tasks: list[Task] = []
    available_tasks: list[Task] = []
    upcoming_tasks: list[Task] = []
    raw_tasks: list[tuple] = conn.get_family_tasks(family_id=family_id)

    if(len(raw_tasks) == 0):
        return [],[],[]
    
    for raw_task in raw_tasks:
        task_id: int = raw_task[1]
        cur_person_id: int = raw_task[2]
        completed: bool = raw_task[3]
    
        task_info: tuple = conn.get_task_info(task_id=task_id)
        filled_task: Task = Task(task_info[1],task_info[2], task_info[3],task_info[4])
        filled_task.change_id(task_id)#assign id 

        if completed == True: #if completed there is no point of adding it
            filled_task.change_completed(True)
            all_tasks.append(filled_task)
            continue

        if cur_person_id is not None: #task is assigned, therefore add it to upcoming or user list
            name = get_user_info(person_id=cur_person_id)[0].name
            filled_task.assign_task(cur_person_id, name)

            if(cur_person_id == person_id):
                your_tasks.append(filled_task)
            else:
                upcoming_tasks.append(filled_task)
        else:#no person assigned yet
            available_tasks.append(filled_task)

        all_tasks.append(filled_task)
    
    #sort tasks and return
    return get_formatted_task_lists(all_tasks,your_tasks, upcoming_tasks, available_tasks)

def get_formatted_task_lists(all_tasks: list[Task],your_tasks: list[Task], upcoming_tasks:list[Task], available_tasks:list[Task]):
    """ sort and format tasks

    Args:
        all_tasks (list[Task])
        your_tasks (list[Task])
        upcoming_tasks (list[Task])
        available_tasks (list[Task])

    Returns:
        your_tasks (list[Task])
        upcoming_tasks (list[Task])
        available_tasks (list[Task])
    """

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


def format_time_in_task(tasks: list[Task]):
    """Change the format of tasks, so it's easier to show

    Args:
        tasks (list[Task]):

    Returns:
        tasks (list[Task])
    """
    for task in tasks:
        date = task.date
        start_time = task.start_time
        end_time = task.end_time

        #formats
        formatted_date = date.strftime("%d/%m/%y")
        start_am_pm = start_time.strftime('%I:%M %p')
        end_am_pm = end_time.strftime('%I:%M %p')

        task.edit_date(formatted_date, start_am_pm, end_am_pm)

    return tasks
    
def sort_by_date_time(task: Task):
    """Convert into datetime, and return

    Args:
        task (Task)
    """
    date_str = task.date
    time_str = task.start_time
    full_date_str = f"{date_str} {time_str}"
    return datetime.strptime(full_date_str, "%Y-%m-%d %H:%M:%S")

def is_valid_date(date:str, start_time: str, end_time: str):
    """Check if date is valid

    Args:
        date (str)
        start_time (str)
        end_time (str)

    Returns:
        Optional[str] - string message if error, otherwise None
    """
    error: Optional[str] = None
    cur_time: datetime = datetime.now()
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

def sign_up_user(email: str, password: str, name:str, family_id:int):
    """Sign up user. Check if email exist in db, if not add it

    Args:
        email (str)
        password (str)
        name (str)
        family_id (int)

    Returns:
        str: message to display
    """
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


