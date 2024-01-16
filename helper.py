from family import Family, Task, Person

def create_person(name, email, password):
    new_person = Person(name, email, password)


def create_family(members: list[Person]):
    new_family = Family(members)
    