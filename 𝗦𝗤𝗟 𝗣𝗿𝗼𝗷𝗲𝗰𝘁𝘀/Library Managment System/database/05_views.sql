CREATE VIEW student_details AS
SELECT
    student_id,
    name,
    gender,
    city,
    phone,
    email,admission_date
FROM students;
---------------

CREATE VIEW student_marks AS
SELECT
    s.student_id,
    s.name,
    m.subject,
    m.marks
	
FROM students s
JOIN marks m
ON s.student_id = m.student_id;
--------

CREATE VIEW student_performance AS
SELECT
    s.student_id,
    s.name,
    ROUND(AVG(m.marks), 2) AS average_marks
FROM students s
JOIN marks m
ON s.student_id = m.student_id
GROUP BY s.student_id, s.name;
------------------

CREATE VIEW paid_students AS
SELECT
    s.student_id,
    s.name,
    f.amount,
    f.payment_date
FROM students s
JOIN fees f
ON s.student_id = f.student_id
WHERE f.status = 'Paid';
----------------

CREATE VIEW pending_fees AS
SELECT
    s.student_id,
    s.name,
    f.amount
FROM students s
JOIN fees f
ON s.student_id = f.student_id
WHERE f.status = 'Pending';
---------------

CREATE VIEW student_fee_report AS
SELECT
    s.student_id,
    s.name,
    s.city,
    f.amount,
    f.status,
    f.payment_date
FROM students s
JOIN fees f
ON s.student_id = f.student_id;
-------------------

CREATE VIEW topper_students AS
SELECT
    s.student_id,
    s.name,
    ROUND(AVG(m.marks), 2) AS average_marks
FROM students s
JOIN marks m
ON s.student_id = m.student_id
GROUP BY s.student_id, s.name
HAVING AVG(m.marks) >= 80;
------------------

CREATE VIEW complete_student_report AS
SELECT
    s.student_id,
    s.name,
    s.city,
    ROUND(AVG(m.marks), 2) AS average_marks,
    f.amount,
    f.status
FROM students s
JOIN marks m
ON s.student_id = m.student_id
JOIN fees f
ON s.student_id = f.student_id
GROUP BY
    s.student_id,
    s.name,
    s.city,
    f.amount,
    f.status;



--now lets call all views

SELECT * FROM student_details;

SELECT * FROM student_marks;

SELECT * FROM student_performance;

SELECT * FROM paid_students;


SELECT * FROM pending_fees;

SELECT * FROM student_fee_report;

SELECT * FROM topper_students;

SELECT * FROM complete_student_report;