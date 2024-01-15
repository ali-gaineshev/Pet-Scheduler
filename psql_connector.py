import psycopg2 
import sys 



def read_credentials():
    params = {}
    with open("./secret/db_secret.txt") as f:
        for i in range(5):
            line = f.readline()
            split_line = line.split(":")
            params[split_line[0].strip()] = split_line[1].strip()
    return params

def main(): 
    db_params = read_credentials()                                
    try:
        conn = psycopg2.connect(**db_params) 
        print("Database connected")
    except Exception as e:
        print("Couldn't connect to the database! Something went wrong either with the server, username or password. Error:\n")
        print(e)
        exit(1)

    

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