

-- Students (20)
INSERT INTO students (name, phone, email) VALUES
('Rahul Sharma','9876500001','rahul1@gmail.com'),
('Priya Singh','9876500002','priya2@gmail.com'),
('Aman Verma','9876500003','aman3@gmail.com'),
('Neha Gupta','9876500004','neha4@gmail.com'),
('Rohit Kumar','9876500005','rohit5@gmail.com'),
('Anjali Mishra','9876500006','anjali6@gmail.com'),
('Vikas Yadav','9876500007','vikas7@gmail.com'),
('Pooja Patel','9876500008','pooja8@gmail.com'),
('Saurabh Rai','9876500009','saurabh9@gmail.com'),
('Sneha Das','9876500010','sneha10@gmail.com'),
('Karan Mehta','9876500011','karan11@gmail.com'),
('Riya Kapoor','9876500012','riya12@gmail.com'),
('Deepak Joshi','9876500013','deepak13@gmail.com'),
('Nisha Roy','9876500014','nisha14@gmail.com'),
('Arjun Singh','9876500015','arjun15@gmail.com'),
('Meera Shah','9876500016','meera16@gmail.com'),
('Aditya Jain','9876500017','aditya17@gmail.com'),
('Kavya Sinha','9876500018','kavya18@gmail.com'),
('Harsh Tiwari','9876500019','harsh19@gmail.com'),
('Simran Kaur','9876500020','simran20@gmail.com');

-- Library Cards (20)
INSERT INTO library_cards (student_id, card_number) VALUES
(1,'LIB1001'),(2,'LIB1002'),(3,'LIB1003'),(4,'LIB1004'),(5,'LIB1005'),
(6,'LIB1006'),(7,'LIB1007'),(8,'LIB1008'),(9,'LIB1009'),(10,'LIB1010'),
(11,'LIB1011'),(12,'LIB1012'),(13,'LIB1013'),(14,'LIB1014'),(15,'LIB1015'),
(16,'LIB1016'),(17,'LIB1017'),(18,'LIB1018'),(19,'LIB1019'),(20,'LIB1020');

-- Authors (20)
INSERT INTO authors (author_name,country) VALUES
('J.K. Rowling','UK'),
('Dan Brown','USA'),
('Chetan Bhagat','India'),
('George Orwell','UK'),
('Paulo Coelho','Brazil'),
('James Clear','USA'),
('Robert Kiyosaki','USA'),
('Yuval Noah Harari','Israel'),
('Stephen King','USA'),
('Ruskin Bond','India'),
('R.K. Narayan','India'),
('Agatha Christie','UK'),
('J.R.R. Tolkien','UK'),
('Khaled Hosseini','Afghanistan'),
('Sudha Murty','India'),
('Robin Sharma','Canada'),
('Napoleon Hill','USA'),
('Dale Carnegie','USA'),
('Jane Austen','UK'),
('Arthur Conan Doyle','UK');

-- Categories
INSERT INTO categories (category_name) VALUES
('Programming'),
('Novel'),
('Science'),
('History'),
('Finance'),
('Self Help'),
('Mystery'),
('Fantasy'),
('Biography'),
('Technology');

-- Books (20)
INSERT INTO books (title,author_id,category_id,publication_year,copies_available) VALUES
('Harry Potter',1,8,1997,5),
('Inferno',2,7,2013,4),
('Five Point Someone',3,2,2004,3),
('1984',4,2,1949,4),
('The Alchemist',5,2,1988,6),
('Atomic Habits',6,6,2018,7),
('Rich Dad Poor Dad',7,5,1997,5),
('Sapiens',8,4,2011,3),
('The Shining',9,7,1977,2),
('The Blue Umbrella',10,2,1980,4),
('Malgudi Days',11,2,1943,5),
('Murder on the Orient Express',12,7,1934,3),
('The Hobbit',13,8,1937,6),
('The Kite Runner',14,2,2003,4),
('Wise and Otherwise',15,9,2002,5),
('The Monk Who Sold His Ferrari',16,6,1997,4),
('Think and Grow Rich',17,5,1937,5),
('How to Win Friends',18,6,1936,6),
('Pride and Prejudice',19,2,1813,4),
('Sherlock Holmes',20,7,1892,5);

-- Borrow Records (20)
INSERT INTO borrow_records
(student_id,book_id,borrow_date,due_date,return_date,status) VALUES
(1,1,'2026-07-01','2026-07-15',NULL,'Borrowed'),
(2,2,'2026-06-20','2026-07-04','2026-07-03','Returned'),
(3,3,'2026-07-02','2026-07-16',NULL,'Borrowed'),
(4,4,'2026-06-10','2026-06-24','2026-06-22','Returned'),
(5,5,'2026-07-03','2026-07-17',NULL,'Borrowed'),
(6,6,'2026-07-04','2026-07-18',NULL,'Borrowed'),
(7,7,'2026-06-12','2026-06-26','2026-06-25','Returned'),
(8,8,'2026-07-05','2026-07-19',NULL,'Borrowed'),
(9,9,'2026-06-15','2026-06-29','2026-06-28','Returned'),
(10,10,'2026-07-01','2026-07-15',NULL,'Borrowed'),
(11,11,'2026-07-02','2026-07-16',NULL,'Borrowed'),
(12,12,'2026-06-18','2026-07-02','2026-07-01','Returned'),
(13,13,'2026-07-03','2026-07-17',NULL,'Borrowed'),
(14,14,'2026-06-21','2026-07-05','2026-07-04','Returned'),
(15,15,'2026-07-04','2026-07-18',NULL,'Borrowed'),
(16,16,'2026-07-05','2026-07-19',NULL,'Borrowed'),
(17,17,'2026-06-22','2026-07-06','2026-07-05','Returned'),
(18,18,'2026-07-06','2026-07-20',NULL,'Borrowed'),
(19,19,'2026-06-25','2026-07-09','2026-07-08','Returned'),
(20,20,'2026-07-06','2026-07-20',NULL,'Borrowed');
