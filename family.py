class Person:

    def __init__(self, name, email, password, tasks = []):
        self.name = name
        self.email = email
        self.password = password 
        self.tasks = tasks

    def change_password(password):
        self.password = password

class Family:

    family_id = 1

    def __init__(self, members):
        #self.email = email
        self.members = members
        self.head_member = member[0]

        Family.family_id += 1

    

    def add_member