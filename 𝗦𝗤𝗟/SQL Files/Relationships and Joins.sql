In a relational database, data is stored across
multiple tables, and these tables are connected
through relationships.
Instead of repeating the same data again and again in
one huge table, we split it into smaller, meaningful
tables and connect them using keys (Primary and
Foreign Keys)


 Types of Relationships 
 
1. One-to-One (1:1)
2. One-to-Many (1:N) MOST COMMON)
3. Many-to-Many (M:N)

---------------------------------------------------------------------
1. One-to-One (1:1) RelationShips
---------------------------------------------------------------------

CREATE TABLE students (
student_id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL)

INSERT INTO students (name)
VALUES
('Akarsh Vyas'),
('Simran Mehta'),
('Rohan Gupta');

Select * from Students;



CREATE TABLE student_profiles (
student_id INT PRIMARY KEY, 
address TEXT,
age INT,
phone VARCHAR(15));


INSERT INTO student_profiles (student_id, address, age, phone)
VALUES
(1, 'Delhi, India', 22, '9999999999'),
(2, 'Mumbai, India', 21, '8888888888'),
(3, 'Bangalore, India', 23, '7777777777');

Select * from Students;

Select * from student_profiles;

---------------------------------------------------------------------
---------------------------------------------------------------------
-- Now both the tables have been created and we can
-- clearly see there is a similar column and that is
-- student_id but currently there is no relationship setup
-- between them for setting them up you have to create
-- a foreign key in the 2nd table.

-- Primary Key uniquely identifies each row in a
-- table.
-- Foreign Key links one table to another by refer
-- to the Primary Key of that table



-- now lets convert student_profile table constrauiint to primary key to foreign key 

ALTER TABLE student_profiles
Add constraint fk_students_id
FOREIGN KEY (student_id)
REFERENCES students(student_id)

Select * from Students;

Select * from student_profiles;



