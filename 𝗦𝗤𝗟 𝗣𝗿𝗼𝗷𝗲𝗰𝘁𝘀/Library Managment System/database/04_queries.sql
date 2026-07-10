--now we will write queries 

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

--- queries from students table 

-- 1.Show all students.
-- 2.Find a student by name.
-- 3.Count total students.
-- 4.Find students whose names start with R.
-- 5.Find students by email.


-- 1.Show all students.

Select * from students

-- 2.Find a student by name.

Select * from students 
where name = 'Rohit Kumar';


-- 3.Count total students.

Select Count(name) from students;

-- 4.Find students whose names start with R.

SELECT * FROM students
WHERE name LIKE 'R%';


-- 5.Find students by email.

Select * from students 
where email = 'rahul1@gmail.com';



===========================================================
-now queries from library_cards table 
===========================================================


1. Show all library cards.
2. Which student has which card?
3. Card issued today?
4. Count total cards.



-- 1. Show all library cards.

select * from library_cards



-- 2. Which student has which card?

Select s.student_id,s.name,card_number from students s join library_cards lc on s.student_id  = lc.student_id


-- 3. Card issued today?

Select s.student_id,s.name,lc.card_number,lc.issue_date from students s join library_cards lc on s.student_id  = lc.student_id
where issue_date = '2026-07-10'

-- 4. Count total cards.

Select Count(card_number) as total_cards from library_cards


===========================================================
-now queries from category table 
===========================================================

-- 1. Show all categories.
-- 2. Count categories.

Select * from categories

-- 2. Count categories.
Select Count(Distinct category_name ) as total_categories from  categories



===========================================================
--now queries from books table 
===========================================================

-- 1. Show all books.
-- 2.Find books published after 2000.
-- 3.Books with more than 5 copies.
-- 4.Books in Fantasy.
-- 5.Books written by J.K. Rowling

-- 1. Show all books.

Select * from books

-- 2.Find books published after 2000.


Select title,publication_year from books 
where publication_year > 2000;


-- 3.Books with more than 5 copies.

Select title , publication_year, copies_available from books 
where copies_available > 5;

-- 4.Books in Fantasy.


Select * from books
Select * from authors

SELECT


Select books.title,categories.category_name, from books join categories  on books.author_id = categories.category_id 

