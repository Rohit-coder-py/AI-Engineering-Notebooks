-- 1. Display all students
SELECT * FROM students;

-- 2. Display only student names and cities
SELECT name, city
FROM students;

-- 3. Find students from Delhi
SELECT *
FROM students
WHERE city = 'Delhi';

-- 4. Find female students
SELECT *
FROM students
WHERE gender = 'Female';

-- 5. Students admitted today
SELECT *
FROM students
WHERE admission_date = CURRENT_DATE;

-- 6. Students sorted alphabetically
SELECT *
FROM students
ORDER BY name;

-- 7. Oldest students
SELECT *
FROM students
ORDER BY dob
LIMIT 10;

-- 8. Newest students
SELECT *
FROM students
ORDER BY admission_date DESC;

-- 9. Total number of students
SELECT COUNT(*) AS total_students
FROM students;

-- 10. Students city-wise
SELECT city,
       COUNT(*) AS total_students
FROM students
GROUP BY city
ORDER BY total_students DESC;

-- 11. Gender-wise student count
SELECT gender,
       COUNT(*) AS total_students
FROM students
GROUP BY gender;

-- ============================================
-- MARKS QUERIES
-- ============================================

-- 12. Display all marks
SELECT *
FROM marks;

-- 13. Students scoring above 90
SELECT *
FROM marks
WHERE marks > 90;

-- 14. Average marks
SELECT ROUND(AVG(marks),2) AS average_marks
FROM marks;

-- 15. Highest marks
SELECT MAX(marks) AS highest_marks
FROM marks;

-- 16. Lowest marks
SELECT MIN(marks) AS lowest_marks
FROM marks;

-- 17. Subject-wise average marks
SELECT subject,
       ROUND(AVG(marks),2) AS average_marks
FROM marks
GROUP BY subject;

-- 18. Students who failed (<35)
SELECT *
FROM marks
WHERE marks < 35;

-- ============================================
-- FEES QUERIES
-- ============================================

-- 19. Display all fee records
SELECT *
FROM fees;

-- 20. Students who paid fees
SELECT *
FROM fees
WHERE status = 'Paid';

-- 21. Students with pending fees
SELECT *
FROM fees
WHERE status = 'Pending';

-- 22. Total fee collected
SELECT SUM(amount) AS total_fee_collected
FROM fees
WHERE status = 'Paid';

-- 23. Total pending fee
SELECT SUM(amount) AS pending_fee
FROM fees
WHERE status = 'Pending';

-- 24. Number of paid and pending payments
SELECT status,
       COUNT(*) AS total
FROM fees
GROUP BY status;

-- ============================================
-- JOIN QUERIES
-- ============================================

-- 25. Student details with marks
SELECT s.student_id,
       s.name,
       m.subject,
       m.marks
FROM students s
JOIN marks m
ON s.student_id = m.student_id;

-- 26. Student fee details
SELECT s.student_id,
       s.name,
       f.amount,
       f.payment_date,
       f.status
FROM students s
JOIN fees f
ON s.student_id = f.student_id;

-- 27. Students with pending fees
SELECT s.student_id,
       s.name,
       s.city,
       f.amount
FROM students s
JOIN fees f
ON s.student_id = f.student_id
WHERE f.status = 'Pending';

-- 28. Students with paid fees
SELECT s.student_id,
       s.name,
       f.payment_date,
       f.amount
FROM students s
JOIN fees f
ON s.student_id = f.student_id
WHERE f.status = 'Paid';

-- ============================================
-- AGGREGATE QUERIES
-- ============================================

-- 29. Average marks of each student
SELECT student_id,
       ROUND(AVG(marks),2) AS average_marks
FROM marks
GROUP BY student_id
ORDER BY average_marks DESC;

-- 30. Top 5 students by average marks
SELECT student_id,
       ROUND(AVG(marks),2) AS average_marks
FROM marks
GROUP BY student_id
ORDER BY average_marks DESC
LIMIT 5;

-- ============================================
-- SUBQUERY
-- ============================================

-- 31. Students scoring above overall average
SELECT *
FROM marks
WHERE marks >
(
    SELECT AVG(marks)
    FROM marks
);

-- ============================================
-- LEFT JOIN
-- ============================================

-- 32. Show every student with fee status
SELECT s.student_id,
       s.name,
       f.status
FROM students s
LEFT JOIN fees f
ON s.student_id = f.student_id;

-- ============================================
-- HAVING
-- ============================================

-- 33. Students with average marks above 80
SELECT student_id,
       ROUND(AVG(marks),2) AS average_marks
FROM marks
GROUP BY student_id
HAVING AVG(marks) > 80;

-- ============================================
-- CASE
-- ============================================

-- 34. Grade students
SELECT student_id,
       subject,
       marks,
       CASE
           WHEN marks >= 90 THEN 'A+'
           WHEN marks >= 80 THEN 'A'
           WHEN marks >= 70 THEN 'B'
           WHEN marks >= 60 THEN 'C'
           WHEN marks >= 35 THEN 'Pass'
           ELSE 'Fail'
       END AS grade
FROM marks;

-- ============================================
-- WINDOW FUNCTION
-- ============================================

-- 35. Rank students by marks
SELECT student_id,
       subject,
       marks,
       RANK() OVER(ORDER BY marks DESC) AS student_rank
FROM marks;

-- ============================================
-- SEARCH
-- ============================================

-- 36. Students whose name starts with A
SELECT *
FROM students
WHERE name LIKE 'A%';

-- 37. Gmail users
SELECT *
FROM students
WHERE email LIKE '%gmail.com';

-- ============================================
-- DATE QUERIES
-- ============================================

-- 38. Payments made in July 2026
SELECT *
FROM fees
WHERE payment_date BETWEEN '2026-07-01' AND '2026-07-31';

-- ============================================
-- MULTIPLE TABLE REPORT
-- ============================================

-- 39. Student + Marks + Fees
SELECT s.student_id,
       s.name,
       m.subject,
       m.marks,
       f.status
FROM students s
JOIN marks m
ON s.student_id = m.student_id
JOIN fees f
ON s.student_id = f.student_id;

-- ============================================
-- FINAL REPORT
-- ============================================

-- 40. Student Performance Report
SELECT
    s.student_id,
    s.name,
    s.city,
    ROUND(AVG(m.marks),2) AS average_marks,
    f.status AS fee_status
FROM students s
JOIN marks m
ON s.student_id = m.student_id
JOIN fees f
ON s.student_id = f.student_id
GROUP BY
    s.student_id,
    s.name,
    s.city,
    f.status
ORDER BY average_marks DESC;