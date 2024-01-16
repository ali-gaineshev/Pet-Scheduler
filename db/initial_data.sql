INSERT INTO Persons VALUES ('Test Person', 'test@example.com', 'test123');
INSERT INTO Tasks (task_id, name, date) VALUES (0, 'test task #1', '2024-01-14');
INSERT INTO Families VALUES (1, 1);
INSERT INTO Familymembers VALUES (1, 1);


DELETE from <TABLENAME> where <condition>;
UPDATE <TABLENAME> set <column_name> = <new_value>, ..., WHERE <condition> (important condition!); 
