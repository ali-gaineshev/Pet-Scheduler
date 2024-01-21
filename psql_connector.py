import psycopg2 
from flask import g
from family import Family, Task, Person
import functools

PATH_TO_PARAMS = "./secret/db_secret.txt"

def read_credentials():
    """
    READ DB credentials from secret path!
    """
    params = {}
    with open(PATH_TO_PARAMS) as f:
        for i in range(5):
            line = f.readline()
            split_line = line.split(":")
            params[split_line[0].strip()] = split_line[1].strip()
    return params

DB_PARAMS = read_credentials()  

def get_db(): 
                                  
    try:
        if 'db' not in g:
            g.db = psycopg2.connect(**DB_PARAMS) 
            print("Database connected")
    except Exception as e:
        print("Couldn't connect to the database! Something went wrong either with the server, username or password. Error:\n")
        print(e)
        return None

    return g.db

def close_db(e = None):
    if e is not None:
        print(f"Error with db: {e}")
        exit(1)
    
    db = g.pop('db',None)
    if db is not None:
        db.close()

def get_db_connection(commit = True):
    """
    Decorator. Gets the connection to db. If connected, proceed to original function
    Otherwise return None
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = get_db()
            if conn is None:
                print("\n--ERROR No connection\n")
                return None
            try:
                with conn:
                    with conn.cursor() as cursor:
                        return func(cursor, *args, **kwargs)
                    if(commit == True):
                        conn.commit()
            except Exception as e:
                print(f"\n--ERROR with conn to db {e}\n")
        return wrapper
    return decorator

@get_db_connection(commit = True)
def add_user(cursor, name, email, password):
    """
    Adds a user to db
    Returns:
        None if error
        new persoin id if completed
    """
    person_id = None

    try:
        #check if email is already in db
        cursor.execute("SELECT * FROM PERSONS where email = (%s)", (email,))
        match_len = len(cursor.fetchall())
        if(match_len > 0):
            print("----DEBUG: EMAIL IS ALREADY IN DB")
            return None
        #email is not in db
        cursor.execute("INSERT INTO PERSONS(name, email, password) VALUES (%s, %s, %s) RETURNING person_id", (name, email, password))
        person_id = cursor.fetchone()[0]

    except Exception as e:
        print(f"\n--ERROR with adding a new user: {e}\n")


    return person_id

@get_db_connection(commit = True)
def create_family(cursor, head_member_id):
    """
    Creates a new family in db
    Returns:
        None - if error
        family_id - if completed
    """
    family_id = None

    try:
        cursor.execute("INSERT INTO FAMILIES(head_member_id) VALUES (%s) RETURNING family_id", (head_member_id,))
        family_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO FAMILYMEMBERS(family_id, person_id) VALUES (%s, %s)", (family_id, head_member_id))
    except Exception as e:
        print(f"\n--ERROR with creating a family: {e}\n")

    return family_id

@get_db_connection(commit = True)
def add_user_to_family(cursor, person_id, family_id):
    """
    Add a new user to family. Use after get_user_info() and add_user(). Check if person is in any other family
    Assumption: user exits in persons
    """
    try:
        cursor.execute("INSERT INTO FAMILYMEMBERS(family_id, person_id) VALUES (%s, %s)", (family_id, person_id))
    except Exception as e:
        print(f"\n--ERROR adding a user to a family: {e}\n")

@get_db_connection(commit=True)
def create_task(cursor, name, date, start_time, end_time, family_id=None):
    """
    Creates a task in db, return the new task_id. Family_id is optional but preferred to do it right away
    Doesn't assign a task to a person.
    """
    task_id = None
    try:
        cursor.execute(
            "INSERT INTO TASKS(name, date, start_time, end_time) VALUES (%s, %s, %s, %s) RETURNING task_id",
            (name, date, start_time, end_time),
        )
        task_id = cursor.fetchone()[0]
        if family_id is not None:
            cursor.execute(
                "INSERT INTO FAMILYTASKS (family_id, task_id) VALUES (%s, %s)",
                (family_id, task_id),
            )

    except Exception as e:
        print(f"\n--ERROR with creating a task: {e}\n")
    return task_id


@get_db_connection(commit = True)
def assign_task_to_user(cursor, task_id, person_id):
    """
    Assign a task to a specific user. Returns family_id
    Returns
        
    """
    family_id = None
    try:
        cursor.execute("UPDATE FAMILYTASKS set person_id = (%s) where task_id = (%s) RETURNING family_id", (person_id, task_id))
        family_id = cursor.fetchone()[0]
    except Exception as e:
        print(f"\n--ERROR with giving task to a user: {e}\n")
    return family_id

@get_db_connection(commit = True)
def change_task_complete(cursor, task_id, complete):
    """
    Assumption: task is already assigned to a family
    """
    try:
        cursor.execute("UPDATE FAMILYTASKS SET completed = (%s) WHERE task_id = (%s)", (complete, task_id))

    except Exception as e:
        print(f"\n--ERROR changing task.complete bool: {e}\n")

@get_db_connection(commit = True)
def unassign_task(cursor, task_id):
    """
    Assumption: task is already assigned to a family
    """
    try:
        cursor.execute("UPDATE FAMILYTASKS SET person_id = NULL WHERE task_id = (%s)", (task_id, ))

    except Exception as e:
        print(f"\n--ERROR unassigning task from user: {e}\n")

@get_db_connection(commit = False)
def get_user_info(cursor, email, person_id = None):
    """
    Get all of the user information based on email

    Parameters:
    - email - primary
    - person_id

    Returns:
    4 elem tuple - (person_id, name, email, password)
    NONE - if no user
    """
    info = None
    try: 
        if(person_id is None):
            cursor.execute("SELECT * FROM PERSONS WHERE email = %s", (email,))
        else:
            cursor.execute("SELECT * FROM PERSONS WHERE person_id = %s", (person_id,))            
        info = cursor.fetchone()
    except Exception as e:
        print(f"\n--ERROR getting user info: {e}\n")

    return info

@get_db_connection(commit=False)
def find_family_by_person_id(cursor, person_id):
    family_id = None
    try:
        cursor.execute("SELECT family_id FROM FAMILYMEMBERS WHERE person_id = %s", (person_id,))
        family_id = cursor.fetchone()[0]
        
    except Exception as e:
        print(f"\n--ERROR getting family info from the person id: {e}\n")

    return family_id

@get_db_connection(commit = False)
def get_family_info(cursor, family_id):
    """
    
    """
    head_member_id = None
    member_ids = None
    try:
        cursor.execute("SELECT * FROM FAMILIES WHERE family_id = %s", (family_id,))
        head_member_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM FAMILYMEMBERS WHERE family_id = (%s)", (family_id,))
        member_ids = cursor.fetchall()    
    except Exception as e:
        print(f"\n--ERROR getting family info: {e}\n")

    return head_member_id, member_ids

@get_db_connection(commit = False)
def get_family_tasks(cursor, family_id):
    """
    Assumption: task is already assigned to a family
    Returns:
        array of tasks
    """
    family_tasks = []
    try:
        cursor.execute("SELECT * from FAMILYTASKS WHERE family_id = (%s)", (family_id,))
        family_tasks = cursor.fetchall()

    except Exception as e:
        print(f"\n--ERROR getting family's tasks info: {e}\n")

    return family_tasks

@get_db_connection(commit = False)
def get_task_info(cursor, task_id):
    """
    Assumption: task is already assigned to a family
    """
    task = None
    try:
        cursor.execute("SELECT * from TASKS WHERE task_id = (%s)", (task_id,))
        task = cursor.fetchone()

    except Exception as e:
        print(f"\n--ERROR getting task info: {e}\n")

    return task

