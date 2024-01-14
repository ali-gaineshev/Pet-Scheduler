class Pets:

    def __init__(self, family_id, name):
        self.family_id = family_id
        self.name = name

class Person:

    def __init__(self, name, email, password):
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
    family_count = 1 #for db purposes

    def __init__(self, members):
        
        self.members: list[Person] = members #a list of member objects
        self.head_member = self.members[0] #admin role
        self.all_tasks = []
        self.pets = []
        
        self.family_id = Family.family_count #family id for db
        Family.family_count += 1 #counter for how many family count
    

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
    task_count = 1

    def __init__(self, name, date):
        self.name = name #the task string
        self.date = date #yyyy-mm-dd
        self.id = Task.task_count
        Task.task_count += 1

    def edit_task_name(self , new_name):
        self.name = new_name
    def edit_task_date(self, new_date):
        self.date = new_date
    def get_task(self):
        return self.name
    def get_date(self):
        return self.date

    def __str__(self):
        return f"Id - {self.id}. What to do: {self.name}. Date: {self.date}"

    def __repr__(self):
        return f'Task({self.id},\'{self.name}\',\'{self.date}\' )'