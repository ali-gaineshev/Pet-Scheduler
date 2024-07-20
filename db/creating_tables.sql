CREATE TABLE Persons (
    person_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE Tasks (
    task_id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    date TIMESTAMP NOT NULL CHECK (date > CURRENT_TIMESTAMP),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    person_id INTEGER DEFAULT NULL,
    FOREIGN KEY (person_id) REFERENCES Persons(person_id) ON DELETE CASCADE
);

CREATE TABLE Family (
    family_id SERIAL PRIMARY KEY,
    head_member_id INTEGER NOT NULL,
    FOREIGN KEY (head_member_id) REFERENCES Persons(person_id)
);

CREATE TABLE FamilyMembers (
    family_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (family_id, person_id),
    FOREIGN KEY (family_id) REFERENCES Family(family_id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES Persons(person_id) ON DELETE CASCADE
);

