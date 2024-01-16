import psycopg2 
from flask import g

PATH_TO_PARAMS = "./secret/db_secret.txt"

def read_credentials():
    params = {}
    with open(PATH_TO_PARAMS) as f:
        for i in range(5):
            line = f.readline()
            split_line = line.split(":")
            params[split_line[0].strip()] = split_line[1].strip()
    return params

def get_db(): 
    db_params = read_credentials()                                
    try:
        if 'db' not in g:
            g.db = psycopg2.connect(**db_params) 
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

def add_user(name, email, password):
    """
    Adds a user to db
    Returns:
        None if error
        new persoin id if completed
    """
    person_id = None
    conn = get_db()
    if conn is None:
        print("No connection")
        return None
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO PERSONS(name, email, password) VALUES (%s, %s, %s) RETURNING person_id", (name, email, password))
                person_id = cursor.fetchone()[0]
            conn.commit()
            
    except Exception as e:
        print(f"Error adding user: {e}")

    return person_id

def get_user_info(email):
    info = None
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM PERSONS WHERE email = %s", (email,))
                info = cursor.fetchone()
    except Exception as e:
        print(f"Error checking user: {e}")

    return info

def create_family(head_member_id):
    """
    Creates a new family in db
    Returns:
        None - if error
        family_id - if completed
    """
    family_id = None
    conn = get_db()
    if conn is None:
        print("No connection")
        return None
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO FAMILIES(head_member_id) VALUES (%s) RETURNING family_id", (head_member_id,))
                family_id = cursor.fetchone()[0]
            conn.commit()

    except Exception as e:
        print(f"Error adding family: {e}")

    return family_id

def execute_commands(conn, input_title):
    cur = conn.cursor() 
    cur.execute(f"select * from user026_series('{input_title}')") 
    series_sql = cur.fetchall()
    

    if(len(series_sql) > 1):
        print(f"Error. There are {len(series_sql)} tv series with the same title!")
        exit(1)
    
    if(series_sql == [] or series_sql[0] == (None,None, None, None, None, None, None)):
        print("Error. Couldn't find the title!")
        exit(1)

    series_sql = series_sql[0]
    series = {"Series" : series_sql[0], "Year": series_sql[1], "Number of Seasons": series_sql[2], "Number of Episodes": series_sql[3], "Runtime": series_sql[4], "Rating": series_sql[5], "Votes": series_sql[6]}
    
    cur.execute(f"select * from user026_episodes('{input_title}')") 
    episodes_sql = cur.fetchall()

    if(episodes_sql == []):
        print("Something went wrong. Couldn't use the title")
        exit(1)
   
    episodes = []
    for row in episodes_sql:
            season = {"Season" : row[0], "Year": row[1], "Episodes": row[2], "Avg. Votes": row[3], "Avg. Rating": row[4], "Difference": row[5]}
            episodes.append(season)

    print_html(series,episodes)

    cur.close()
    conn.close() 


if __name__ == '__main__':
    main()