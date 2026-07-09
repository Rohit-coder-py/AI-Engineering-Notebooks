
💡 A simple rule:

Foreign Key only → One-to-Many
Foreign Key + UNIQUE → One-to-One
Two Foreign Keys in a junction table → Many-to-Many



-- ==========================================
-- STEP 1: CREATE TABLES
-- ==========================================

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE enrollments (

    enrollment_id SERIAL PRIMARY KEY,

    student_id INT,

    course_id INT,

     (studenFOREIGN KEYt_id)
    REFERENCES students(student_id),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);

-- ==========================================
-- STEP 2: INSERT DATA
-- ==========================================

INSERT INTO students (name)
VALUES
('Rahul'),
('Priya'),
('Aman');

INSERT INTO courses (course_name)
VALUES
('Python'),
('SQL'),
('Machine Learning');

INSERT INTO enrollments (student_id, course_id)
VALUES
(1,1),   -- Rahul -> Python
(1,2),   -- Rahul -> SQL
(2,2),   -- Priya -> SQL
(3,1),   -- Aman -> Python
(3,3);   -- Aman -> Machine Learning

-- ==========================================
-- STEP 3: VIEW TABLES
-- ==========================================

SELECT * FROM students;

SELECT * FROM courses;

SELECT * FROM enrollments;

-- ==========================================
-- STEP 4: INNER JOIN
-- ==========================================

SELECT
    students.name,
    courses.course_name
FROM enrollments
INNER JOIN students
ON enrollments.student_id = students.student_id
INNER JOIN courses
ON enrollments.course_id = courses.course_id;