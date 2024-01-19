from family import Family, Task, Person

key_path = "./secret/session_secret.txt"
def get_key_to_session():
    key = ""
    with open(key_path) as f:
        key = f.readline()
    return key