



💡 A simple rule:

Foreign Key only → One-to-Many
Foreign Key + UNIQUE → One-to-One
Two Foreign Keys in a junction table → Many-to-Many


-- ==========================================
-- STEP 1: CREATE TABLES
-- ==========================================

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(50),
    marks INT,

    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
);

-- ==========================================
-- STEP 2: INSERT STUDENTS
-- ==========================================

INSERT INTO students (name)
VALUES
('Rahul'),
('Priya'),
('Aman');

-- ==========================================
-- STEP 3: INSERT MARKS
-- ==========================================

INSERT INTO marks (student_id, subject, marks)
VALUES
(1, 'Math', 95),
(1, 'English', 88),
(2, 'Math', 76),
(3, 'Science', 91),
(3, 'English', 84);

-- ==========================================
-- STEP 4: VIEW TABLES
-- ==========================================

SELECT * FROM students;

SELECT * FROM marks;

-- ==========================================
-- STEP 5: INNER JOIN
-- Show each student's name with their marks
-- ==========================================

SELECT
    students.student_id,
    students.name,
    marks.subject,
    marks.marks
FROM students
INNER JOIN marks
ON students.student_id = marks.student_id;
