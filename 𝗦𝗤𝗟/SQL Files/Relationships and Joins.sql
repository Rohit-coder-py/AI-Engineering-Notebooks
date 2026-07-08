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

This is called Normalization.
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


-- now lets join both 

=============================================
SYNTAX:

SELECT
    t1.column1,
    t1.column2,
    t2.column3,
    t2.column4
FROM table1 AS t1
JOIN table2 AS t2
ON t1.common_column = t2.common_column;

===============================================


SELECT
s.student_id,
s. name,
sp.address,
sp.age,
sp.phone
FROM students s
JOIN student_profiles sp
ON s.student_id = sp.student_id;




====================================================================
2. One to many relationship

One record in the first table can be related to many records in the second table.
====================================================================


STEP 1: CREATE TABLES

• students table → student info
• marks table → subject-wise marks (linked to student)

STEP 2: INSERT SAMPLE DATA

STEP 3: ADD FOREIGN KEY CONSTRAINT

STEP 4: TEACH JOINS (WITH EXAMPLES LIKE INNER JOIN, LEFT JOIN, ETC.)

==================================================================================================================================



CREATE TABLE students (
student_id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL)

CREATE TABLE marks (
mark_id SERIAL PRIMARY KEY,
student_id INT,
subject VARCHAR(50),
marks INT,
FOREIGN KEY (student_id) REFERENCES students(student_id))



INSERT INTO students (name)
VALUES ('Akarsh Vyas'), ('Simran Mehta'), ('Rohan Gupta');

INSERT INTO marks (student_id, subject, marks)
VALUES

(1, 'English', 85),
(1, 'Math', 89),
(1, 'Science', 92),

(2, 'English', 80),
(2, 'Math', 75),
(2, 'Science', 78),

(3, 'English', 72),
(3, 'Math', 70),
(3, 'Science', 74);




Select * from students;
select * from marks;


-- now lets join both 

=============================================
SYNTAX:

SELECT
    t1.column1,
    t1.column2,
    t2.column3,
    t2.column4
FROM table1 AS t1
JOIN table2 AS t2
ON t1.common_column = t2.common_column;

===============================================
Select * from students;
select * from marks;


Select 
      s.student_id,
	  s.name,
	  m.subject,
	  m.marks
From students s
JOIN marks m
ON s.student_id = m.student_id




