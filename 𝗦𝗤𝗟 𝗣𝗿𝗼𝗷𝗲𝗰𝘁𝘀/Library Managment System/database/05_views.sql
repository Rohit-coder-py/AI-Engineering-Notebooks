
--View data 


Select * from students;
Select * from library_cards;
Select * from categories;
Select * from books;
Select * from authors;


--


SELECT
    s.student_id,
    s.name,
    s.phone,
    s.email,

    lc.card_number,
    lc.issue_date,

    b.title AS book_name,
    a.author_name,
    c.category_name,

    br.borrow_date,
    br.due_date,
    br.return_date,
    br.status

FROM students s

JOIN library_cards lc
ON s.student_id = lc.student_id

LEFT JOIN borrow_records br
ON s.student_id = br.student_id

LEFT JOIN books b
ON br.book_id = b.book_id

LEFT JOIN authors a
ON b.author_id = a.author_id

LEFT JOIN categories c
ON b.category_id = c.category_id

WHERE s.name = 'Rahul Sharma';


--

SELECT
    s.student_id,
    s.name,
    s.phone,
    s.email,

    lc.card_number,
    lc.issue_date,

    b.title AS book_name,
    a.author_name,
    c.category_name,

    br.borrow_date,
    br.due_date,
    br.return_date,
    br.status

FROM students s

JOIN library_cards lc
ON s.student_id = lc.student_id

LEFT JOIN borrow_records br
ON s.student_id = br.student_id

LEFT JOIN books b
ON br.book_id = b.book_id

LEFT JOIN authors a
ON b.author_id = a.author_id

LEFT JOIN categories c
ON b.category_id = c.category_id
ORDER BY student_id DESC;



--creating view of all joined table 


CREATE VIEW all_tables AS
SELECT
    s.student_id,
    s.name,
    s.phone,
    s.email,

    lc.card_number,
    lc.issue_date,

    b.title AS book_name,
    a.author_name,
    c.category_name,

    br.borrow_date,
    br.due_date,
    br.return_date,
    br.status

FROM students s

JOIN library_cards lc
ON s.student_id = lc.student_id

LEFT JOIN borrow_records br
ON s.student_id = br.student_id

LEFT JOIN books b
ON br.book_id = b.book_id

LEFT JOIN authors a
ON b.author_id = a.author_id

LEFT JOIN categories c
ON b.category_id = c.category_id;

Select * from all_tables