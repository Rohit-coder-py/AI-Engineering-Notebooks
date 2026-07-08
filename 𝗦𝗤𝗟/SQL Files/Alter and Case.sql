-- USE CASES OF ALTER:

-- ALTER is used to change the structure of an existing table

-- 1. Add new columns
-- 2. Remove columns
-- 3. Rename columns
-- 4. Change data types
-- 5. Set or remove default values
-- 6. Add or remove constraints
-- 7. Drop a constraints
-- 8. Rename the table



CREATE TABLE students(
student_id SERIAL Primary Key,
name VARCHAR(100),
age bigint)
;

insert into students(name,age)
Values('Anjali',21)




select * from students;




-- 1. Add new columns

ALTER TABLE students 
Add column email Varchar(100) DEFAULT 'Not provided'



Update students
SET email = 'vjha9984@gmail.com' where student_id = 1


select * from students



-- 2. Remove columns


Alter table students
DROP column email;


-- 3. Rename columns


Alter table students
Rename email to contact_number;

select * from students


-- 4. Change data types

Alter table students
ALTER age TYPE smallint;


-- 5. Set or remove default values
ALTER TABLE students
ALTER COLUMN age
SET DEFAULT 18;


-- SET or remove default values
ALTER TABLE students
Alter column age 
DROP Default


-- Add or remove constraints
ALTER Table students 
ADD Constraint age_check check (age>=0)

Select * from college_students



-- 8. Drop a constraints

ALTER Table students
DRop constraint age_check



-- Rename a table

ALTER table students
Rename to  college_students

Select * from college_students



----------------------------------------------------------------
----------------------------------------------------------------
----------------------------------------------------------------


-- Cases in SQL 

-- CASE is a conditional expression in SQL that works
-- like an if-else or switch statement. It lets you
-- return different values based on different
-- conditions - all within a single query.


-- WHY DO WE USE CASE?

-- . To create custom columns on-the-fly
-- · To categorize data based on certain logic
-- . To replace values conditionally
-- . To handle nulls or missing values gracefully
-- . To simplify complex logic inside SELECT queries

