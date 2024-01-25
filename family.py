class Pets:

    def __init__(self, family_id, name):
        self.family_id = family_id
        self.name = name

class Person:

    def __init__(self, person_id, name, email, password = None):
        self.person_id = person_id #update after sql
        self.name = name
        self.email = email
        self.password = password 
        self.tasks = []

    def change_password(self,password):
        self.password = password

    def get_name(self,):
        return self.name
        
    def add_task(self,new_task):
        self.tasks.append(new_task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_persons_tasks(self):
        return self.tasks

    def __str__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nPass: {self.password}\nTasks: {self.tasks}"

class Family:

    def __init__(self, id, members):
        
        self.members: list[Person] = members #a list of member objects
        self.head_member = self.members[0] #admin role
        self.all_tasks = []
        self.pets = []
        

    def add_member(self, new_member):
        self.members.append(new_member)
        

    def create_task(self, name, date):
        new_task = Task(name, date)    
        self.all_tasks.append(new_task)
        return self.all_tasks[-1]
    

    def remove_task(self,task_id):
        for task in self.all_tasks:
            if task_id == task.id:
                self.all_tasks.remove(task) 
        
        for member in self.members:
            for task in member.tasks:
                if(task_id == task.id):
                    member.remove_task(task)
                    break

    def give_task(self,task, person_name):
        
        index = self.person_name_to_member_index(person_name)
        if(index == -1):
            print("Error with member array")
        
        self.members[index].add_task(task)
    
    def unassign_task(self,task, person_name):
        index = self.person_name_to_member_index(person_name)
        if(index == -1):
            print("Error with member array")
        
        self.members[index].remove_task(task)

    def person_name_to_member_index(self, person_name):
        #return index of person on person's name
        for index, member in enumerate(self.members):
            if(member.get_name() == person_name):
                return index
                
        return -1         
        
    def print_member_with_tasks(self):
        for member in self.members:
            print(f"Member: {member.name}")
            print("Tasks: ")
            for task in member.tasks:
                print(task)
            print("")
        

class Task:

    def __init__(self, name, date, start_time, end_time):
        self.task_id = None
        self.name = name #the task string
        self.date = date #yyyy-mm-dd
        self.start_time = start_time
        self.end_time = end_time
        self.completed = False
        self.person_id_to_do = None
        self.person_name_to_do = None

    def assign_task(self,person_id, name):
        self.person_id_to_do = person_id
        self.person_name_to_do = name

    def change_completed(self,completed):
        self.completed = completed

    def change_id(self, task_id):
        self.task_id = task_id

    def edit_date(self, date, start_time, end_time):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def edit_task_name(self , new_name):
        self.name = new_name
    def get_task(self):
        return self.name
    def get_date(self):
        return self.date

    def __str__(self):
        return f"Id - {self.id}. What to do: {self.name}. Date: {self.date}"

    def __repr__(self):
        return f'Task({self.task_id},\'{self.name}\',\'{self.date}\',\'{self.start_time}\',\'{self.end_time}\',\'{self.completed}\',\'{self.person_id_to_do}\' )'