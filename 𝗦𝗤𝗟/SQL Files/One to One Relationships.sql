
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

CREATE TABLE library_cards (
    card_id SERIAL PRIMARY KEY,

    student_id INT UNIQUE NOT NULL,

    card_number VARCHAR(20) UNIQUE,

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
-- STEP 3: INSERT LIBRARY CARDS
-- ==========================================

INSERT INTO library_cards (student_id, card_number)
VALUES
(1, 'LIB1001'),
(2, 'LIB1002'),
(3, 'LIB1003');

-- ==========================================
-- STEP 4: VIEW TABLES
-- ==========================================

SELECT * FROM students;

SELECT * FROM library_cards;

-- ==========================================
-- STEP 5: INNER JOIN
-- Show student with their library card
-- ==========================================

SELECT
    students.student_id,
    students.name,
    library_cards.card_number
FROM students
INNER JOIN library_cards
ON students.student_id = library_cards.student_id;