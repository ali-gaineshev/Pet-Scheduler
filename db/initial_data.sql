INSERT INTO Persons(name, email,password) VALUES ('Test Person', 'test@example.com', 'test123');
INSERT INTO Persons(name, email,password) VALUES ('Test Person 2', 'admin', 'test123');
INSERT INTO Families(head_member_id) VALUES (1);
INSERT INTO Familymembers(family_id, person_id) VALUES (1, 1);
INSERT INTO Familymembers(family_id, person_id) VALUES (1, 2);


INSERT INTO Tasks(name, date,start_time, end_time) VALUES ('test task #1', '2024-01-21', '10:00:00', '12:00:00');
INSERT INTO Tasks(name, date,start_time, end_time) VALUES ('Walk Yumi', 'test task #2', '2024-01-21', '7:00:00', '10:00:00');
INSERT INTO Tasks(name, date,start_time, end_time) VALUES ('Walk Yumi', 'test task #3', '2024-01-22', '23:00:00', '23:50:00');

INSERT INTO FAMILYTASKS(family_id, task_id, person_id) VALUES (1, 1, 1);
INSERT INTO FAMILYTASKS(family_id, task_id) VALUES (1, 2);
INSERT INTO FAMILYTASKS(family_id, task_id) VALUES (1, 3);
