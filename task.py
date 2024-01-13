import family

class Task:

    def __init__(self, name, cooperators, family):
        self.name = name
        self.cooperators = cooperators # a list of member objects
        self.family = family # a family object
