-- Sample Data for E-Commerce Database
BEGIN;

-- Clears any existing data first so this script can be re-run safely.
-- (If this is the very first load, the tables are already empty and
-- this is a no-op.)
TRUNCATE TABLE
    reviews, shipping, payments, order_items,
    orders, inventory, products, categories, customers
RESTART IDENTITY CASCADE;

INSERT INTO categories(category_id,category_name,description) VALUES (1,'Electronics','Electronics products');
INSERT INTO categories(category_id,category_name,description) VALUES (2,'Fashion','Fashion products');
INSERT INTO categories(category_id,category_name,description) VALUES (3,'Books','Books products');
INSERT INTO categories(category_id,category_name,description) VALUES (4,'Home & Kitchen','Home & Kitchen products');
INSERT INTO categories(category_id,category_name,description) VALUES (5,'Sports','Sports products');
INSERT INTO categories(category_id,category_name,description) VALUES (6,'Beauty','Beauty products');
INSERT INTO categories(category_id,category_name,description) VALUES (7,'Toys','Toys products');
INSERT INTO categories(category_id,category_name,description) VALUES (8,'Groceries','Groceries products');
INSERT INTO categories(category_id,category_name,description) VALUES (9,'Furniture','Furniture products');
INSERT INTO categories(category_id,category_name,description) VALUES (10,'Automotive','Automotive products');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Kumar','aditya.kumar1@gmail.com','9427262400','2004-08-20','Male','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Mehta','karan.mehta2@gmail.com','9178581181','1987-04-07','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Jha','aditi.jha3@gmail.com','9488122217','1991-03-25','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Singh','vivaan.singh4@gmail.com','9669729256','1997-09-11','Male','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rahul','Jha','rahul.jha5@gmail.com','9390272619','2001-01-19','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Kumar','meera.kumar6@gmail.com','9201790292','2004-10-26','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Verma','isha.verma7@gmail.com','9565977166','1980-09-24','Male','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Yadav','aditi.yadav8@gmail.com','9104405799','2002-08-09','Other','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rahul','Patel','rahul.patel9@gmail.com','9887076892','1981-11-10','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Patel','meera.patel10@gmail.com','9868948611','2000-06-13','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Kumar','aditi.kumar11@gmail.com','9953255906','2003-10-13','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rohan','Kumar','rohan.kumar12@gmail.com','9366118315','2003-01-23','Male','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Ananya','Kumar','ananya.kumar13@gmail.com','9150603738','2003-10-22','Other','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Sneha','Kumar','sneha.kumar14@gmail.com','9756826124','2000-03-12','Male','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Gupta','arjun.gupta15@gmail.com','9367445361','2000-12-20','Male','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Kumar','karan.kumar16@gmail.com','9227371361','1983-08-18','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rohan','Yadav','rohan.yadav17@gmail.com','9304397939','1982-08-24','Female','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Singh','aditya.singh18@gmail.com','9216388512','1988-11-26','Other','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Ananya','Mehta','ananya.mehta19@gmail.com','9694465330','1995-11-07','Other','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Gupta','neha.gupta20@gmail.com','9341079174','1994-10-27','Female','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Verma','arjun.verma21@gmail.com','9473374557','1981-11-18','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Singh','neha.singh22@gmail.com','9138988283','2004-12-09','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Mehta','aditya.mehta23@gmail.com','9195210298','1987-07-07','Other','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Jha','kabir.jha24@gmail.com','9131485060','1992-03-27','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Sneha','Jha','sneha.jha25@gmail.com','9365129803','1999-01-03','Other','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Verma','isha.verma26@gmail.com','9914254044','2004-05-07','Male','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Jha','meera.jha27@gmail.com','9917795674','2001-02-01','Male','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Joshi','isha.joshi28@gmail.com','9971076829','1996-04-24','Other','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Singh','kabir.singh29@gmail.com','9785900252','1999-03-10','Other','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Yadav','isha.yadav30@gmail.com','9997487500','1983-02-12','Other','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Joshi','meera.joshi31@gmail.com','9921672449','1999-03-25','Other','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Verma','arjun.verma32@gmail.com','9799187429','1991-02-05','Male','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Verma','arjun.verma33@gmail.com','9768029395','1994-05-01','Male','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Patel','aditi.patel34@gmail.com','9434459701','1987-08-03','Other','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Gupta','kabir.gupta35@gmail.com','9133724092','1992-03-23','Female','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Priya','Verma','priya.verma36@gmail.com','9674761580','1983-03-08','Other','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Joshi','karan.joshi37@gmail.com','9583072138','2004-11-23','Other','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Verma','meera.verma38@gmail.com','9534989400','2002-04-15','Other','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Sharma','aditya.sharma39@gmail.com','9575787572','1997-10-16','Male','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rahul','Singh','rahul.singh40@gmail.com','9706152678','2002-01-01','Male','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Patel','vivaan.patel41@gmail.com','9700327185','1998-01-11','Other','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Yadav','kabir.yadav42@gmail.com','9971882006','1980-09-11','Female','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Joshi','aditi.joshi43@gmail.com','9452326133','1989-03-25','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aarav','Kumar','aarav.kumar44@gmail.com','9798640498','1999-04-21','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Jha','aditi.jha45@gmail.com','9220937750','1998-07-14','Other','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Sneha','Gupta','sneha.gupta46@gmail.com','9476149891','1991-07-02','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Gupta','isha.gupta47@gmail.com','9649948221','1984-04-26','Female','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Verma','kabir.verma48@gmail.com','9254936924','1993-09-18','Other','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rahul','Joshi','rahul.joshi49@gmail.com','9569413295','1991-01-07','Female','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Singh','arjun.singh50@gmail.com','9843454996','2004-10-09','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Yadav','aditi.yadav51@gmail.com','9834191214','1990-12-27','Male','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Verma','neha.verma52@gmail.com','9627496151','2003-03-17','Male','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Patel','kabir.patel53@gmail.com','9899305948','1988-09-27','Other','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Gupta','aditi.gupta54@gmail.com','9156145459','1993-05-09','Other','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Joshi','kabir.joshi55@gmail.com','9795938461','1986-11-18','Male','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Gupta','kabir.gupta56@gmail.com','9531097962','1991-01-26','Other','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Priya','Singh','priya.singh57@gmail.com','9311613871','1986-08-10','Male','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Joshi','aditi.joshi58@gmail.com','9644065882','2002-10-26','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Priya','Patel','priya.patel59@gmail.com','9212500233','1981-12-12','Other','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Kumar','vivaan.kumar60@gmail.com','9397260736','2003-08-18','Female','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aarav','Mehta','aarav.mehta61@gmail.com','9134555783','1990-05-15','Male','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rahul','Singh','rahul.singh62@gmail.com','9706932936','1996-01-20','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Kumar','aditi.kumar63@gmail.com','9830345945','1999-12-14','Male','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Priya','Patel','priya.patel64@gmail.com','9527910724','1996-03-08','Female','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Sneha','Yadav','sneha.yadav65@gmail.com','9434310410','1980-06-18','Female','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Arjun','Sharma','arjun.sharma66@gmail.com','9440876554','2002-09-02','Other','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Yadav','kabir.yadav67@gmail.com','9405497021','2001-05-08','Other','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Mehta','neha.mehta68@gmail.com','9845100172','1991-09-25','Female','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Sharma','kabir.sharma69@gmail.com','9416677942','1988-04-16','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Sneha','Jha','sneha.jha70@gmail.com','9260621109','1985-08-24','Female','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Jha','kabir.jha71@gmail.com','9151252419','2004-02-08','Female','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Gupta','isha.gupta72@gmail.com','9729496222','1982-02-20','Female','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rohan','Kumar','rohan.kumar73@gmail.com','9480609047','1988-03-12','Female','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Yadav','aditi.yadav74@gmail.com','9510867013','1996-08-21','Other','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Verma','karan.verma75@gmail.com','9792512502','1991-08-03','Other','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Gupta','karan.gupta76@gmail.com','9866987412','1988-11-27','Male','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Singh','vivaan.singh77@gmail.com','9109408015','1981-10-19','Female','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Gupta','vivaan.gupta78@gmail.com','9855967777','1990-11-27','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aarav','Singh','aarav.singh79@gmail.com','9642494548','1998-05-22','Male','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Kumar','kabir.kumar80@gmail.com','9611955438','1982-10-04','Female','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Mehta','aditya.mehta81@gmail.com','9589609257','1980-04-01','Male','Lucknow','Uttar Pradesh','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditi','Patel','aditi.patel82@gmail.com','9687011258','1986-04-28','Other','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Yadav','meera.yadav83@gmail.com','9280334572','2002-02-21','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Gupta','neha.gupta84@gmail.com','9474019980','1992-07-11','Female','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rohan','Singh','rohan.singh85@gmail.com','9155828014','1998-10-21','Other','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aarav','Jha','aarav.jha86@gmail.com','9407044155','1993-01-08','Male','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Joshi','karan.joshi87@gmail.com','9689480826','1983-12-10','Other','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Verma','aditya.verma88@gmail.com','9645812688','1999-10-18','Male','Chennai','Tamil Nadu','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aarav','Gupta','aarav.gupta89@gmail.com','9772116067','1992-12-12','Other','Kolkata','West Bengal','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Karan','Yadav','karan.yadav90@gmail.com','9562542206','1981-07-13','Female','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Aditya','Mehta','aditya.mehta91@gmail.com','9621627437','1983-01-27','Female','Hyderabad','Telangana','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Rohan','Kumar','rohan.kumar92@gmail.com','9392313640','1994-01-23','Male','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Neha','Yadav','neha.yadav93@gmail.com','9460575962','1988-01-13','Other','Ahmedabad','Gujarat','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Vivaan','Kumar','vivaan.kumar94@gmail.com','9800480822','1987-09-26','Female','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Ananya','Jha','ananya.jha95@gmail.com','9927002423','1997-07-05','Female','Pune','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Meera','Verma','meera.verma96@gmail.com','9529757245','1987-09-26','Male','Mumbai','Maharashtra','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Isha','Kumar','isha.kumar97@gmail.com','9837465557','1986-04-28','Female','Delhi','Delhi','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Kabir','Kumar','kabir.kumar98@gmail.com','9840886562','1982-12-25','Male','Bengaluru','Karnataka','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Ananya','Verma','ananya.verma99@gmail.com','9299741584','1998-07-11','Male','Jaipur','Rajasthan','India');
INSERT INTO customers(first_name,last_name,email,phone,date_of_birth,gender,city,state,country)
VALUES ('Priya','Patel','priya.patel100@gmail.com','9764826963','2004-11-02','Male','Hyderabad','Telangana','India');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 1','Description for Product 1','Apple',13350.88,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 2','Description for Product 2','LG',83072.17,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 3','Description for Product 3','Boat',13257.24,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 4','Description for Product 4','HP',73931.34,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 5','Description for Product 5','Puma',70974.41,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 6','Description for Product 6','Apple',5849.43,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 7','Description for Product 7','Dell',16731.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 8','Description for Product 8','Nike',27804.81,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 9','Description for Product 9','Samsung',3729.03,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 10','Description for Product 10','HP',11243.95,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 11','Description for Product 11','Samsung',68114.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 12','Description for Product 12','LG',66763.75,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 13','Description for Product 13','Adidas',2294.38,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 14','Description for Product 14','Puma',76975.09,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 15','Description for Product 15','Boat',11336.95,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 16','Description for Product 16','HP',73388.77,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 17','Description for Product 17','Apple',5203.77,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 18','Description for Product 18','Adidas',97763.75,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 19','Description for Product 19','Apple',20284.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 20','Description for Product 20','Sony',28319.35,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 21','Description for Product 21','Sony',29273.51,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 22','Description for Product 22','HP',62155.4,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 23','Description for Product 23','Dell',20504.12,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 24','Description for Product 24','Sony',80096.92,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 25','Description for Product 25','Adidas',1920.72,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 26','Description for Product 26','LG',39108.67,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 27','Description for Product 27','Nike',66865.77,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 28','Description for Product 28','HP',36316.19,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 29','Description for Product 29','HP',5130.82,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 30','Description for Product 30','Nike',15054.59,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 31','Description for Product 31','Sony',60453.55,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 32','Description for Product 32','Dell',86757.17,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 33','Description for Product 33','Nike',74453.74,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 34','Description for Product 34','Sony',78194.08,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 35','Description for Product 35','Apple',73451.62,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 36','Description for Product 36','HP',64689.88,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 37','Description for Product 37','Boat',88381.03,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 38','Description for Product 38','HP',66351.68,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 39','Description for Product 39','Dell',21956.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 40','Description for Product 40','Sony',51508.08,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 41','Description for Product 41','Boat',16752.75,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 42','Description for Product 42','Nike',23923.34,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 43','Description for Product 43','Nike',87150.34,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 44','Description for Product 44','Apple',24235.8,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 45','Description for Product 45','Apple',61376.1,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 46','Description for Product 46','HP',32057.93,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 47','Description for Product 47','LG',87244.04,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 48','Description for Product 48','Nike',61827.36,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 49','Description for Product 49','Boat',15472.39,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 50','Description for Product 50','Boat',97075.51,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 51','Description for Product 51','Dell',95368.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 52','Description for Product 52','Adidas',27776.5,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 53','Description for Product 53','HP',98775.36,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 54','Description for Product 54','LG',64733.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 55','Description for Product 55','Samsung',96328.74,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 56','Description for Product 56','LG',29071.79,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 57','Description for Product 57','Boat',26379.58,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 58','Description for Product 58','HP',70132.46,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 59','Description for Product 59','Puma',17461.62,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 60','Description for Product 60','Puma',41929.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 61','Description for Product 61','Sony',73912.06,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 62','Description for Product 62','Boat',7816.68,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 63','Description for Product 63','Puma',71156.58,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 64','Description for Product 64','Samsung',65104.42,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 65','Description for Product 65','Boat',28720.72,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 66','Description for Product 66','Dell',1527.62,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 67','Description for Product 67','Boat',497.56,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 68','Description for Product 68','Nike',62606.86,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 69','Description for Product 69','Dell',44780.81,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 70','Description for Product 70','Apple',63607.64,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 71','Description for Product 71','Dell',16451.73,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 72','Description for Product 72','Dell',32861.6,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 73','Description for Product 73','Nike',94171.62,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 74','Description for Product 74','Apple',63369.11,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 75','Description for Product 75','Boat',79081.29,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 76','Description for Product 76','LG',51661.97,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 77','Description for Product 77','Dell',80257.14,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 78','Description for Product 78','LG',66006.88,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 79','Description for Product 79','Boat',13971.12,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 80','Description for Product 80','LG',57185.42,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 81','Description for Product 81','LG',26280.48,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 82','Description for Product 82','LG',45583.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 83','Description for Product 83','Adidas',66072.83,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 84','Description for Product 84','Sony',87003.52,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 85','Description for Product 85','Nike',22068.89,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 86','Description for Product 86','Samsung',95932.28,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 87','Description for Product 87','Nike',68072.42,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 88','Description for Product 88','Boat',40242.9,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 89','Description for Product 89','Dell',13366.83,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 90','Description for Product 90','Dell',59560.1,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 91','Description for Product 91','Boat',93140.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 92','Description for Product 92','Nike',56397.35,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 93','Description for Product 93','Puma',82735.9,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 94','Description for Product 94','Nike',18664.9,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 95','Description for Product 95','HP',63949.24,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 96','Description for Product 96','Apple',94092.49,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 97','Description for Product 97','Sony',31005.91,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 98','Description for Product 98','HP',83528.76,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 99','Description for Product 99','LG',70109.35,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 100','Description for Product 100','Samsung',91903.94,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 101','Description for Product 101','Sony',93649.62,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 102','Description for Product 102','Apple',10028.79,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 103','Description for Product 103','Sony',22557.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 104','Description for Product 104','Adidas',83021.55,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 105','Description for Product 105','Dell',57674.28,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 106','Description for Product 106','Dell',62068.26,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 107','Description for Product 107','Nike',27757.71,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 108','Description for Product 108','Dell',23690.24,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 109','Description for Product 109','Apple',40956.23,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 110','Description for Product 110','HP',89814.47,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 111','Description for Product 111','HP',54505.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 112','Description for Product 112','LG',66117.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 113','Description for Product 113','Adidas',58793.89,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 114','Description for Product 114','HP',30124.72,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 115','Description for Product 115','Sony',78815.39,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 116','Description for Product 116','Samsung',49726.4,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 117','Description for Product 117','Samsung',46962.36,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 118','Description for Product 118','Sony',18703.13,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 119','Description for Product 119','Sony',26928.82,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 120','Description for Product 120','HP',84269.02,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 121','Description for Product 121','Nike',74662.92,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 122','Description for Product 122','Boat',36404.84,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 123','Description for Product 123','Apple',42426.87,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 124','Description for Product 124','Apple',6491.75,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 125','Description for Product 125','Apple',70261.63,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 126','Description for Product 126','Sony',46577.92,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 127','Description for Product 127','Apple',30902.02,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 128','Description for Product 128','Nike',10946.02,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 129','Description for Product 129','Nike',80875.25,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 130','Description for Product 130','Apple',9443.79,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 131','Description for Product 131','Nike',42707.21,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 132','Description for Product 132','Nike',64914.32,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 133','Description for Product 133','HP',88455.58,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 134','Description for Product 134','Boat',11692.03,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 135','Description for Product 135','Adidas',52291.24,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 136','Description for Product 136','Samsung',9678.98,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 137','Description for Product 137','Boat',2841.15,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 138','Description for Product 138','LG',91833.46,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 139','Description for Product 139','Boat',1670.73,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 140','Description for Product 140','Adidas',84703.11,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 141','Description for Product 141','Adidas',93971.87,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 142','Description for Product 142','HP',16971.96,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 143','Description for Product 143','HP',90884.0,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 144','Description for Product 144','Boat',86124.6,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 145','Description for Product 145','Puma',14334.15,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 146','Description for Product 146','Dell',36956.04,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 147','Description for Product 147','Boat',85439.67,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 148','Description for Product 148','Sony',55343.17,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 149','Description for Product 149','Samsung',62512.91,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 150','Description for Product 150','Nike',14821.88,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 151','Description for Product 151','Apple',99357.39,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 152','Description for Product 152','Apple',88788.31,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 153','Description for Product 153','Boat',73987.34,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 154','Description for Product 154','Boat',81259.41,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 155','Description for Product 155','Dell',87435.03,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 156','Description for Product 156','Samsung',84830.4,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 157','Description for Product 157','Samsung',55734.79,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 158','Description for Product 158','Puma',40397.2,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 159','Description for Product 159','Boat',12309.25,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 160','Description for Product 160','Apple',68030.01,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 161','Description for Product 161','Apple',79131.71,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 162','Description for Product 162','Dell',88377.05,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 163','Description for Product 163','Apple',52851.8,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 164','Description for Product 164','Samsung',25972.58,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 165','Description for Product 165','Adidas',64651.73,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 166','Description for Product 166','Boat',69727.08,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 167','Description for Product 167','Sony',24632.28,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 168','Description for Product 168','Adidas',96294.98,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 169','Description for Product 169','LG',12230.38,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 170','Description for Product 170','Nike',80207.69,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 171','Description for Product 171','Adidas',88380.35,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 172','Description for Product 172','Apple',88379.16,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 173','Description for Product 173','LG',78150.79,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 174','Description for Product 174','Boat',61889.16,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 175','Description for Product 175','Boat',25323.57,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 176','Description for Product 176','Samsung',36608.83,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 177','Description for Product 177','LG',34177.73,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 178','Description for Product 178','LG',94258.86,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 179','Description for Product 179','Adidas',17803.89,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (8,'Product 180','Description for Product 180','Adidas',29620.32,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 181','Description for Product 181','Sony',82712.46,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 182','Description for Product 182','Sony',45917.57,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 183','Description for Product 183','Dell',98410.23,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 184','Description for Product 184','Boat',99611.18,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 185','Description for Product 185','LG',18992.49,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (4,'Product 186','Description for Product 186','Apple',39075.57,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 187','Description for Product 187','Samsung',93238.7,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 188','Description for Product 188','Sony',52240.92,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (6,'Product 189','Description for Product 189','HP',67754.68,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (5,'Product 190','Description for Product 190','Apple',29674.85,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (7,'Product 191','Description for Product 191','Samsung',26086.21,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 192','Description for Product 192','Nike',54403.59,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 193','Description for Product 193','Apple',88985.04,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 194','Description for Product 194','HP',45054.93,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 195','Description for Product 195','Boat',1291.28,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (2,'Product 196','Description for Product 196','Apple',54534.43,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (9,'Product 197','Description for Product 197','Dell',98410.19,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (1,'Product 198','Description for Product 198','Puma',95043.72,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (3,'Product 199','Description for Product 199','Samsung',32120.57,'Available');
INSERT INTO products(category_id,product_name,description,brand,price,status)
VALUES (10,'Product 200','Description for Product 200','Nike',30160.89,'Available');
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (1,196,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (2,75,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (3,83,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (4,292,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (5,29,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (6,79,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (7,34,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (8,207,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (9,73,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (10,141,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (11,72,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (12,121,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (13,128,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (14,197,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (15,246,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (16,48,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (17,226,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (18,288,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (19,162,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (20,174,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (21,200,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (22,93,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (23,69,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (24,57,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (25,255,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (26,90,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (27,84,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (28,216,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (29,191,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (30,215,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (31,225,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (32,1,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (33,229,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (34,20,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (35,73,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (36,222,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (37,169,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (38,194,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (39,254,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (40,169,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (41,137,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (42,67,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (43,8,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (44,159,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (45,149,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (46,291,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (47,170,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (48,262,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (49,47,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (50,56,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (51,242,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (52,11,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (53,13,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (54,252,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (55,107,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (56,230,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (57,0,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (58,231,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (59,162,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (60,53,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (61,191,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (62,222,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (63,250,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (64,157,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (65,142,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (66,43,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (67,261,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (68,25,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (69,102,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (70,145,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (71,277,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (72,129,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (73,134,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (74,223,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (75,93,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (76,222,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (77,282,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (78,94,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (79,25,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (80,160,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (81,31,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (82,292,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (83,73,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (84,156,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (85,130,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (86,13,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (87,212,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (88,188,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (89,285,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (90,145,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (91,132,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (92,246,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (93,120,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (94,1,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (95,192,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (96,223,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (97,5,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (98,180,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (99,218,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (100,62,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (101,273,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (102,136,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (103,253,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (104,258,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (105,289,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (106,197,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (107,198,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (108,121,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (109,194,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (110,25,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (111,166,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (112,117,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (113,223,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (114,206,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (115,241,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (116,84,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (117,33,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (118,8,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (119,43,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (120,157,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (121,0,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (122,260,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (123,251,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (124,171,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (125,147,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (126,40,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (127,261,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (128,12,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (129,169,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (130,268,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (131,139,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (132,293,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (133,105,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (134,96,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (135,63,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (136,111,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (137,20,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (138,289,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (139,53,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (140,230,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (141,153,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (142,262,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (143,2,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (144,232,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (145,235,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (146,280,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (147,202,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (148,259,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (149,297,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (150,298,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (151,237,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (152,227,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (153,204,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (154,261,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (155,68,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (156,258,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (157,78,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (158,62,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (159,140,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (160,163,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (161,204,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (162,91,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (163,0,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (164,76,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (165,292,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (166,103,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (167,167,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (168,127,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (169,18,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (170,272,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (171,171,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (172,79,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (173,42,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (174,56,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (175,46,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (176,105,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (177,219,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (178,205,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (179,164,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (180,159,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (181,294,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (182,146,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (183,176,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (184,232,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (185,296,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (186,68,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (187,203,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (188,94,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (189,265,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (190,13,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (191,231,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (192,67,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (193,60,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (194,254,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (195,194,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (196,85,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (197,35,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (198,133,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (199,53,10);
INSERT INTO inventory(product_id,stock_quantity,reorder_level) VALUES (200,9,10);
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-07-23 00:00:00','Pending',4513.0);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (1,'Debit Card','Paid',4513.0);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (1,'House 845, Street 13','Chennai','Tamil Nadu','India','287928','2025-07-24','2025-07-26','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2025-04-01 00:00:00','Delivered',20096.4);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (2,'UPI','Paid',20096.4);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (2,'House 816, Street 44','Hyderabad','Telangana','India','851496','2025-04-02','2025-04-07','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (29,'2025-08-06 00:00:00','Processing',32147.66);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (3,'UPI','Paid',32147.66);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (3,'House 854, Street 41','Pune','Maharashtra','India','893676','2025-08-07','2025-08-12','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (52,'2025-07-12 00:00:00','Processing',10783.65);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (4,'UPI','Paid',10783.65);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (4,'House 73, Street 23','Kolkata','West Bengal','India','127148','2025-07-13','2025-07-15','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (33,'2025-03-02 00:00:00','Shipped',13890.68);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (5,'UPI','Paid',13890.68);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (5,'House 390, Street 19','Lucknow','Uttar Pradesh','India','931253','2025-03-03','2025-03-08','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (26,'2025-05-16 00:00:00','Cancelled',37975.89);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (6,'Debit Card','Paid',37975.89);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (6,'House 719, Street 8','Jaipur','Rajasthan','India','946877','2025-05-17','2025-05-20','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (25,'2025-04-08 00:00:00','Pending',29257.39);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (7,'Credit Card','Paid',29257.39);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (7,'House 710, Street 17','Chennai','Tamil Nadu','India','947657','2025-04-09','2025-04-11','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (55,'2025-12-20 00:00:00','Cancelled',16337.48);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (8,'Credit Card','Paid',16337.48);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (8,'House 974, Street 40','Delhi','Delhi','India','489401','2025-12-21','2025-12-24','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (27,'2025-04-27 00:00:00','Pending',48439.88);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (9,'Debit Card','Paid',48439.88);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (9,'House 418, Street 42','Jaipur','Rajasthan','India','699757','2025-04-28','2025-05-02','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2025-09-17 00:00:00','Delivered',43245.69);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (10,'Credit Card','Paid',43245.69);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (10,'House 455, Street 25','Lucknow','Uttar Pradesh','India','919898','2025-09-18','2025-09-21','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2025-01-21 00:00:00','Shipped',32607.48);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (11,'Cash on Delivery','Paid',32607.48);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (11,'House 864, Street 14','Lucknow','Uttar Pradesh','India','169406','2025-01-22','2025-01-29','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (38,'2025-05-16 00:00:00','Shipped',40881.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (12,'Net Banking','Paid',40881.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (12,'House 75, Street 47','Kolkata','West Bengal','India','284718','2025-05-17','2025-05-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (29,'2025-12-08 00:00:00','Delivered',41643.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (13,'Credit Card','Paid',41643.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (13,'House 326, Street 11','Lucknow','Uttar Pradesh','India','260343','2025-12-09','2025-12-16','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (5,'2025-09-22 00:00:00','Shipped',31379.01);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (14,'Credit Card','Paid',31379.01);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (14,'House 27, Street 40','Delhi','Delhi','India','836584','2025-09-23','2025-09-26','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2025-03-03 00:00:00','Delivered',36734.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (15,'UPI','Paid',36734.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (15,'House 405, Street 35','Kolkata','West Bengal','India','174338','2025-03-04','2025-03-07','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (10,'2026-01-12 00:00:00','Pending',3447.42);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (16,'Debit Card','Paid',3447.42);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (16,'House 898, Street 6','Mumbai','Maharashtra','India','411006','2026-01-13','2026-01-18','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (97,'2025-05-16 00:00:00','Shipped',8457.9);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (17,'Debit Card','Paid',8457.9);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (17,'House 245, Street 47','Pune','Maharashtra','India','407621','2025-05-17','2025-05-21','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (66,'2026-02-04 00:00:00','Processing',47471.09);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (18,'Debit Card','Paid',47471.09);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (18,'House 306, Street 32','Chennai','Tamil Nadu','India','783838','2026-02-05','2026-02-07','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (51,'2025-05-26 00:00:00','Shipped',12510.89);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (19,'Cash on Delivery','Paid',12510.89);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (19,'House 87, Street 17','Kolkata','West Bengal','India','702932','2025-05-27','2025-06-01','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (84,'2025-09-03 00:00:00','Delivered',46476.63);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (20,'Debit Card','Paid',46476.63);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (20,'House 658, Street 6','Kolkata','West Bengal','India','356869','2025-09-04','2025-09-08','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (7,'2025-01-22 00:00:00','Cancelled',32447.56);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (21,'Credit Card','Paid',32447.56);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (21,'House 324, Street 15','Pune','Maharashtra','India','535915','2025-01-23','2025-01-26','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (55,'2026-03-13 00:00:00','Pending',31099.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (22,'Credit Card','Paid',31099.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (22,'House 415, Street 23','Mumbai','Maharashtra','India','626281','2026-03-14','2026-03-20','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (9,'2025-01-20 00:00:00','Cancelled',32717.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (23,'Cash on Delivery','Paid',32717.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (23,'House 315, Street 43','Mumbai','Maharashtra','India','675598','2025-01-21','2025-01-27','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (25,'2025-03-02 00:00:00','Delivered',11755.41);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (24,'UPI','Paid',11755.41);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (24,'House 765, Street 34','Bengaluru','Karnataka','India','815102','2025-03-03','2025-03-10','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (88,'2025-02-11 00:00:00','Processing',20813.43);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (25,'Debit Card','Paid',20813.43);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (25,'House 825, Street 3','Pune','Maharashtra','India','869869','2025-02-12','2025-02-18','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (81,'2026-03-09 00:00:00','Shipped',30744.46);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (26,'Cash on Delivery','Paid',30744.46);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (26,'House 551, Street 18','Kolkata','West Bengal','India','504979','2026-03-10','2026-03-16','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (90,'2026-02-13 00:00:00','Cancelled',8119.19);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (27,'Net Banking','Paid',8119.19);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (27,'House 71, Street 45','Jaipur','Rajasthan','India','693717','2026-02-14','2026-02-16','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (87,'2026-02-12 00:00:00','Delivered',46439.94);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (28,'Net Banking','Paid',46439.94);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (28,'House 825, Street 21','Pune','Maharashtra','India','786927','2026-02-13','2026-02-20','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (53,'2025-05-15 00:00:00','Pending',16136.26);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (29,'Cash on Delivery','Paid',16136.26);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (29,'House 394, Street 3','Mumbai','Maharashtra','India','699628','2025-05-16','2025-05-20','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2026-04-03 00:00:00','Shipped',39395.23);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (30,'Cash on Delivery','Paid',39395.23);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (30,'House 657, Street 3','Hyderabad','Telangana','India','161684','2026-04-04','2026-04-10','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2025-12-23 00:00:00','Cancelled',30623.44);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (31,'Debit Card','Paid',30623.44);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (31,'House 924, Street 18','Bengaluru','Karnataka','India','621075','2025-12-24','2025-12-28','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (51,'2025-03-13 00:00:00','Shipped',31354.58);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (32,'Debit Card','Paid',31354.58);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (32,'House 160, Street 34','Kolkata','West Bengal','India','967828','2025-03-14','2025-03-21','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (98,'2026-03-05 00:00:00','Cancelled',39649.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (33,'Net Banking','Paid',39649.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (33,'House 197, Street 29','Hyderabad','Telangana','India','800290','2026-03-06','2026-03-12','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (27,'2026-03-27 00:00:00','Processing',32538.73);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (34,'Credit Card','Paid',32538.73);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (34,'House 434, Street 11','Delhi','Delhi','India','729208','2026-03-28','2026-04-04','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (47,'2025-07-07 00:00:00','Delivered',33775.01);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (35,'Debit Card','Paid',33775.01);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (35,'House 375, Street 38','Kolkata','West Bengal','India','938834','2025-07-08','2025-07-11','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-08-06 00:00:00','Shipped',18393.57);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (36,'Cash on Delivery','Paid',18393.57);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (36,'House 560, Street 17','Ahmedabad','Gujarat','India','851060','2025-08-07','2025-08-10','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (72,'2025-09-17 00:00:00','Shipped',37131.56);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (37,'Cash on Delivery','Paid',37131.56);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (37,'House 761, Street 13','Chennai','Tamil Nadu','India','145531','2025-09-18','2025-09-20','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (93,'2026-02-08 00:00:00','Shipped',24174.9);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (38,'Credit Card','Paid',24174.9);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (38,'House 519, Street 42','Jaipur','Rajasthan','India','945407','2026-02-09','2026-02-11','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2026-04-20 00:00:00','Processing',2425.01);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (39,'Credit Card','Paid',2425.01);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (39,'House 824, Street 29','Hyderabad','Telangana','India','693102','2026-04-21','2026-04-25','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2025-08-29 00:00:00','Processing',15879.7);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (40,'Cash on Delivery','Paid',15879.7);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (40,'House 760, Street 37','Chennai','Tamil Nadu','India','721506','2025-08-30','2025-09-01','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (64,'2025-10-01 00:00:00','Delivered',559.62);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (41,'Debit Card','Paid',559.62);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (41,'House 243, Street 3','Hyderabad','Telangana','India','624758','2025-10-02','2025-10-09','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2025-11-10 00:00:00','Processing',10703.87);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (42,'Debit Card','Paid',10703.87);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (42,'House 813, Street 12','Mumbai','Maharashtra','India','877523','2025-11-11','2025-11-15','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (55,'2026-05-08 00:00:00','Processing',42590.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (43,'Cash on Delivery','Paid',42590.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (43,'House 185, Street 18','Hyderabad','Telangana','India','818649','2026-05-09','2026-05-16','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (98,'2025-01-09 00:00:00','Cancelled',13957.18);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (44,'Credit Card','Paid',13957.18);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (44,'House 453, Street 19','Jaipur','Rajasthan','India','261996','2025-01-10','2025-01-12','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (88,'2025-07-11 00:00:00','Shipped',20092.19);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (45,'Cash on Delivery','Paid',20092.19);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (45,'House 828, Street 30','Pune','Maharashtra','India','430075','2025-07-12','2025-07-17','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2025-11-21 00:00:00','Shipped',15982.11);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (46,'Debit Card','Paid',15982.11);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (46,'House 260, Street 18','Pune','Maharashtra','India','170297','2025-11-22','2025-11-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (30,'2026-05-07 00:00:00','Cancelled',5100.15);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (47,'UPI','Paid',5100.15);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (47,'House 671, Street 44','Pune','Maharashtra','India','535109','2026-05-08','2026-05-13','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (37,'2026-04-30 00:00:00','Delivered',11742.23);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (48,'Cash on Delivery','Paid',11742.23);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (48,'House 909, Street 3','Kolkata','West Bengal','India','906339','2026-05-01','2026-05-08','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (30,'2025-09-22 00:00:00','Pending',4496.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (49,'Credit Card','Paid',4496.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (49,'House 377, Street 10','Kolkata','West Bengal','India','728732','2025-09-23','2025-09-30','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (83,'2026-03-16 00:00:00','Shipped',24410.23);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (50,'Cash on Delivery','Paid',24410.23);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (50,'House 163, Street 33','Bengaluru','Karnataka','India','814117','2026-03-17','2026-03-19','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (42,'2025-10-09 00:00:00','Pending',14242.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (51,'Debit Card','Paid',14242.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (51,'House 55, Street 35','Chennai','Tamil Nadu','India','675316','2025-10-10','2025-10-14','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (69,'2025-10-12 00:00:00','Shipped',29410.27);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (52,'Credit Card','Paid',29410.27);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (52,'House 260, Street 29','Bengaluru','Karnataka','India','678190','2025-10-13','2025-10-18','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (10,'2025-04-24 00:00:00','Cancelled',41306.54);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (53,'Cash on Delivery','Paid',41306.54);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (53,'House 533, Street 4','Mumbai','Maharashtra','India','974653','2025-04-25','2025-05-01','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (41,'2025-08-23 00:00:00','Processing',16670.19);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (54,'Credit Card','Paid',16670.19);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (54,'House 255, Street 15','Mumbai','Maharashtra','India','848424','2025-08-24','2025-08-31','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (58,'2025-04-19 00:00:00','Shipped',21919.63);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (55,'Net Banking','Paid',21919.63);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (55,'House 957, Street 44','Hyderabad','Telangana','India','162465','2025-04-20','2025-04-26','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2026-02-28 00:00:00','Shipped',34121.84);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (56,'Net Banking','Paid',34121.84);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (56,'House 682, Street 38','Lucknow','Uttar Pradesh','India','339088','2026-03-01','2026-03-07','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (90,'2026-01-08 00:00:00','Shipped',23717.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (57,'Net Banking','Paid',23717.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (57,'House 875, Street 23','Lucknow','Uttar Pradesh','India','112376','2026-01-09','2026-01-14','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (34,'2025-07-02 00:00:00','Delivered',11305.74);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (58,'UPI','Paid',11305.74);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (58,'House 594, Street 24','Bengaluru','Karnataka','India','106566','2025-07-03','2025-07-10','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-01-13 00:00:00','Processing',42850.87);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (59,'Credit Card','Paid',42850.87);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (59,'House 958, Street 4','Chennai','Tamil Nadu','India','181788','2025-01-14','2025-01-20','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (90,'2025-10-05 00:00:00','Shipped',6089.93);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (60,'Cash on Delivery','Paid',6089.93);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (60,'House 677, Street 2','Pune','Maharashtra','India','483574','2025-10-06','2025-10-12','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (41,'2026-04-28 00:00:00','Processing',39657.06);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (61,'Debit Card','Paid',39657.06);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (61,'House 601, Street 44','Kolkata','West Bengal','India','165316','2026-04-29','2026-05-01','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (44,'2025-10-24 00:00:00','Pending',24970.59);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (62,'Cash on Delivery','Paid',24970.59);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (62,'House 115, Street 18','Pune','Maharashtra','India','989402','2025-10-25','2025-10-30','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (57,'2026-02-25 00:00:00','Pending',41339.35);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (63,'Cash on Delivery','Paid',41339.35);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (63,'House 805, Street 21','Mumbai','Maharashtra','India','619110','2026-02-26','2026-03-03','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (79,'2025-09-08 00:00:00','Shipped',9016.4);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (64,'Debit Card','Paid',9016.4);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (64,'House 943, Street 37','Mumbai','Maharashtra','India','262326','2025-09-09','2025-09-16','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (87,'2026-03-17 00:00:00','Cancelled',43208.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (65,'UPI','Paid',43208.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (65,'House 867, Street 31','Lucknow','Uttar Pradesh','India','583549','2026-03-18','2026-03-22','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (56,'2025-05-10 00:00:00','Delivered',5797.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (66,'Net Banking','Paid',5797.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (66,'House 691, Street 23','Jaipur','Rajasthan','India','857217','2025-05-11','2025-05-13','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (48,'2025-09-09 00:00:00','Delivered',29156.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (67,'UPI','Paid',29156.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (67,'House 12, Street 28','Chennai','Tamil Nadu','India','684569','2025-09-10','2025-09-14','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (10,'2026-04-03 00:00:00','Processing',46015.24);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (68,'UPI','Paid',46015.24);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (68,'House 803, Street 18','Pune','Maharashtra','India','744348','2026-04-04','2026-04-07','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (11,'2025-07-14 00:00:00','Delivered',28686.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (69,'Net Banking','Paid',28686.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (69,'House 796, Street 44','Ahmedabad','Gujarat','India','762860','2025-07-15','2025-07-17','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (65,'2025-11-29 00:00:00','Cancelled',45946.01);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (70,'Cash on Delivery','Paid',45946.01);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (70,'House 211, Street 15','Kolkata','West Bengal','India','232353','2025-11-30','2025-12-04','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (47,'2025-02-02 00:00:00','Shipped',45655.43);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (71,'Debit Card','Paid',45655.43);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (71,'House 790, Street 5','Lucknow','Uttar Pradesh','India','474677','2025-02-03','2025-02-10','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2025-10-16 00:00:00','Delivered',27399.83);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (72,'Net Banking','Paid',27399.83);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (72,'House 757, Street 45','Chennai','Tamil Nadu','India','751237','2025-10-17','2025-10-24','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (11,'2025-04-09 00:00:00','Delivered',29157.73);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (73,'Cash on Delivery','Paid',29157.73);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (73,'House 959, Street 8','Mumbai','Maharashtra','India','179714','2025-04-10','2025-04-17','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (8,'2025-09-24 00:00:00','Processing',13829.48);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (74,'Debit Card','Paid',13829.48);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (74,'House 616, Street 46','Delhi','Delhi','India','148837','2025-09-25','2025-10-02','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (11,'2026-05-12 00:00:00','Shipped',20013.45);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (75,'Net Banking','Paid',20013.45);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (75,'House 238, Street 50','Ahmedabad','Gujarat','India','114997','2026-05-13','2026-05-17','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (9,'2026-01-18 00:00:00','Cancelled',48014.44);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (76,'Credit Card','Paid',48014.44);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (76,'House 426, Street 27','Jaipur','Rajasthan','India','141643','2026-01-19','2026-01-24','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (65,'2025-07-02 00:00:00','Cancelled',24302.78);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (77,'Net Banking','Paid',24302.78);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (77,'House 146, Street 36','Hyderabad','Telangana','India','555950','2025-07-03','2025-07-10','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2025-09-22 00:00:00','Processing',6132.13);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (78,'Cash on Delivery','Paid',6132.13);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (78,'House 971, Street 43','Jaipur','Rajasthan','India','194335','2025-09-23','2025-09-27','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (62,'2025-12-14 00:00:00','Pending',41341.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (79,'Cash on Delivery','Paid',41341.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (79,'House 810, Street 16','Kolkata','West Bengal','India','402717','2025-12-15','2025-12-20','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (1,'2025-03-08 00:00:00','Cancelled',36876.54);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (80,'Cash on Delivery','Paid',36876.54);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (80,'House 611, Street 1','Chennai','Tamil Nadu','India','402025','2025-03-09','2025-03-14','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2025-12-15 00:00:00','Cancelled',16467.71);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (81,'Net Banking','Paid',16467.71);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (81,'House 772, Street 33','Delhi','Delhi','India','945994','2025-12-16','2025-12-18','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (76,'2026-03-03 00:00:00','Pending',37124.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (82,'Cash on Delivery','Paid',37124.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (82,'House 378, Street 46','Mumbai','Maharashtra','India','699906','2026-03-04','2026-03-08','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (84,'2025-07-30 00:00:00','Shipped',34621.83);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (83,'Credit Card','Paid',34621.83);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (83,'House 327, Street 9','Bengaluru','Karnataka','India','312248','2025-07-31','2025-08-03','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (42,'2026-04-25 00:00:00','Pending',35070.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (84,'Debit Card','Paid',35070.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (84,'House 551, Street 40','Kolkata','West Bengal','India','291609','2026-04-26','2026-05-02','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (84,'2025-07-21 00:00:00','Cancelled',34395.94);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (85,'Net Banking','Paid',34395.94);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (85,'House 991, Street 43','Hyderabad','Telangana','India','467600','2025-07-22','2025-07-24','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (1,'2026-04-20 00:00:00','Cancelled',18216.56);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (86,'Debit Card','Paid',18216.56);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (86,'House 560, Street 17','Lucknow','Uttar Pradesh','India','708925','2026-04-21','2026-04-26','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2025-04-03 00:00:00','Pending',48418.69);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (87,'Net Banking','Paid',48418.69);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (87,'House 707, Street 22','Mumbai','Maharashtra','India','432261','2025-04-04','2025-04-06','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2025-08-26 00:00:00','Cancelled',17687.47);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (88,'Debit Card','Paid',17687.47);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (88,'House 975, Street 1','Hyderabad','Telangana','India','236947','2025-08-27','2025-08-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (2,'2025-02-20 00:00:00','Shipped',28863.52);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (89,'Credit Card','Paid',28863.52);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (89,'House 818, Street 11','Hyderabad','Telangana','India','502532','2025-02-21','2025-02-25','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (54,'2025-01-04 00:00:00','Shipped',8969.96);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (90,'UPI','Paid',8969.96);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (90,'House 43, Street 48','Ahmedabad','Gujarat','India','957918','2025-01-05','2025-01-07','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2026-03-31 00:00:00','Cancelled',18770.92);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (91,'Cash on Delivery','Paid',18770.92);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (91,'House 667, Street 46','Lucknow','Uttar Pradesh','India','258253','2026-04-01','2026-04-07','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (39,'2025-03-18 00:00:00','Cancelled',42487.34);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (92,'Net Banking','Paid',42487.34);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (92,'House 128, Street 15','Lucknow','Uttar Pradesh','India','939454','2025-03-19','2025-03-25','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (37,'2026-01-01 00:00:00','Shipped',12504.66);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (93,'Cash on Delivery','Paid',12504.66);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (93,'House 286, Street 21','Delhi','Delhi','India','323099','2026-01-02','2026-01-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (69,'2025-07-24 00:00:00','Cancelled',27048.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (94,'Net Banking','Paid',27048.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (94,'House 226, Street 41','Kolkata','West Bengal','India','450180','2025-07-25','2025-07-28','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (96,'2026-02-15 00:00:00','Pending',40280.91);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (95,'Credit Card','Paid',40280.91);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (95,'House 73, Street 47','Delhi','Delhi','India','561351','2026-02-16','2026-02-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (73,'2025-10-07 00:00:00','Cancelled',44413.06);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (96,'Credit Card','Paid',44413.06);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (96,'House 669, Street 43','Pune','Maharashtra','India','844385','2025-10-08','2025-10-10','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (28,'2025-06-21 00:00:00','Pending',13059.54);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (97,'UPI','Paid',13059.54);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (97,'House 547, Street 48','Mumbai','Maharashtra','India','431922','2025-06-22','2025-06-28','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2026-01-13 00:00:00','Shipped',26072.98);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (98,'UPI','Paid',26072.98);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (98,'House 959, Street 33','Ahmedabad','Gujarat','India','260963','2026-01-14','2026-01-20','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (14,'2025-02-17 00:00:00','Processing',5133.59);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (99,'Cash on Delivery','Paid',5133.59);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (99,'House 878, Street 11','Jaipur','Rajasthan','India','470044','2025-02-18','2025-02-23','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (55,'2025-12-22 00:00:00','Shipped',13529.44);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (100,'Debit Card','Paid',13529.44);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (100,'House 589, Street 2','Hyderabad','Telangana','India','157468','2025-12-23','2025-12-29','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (44,'2026-04-03 00:00:00','Pending',36375.47);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (101,'Credit Card','Paid',36375.47);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (101,'House 406, Street 34','Ahmedabad','Gujarat','India','440199','2026-04-04','2026-04-09','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (25,'2026-04-03 00:00:00','Processing',6346.86);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (102,'Cash on Delivery','Paid',6346.86);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (102,'House 999, Street 44','Ahmedabad','Gujarat','India','698496','2026-04-04','2026-04-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (96,'2025-11-07 00:00:00','Delivered',32455.98);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (103,'Cash on Delivery','Paid',32455.98);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (103,'House 369, Street 30','Mumbai','Maharashtra','India','316188','2025-11-08','2025-11-10','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (95,'2025-08-28 00:00:00','Shipped',27372.38);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (104,'Credit Card','Paid',27372.38);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (104,'House 830, Street 45','Mumbai','Maharashtra','India','202268','2025-08-29','2025-09-02','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (39,'2026-02-10 00:00:00','Processing',838.52);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (105,'Net Banking','Paid',838.52);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (105,'House 311, Street 19','Kolkata','West Bengal','India','660460','2026-02-11','2026-02-16','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (40,'2026-01-08 00:00:00','Shipped',21857.84);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (106,'UPI','Paid',21857.84);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (106,'House 294, Street 9','Chennai','Tamil Nadu','India','424236','2026-01-09','2026-01-11','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2025-04-14 00:00:00','Cancelled',11622.45);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (107,'Debit Card','Paid',11622.45);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (107,'House 150, Street 24','Chennai','Tamil Nadu','India','965244','2025-04-15','2025-04-21','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (63,'2025-02-22 00:00:00','Processing',13990.74);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (108,'Debit Card','Paid',13990.74);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (108,'House 313, Street 25','Jaipur','Rajasthan','India','920535','2025-02-23','2025-03-02','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2025-03-07 00:00:00','Delivered',30899.91);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (109,'Cash on Delivery','Paid',30899.91);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (109,'House 692, Street 27','Delhi','Delhi','India','544950','2025-03-08','2025-03-15','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (43,'2025-04-05 00:00:00','Pending',7980.39);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (110,'Debit Card','Paid',7980.39);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (110,'House 30, Street 36','Jaipur','Rajasthan','India','150792','2025-04-06','2025-04-09','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (20,'2026-04-03 00:00:00','Pending',39826.92);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (111,'Credit Card','Paid',39826.92);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (111,'House 437, Street 42','Bengaluru','Karnataka','India','286016','2026-04-04','2026-04-07','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (13,'2025-12-01 00:00:00','Delivered',9084.01);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (112,'Cash on Delivery','Paid',9084.01);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (112,'House 861, Street 27','Chennai','Tamil Nadu','India','772906','2025-12-02','2025-12-08','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (11,'2025-04-07 00:00:00','Delivered',36582.32);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (113,'Net Banking','Paid',36582.32);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (113,'House 939, Street 7','Lucknow','Uttar Pradesh','India','200966','2025-04-08','2025-04-12','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (43,'2025-02-22 00:00:00','Pending',33582.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (114,'Credit Card','Paid',33582.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (114,'House 657, Street 18','Kolkata','West Bengal','India','444820','2025-02-23','2025-03-02','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2026-01-01 00:00:00','Processing',25406.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (115,'Credit Card','Paid',25406.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (115,'House 709, Street 6','Chennai','Tamil Nadu','India','827429','2026-01-02','2026-01-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (81,'2026-01-24 00:00:00','Shipped',14436.41);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (116,'UPI','Paid',14436.41);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (116,'House 40, Street 48','Delhi','Delhi','India','551257','2026-01-25','2026-02-01','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (36,'2025-08-10 00:00:00','Shipped',48400.85);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (117,'Cash on Delivery','Paid',48400.85);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (117,'House 180, Street 48','Chennai','Tamil Nadu','India','167474','2025-08-11','2025-08-14','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2025-05-02 00:00:00','Shipped',42888.52);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (118,'Credit Card','Paid',42888.52);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (118,'House 411, Street 29','Lucknow','Uttar Pradesh','India','383632','2025-05-03','2025-05-06','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-07-06 00:00:00','Processing',30776.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (119,'Net Banking','Paid',30776.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (119,'House 394, Street 39','Kolkata','West Bengal','India','617366','2025-07-07','2025-07-11','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2025-05-23 00:00:00','Cancelled',942.19);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (120,'Debit Card','Paid',942.19);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (120,'House 282, Street 6','Bengaluru','Karnataka','India','460121','2025-05-24','2025-05-29','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2026-02-06 00:00:00','Delivered',25064.81);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (121,'Cash on Delivery','Paid',25064.81);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (121,'House 950, Street 30','Kolkata','West Bengal','India','274413','2026-02-07','2026-02-14','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (32,'2025-11-24 00:00:00','Cancelled',27816.09);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (122,'Debit Card','Paid',27816.09);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (122,'House 469, Street 40','Mumbai','Maharashtra','India','933606','2025-11-25','2025-11-30','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (38,'2025-07-03 00:00:00','Pending',42974.45);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (123,'Cash on Delivery','Paid',42974.45);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (123,'House 545, Street 30','Kolkata','West Bengal','India','831219','2025-07-04','2025-07-07','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (76,'2025-09-22 00:00:00','Delivered',41622.47);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (124,'Cash on Delivery','Paid',41622.47);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (124,'House 122, Street 44','Hyderabad','Telangana','India','612282','2025-09-23','2025-09-30','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (20,'2025-12-03 00:00:00','Shipped',9689.41);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (125,'Net Banking','Paid',9689.41);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (125,'House 526, Street 18','Hyderabad','Telangana','India','514239','2025-12-04','2025-12-06','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (95,'2025-06-27 00:00:00','Delivered',47941.35);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (126,'UPI','Paid',47941.35);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (126,'House 249, Street 42','Kolkata','West Bengal','India','942944','2025-06-28','2025-06-30','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (32,'2025-07-15 00:00:00','Shipped',47991.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (127,'UPI','Paid',47991.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (127,'House 287, Street 12','Hyderabad','Telangana','India','972112','2025-07-16','2025-07-21','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (92,'2025-11-05 00:00:00','Shipped',7064.88);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (128,'Net Banking','Paid',7064.88);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (128,'House 269, Street 31','Mumbai','Maharashtra','India','567892','2025-11-06','2025-11-11','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (100,'2025-11-14 00:00:00','Processing',23505.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (129,'Debit Card','Paid',23505.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (129,'House 472, Street 36','Ahmedabad','Gujarat','India','514025','2025-11-15','2025-11-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (91,'2025-01-27 00:00:00','Shipped',33213.43);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (130,'Cash on Delivery','Paid',33213.43);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (130,'House 634, Street 4','Kolkata','West Bengal','India','842924','2025-01-28','2025-02-02','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2026-05-11 00:00:00','Processing',6235.29);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (131,'Net Banking','Paid',6235.29);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (131,'House 870, Street 28','Mumbai','Maharashtra','India','963556','2026-05-12','2026-05-19','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (66,'2025-12-07 00:00:00','Shipped',34911.6);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (132,'Cash on Delivery','Paid',34911.6);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (132,'House 26, Street 5','Ahmedabad','Gujarat','India','410799','2025-12-08','2025-12-15','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2025-10-02 00:00:00','Pending',38596.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (133,'UPI','Paid',38596.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (133,'House 889, Street 30','Bengaluru','Karnataka','India','311181','2025-10-03','2025-10-08','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (70,'2025-09-04 00:00:00','Processing',45009.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (134,'Credit Card','Paid',45009.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (134,'House 4, Street 39','Bengaluru','Karnataka','India','100938','2025-09-05','2025-09-12','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (1,'2025-06-29 00:00:00','Processing',29577.93);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (135,'UPI','Paid',29577.93);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (135,'House 156, Street 29','Chennai','Tamil Nadu','India','144107','2025-06-30','2025-07-03','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (75,'2025-05-29 00:00:00','Delivered',21778.2);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (136,'Debit Card','Paid',21778.2);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (136,'House 367, Street 32','Pune','Maharashtra','India','349579','2025-05-30','2025-06-05','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (34,'2025-09-22 00:00:00','Cancelled',1852.58);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (137,'UPI','Paid',1852.58);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (137,'House 518, Street 4','Delhi','Delhi','India','894550','2025-09-23','2025-09-28','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (43,'2025-01-19 00:00:00','Pending',11373.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (138,'Cash on Delivery','Paid',11373.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (138,'House 803, Street 49','Pune','Maharashtra','India','149497','2025-01-20','2025-01-22','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (45,'2025-11-20 00:00:00','Delivered',22177.37);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (139,'Cash on Delivery','Paid',22177.37);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (139,'House 690, Street 49','Mumbai','Maharashtra','India','704140','2025-11-21','2025-11-25','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (80,'2025-04-14 00:00:00','Cancelled',49822.42);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (140,'UPI','Paid',49822.42);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (140,'House 60, Street 21','Mumbai','Maharashtra','India','120594','2025-04-15','2025-04-17','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (54,'2025-08-20 00:00:00','Shipped',29302.04);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (141,'Credit Card','Paid',29302.04);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (141,'House 958, Street 3','Delhi','Delhi','India','277758','2025-08-21','2025-08-23','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (5,'2025-06-26 00:00:00','Shipped',37017.72);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (142,'Credit Card','Paid',37017.72);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (142,'House 415, Street 17','Kolkata','West Bengal','India','444707','2025-06-27','2025-06-30','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (74,'2025-11-17 00:00:00','Processing',38381.32);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (143,'Cash on Delivery','Paid',38381.32);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (143,'House 555, Street 8','Hyderabad','Telangana','India','114243','2025-11-18','2025-11-22','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (94,'2025-08-13 00:00:00','Cancelled',48729.09);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (144,'Net Banking','Paid',48729.09);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (144,'House 468, Street 6','Pune','Maharashtra','India','278876','2025-08-14','2025-08-19','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (9,'2025-05-27 00:00:00','Delivered',38506.71);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (145,'Cash on Delivery','Paid',38506.71);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (145,'House 904, Street 11','Kolkata','West Bengal','India','433502','2025-05-28','2025-06-04','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-09-08 00:00:00','Delivered',24324.53);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (146,'Net Banking','Paid',24324.53);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (146,'House 600, Street 50','Kolkata','West Bengal','India','247730','2025-09-09','2025-09-12','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-04-21 00:00:00','Shipped',45422.24);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (147,'Cash on Delivery','Paid',45422.24);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (147,'House 455, Street 38','Mumbai','Maharashtra','India','318141','2025-04-22','2025-04-27','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2026-01-26 00:00:00','Shipped',29367.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (148,'Cash on Delivery','Paid',29367.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (148,'House 224, Street 2','Pune','Maharashtra','India','318681','2026-01-27','2026-01-30','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (49,'2025-12-10 00:00:00','Delivered',45423.54);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (149,'Cash on Delivery','Paid',45423.54);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (149,'House 287, Street 5','Kolkata','West Bengal','India','601641','2025-12-11','2025-12-16','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (61,'2025-09-16 00:00:00','Processing',4288.11);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (150,'Net Banking','Paid',4288.11);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (150,'House 52, Street 17','Ahmedabad','Gujarat','India','740695','2025-09-17','2025-09-22','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (48,'2025-04-12 00:00:00','Processing',29595.69);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (151,'Debit Card','Paid',29595.69);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (151,'House 460, Street 14','Jaipur','Rajasthan','India','653931','2025-04-13','2025-04-17','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (22,'2025-03-20 00:00:00','Cancelled',47693.67);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (152,'UPI','Paid',47693.67);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (152,'House 809, Street 36','Bengaluru','Karnataka','India','260341','2025-03-21','2025-03-24','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2025-06-12 00:00:00','Delivered',10179.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (153,'Net Banking','Paid',10179.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (153,'House 584, Street 41','Hyderabad','Telangana','India','402928','2025-06-13','2025-06-19','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (42,'2025-05-19 00:00:00','Shipped',28975.91);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (154,'UPI','Paid',28975.91);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (154,'House 450, Street 14','Ahmedabad','Gujarat','India','715428','2025-05-20','2025-05-25','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (7,'2025-07-07 00:00:00','Shipped',33009.54);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (155,'Net Banking','Paid',33009.54);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (155,'House 32, Street 1','Hyderabad','Telangana','India','702592','2025-07-08','2025-07-13','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2026-03-12 00:00:00','Cancelled',10927.84);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (156,'Debit Card','Paid',10927.84);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (156,'House 641, Street 29','Ahmedabad','Gujarat','India','675700','2026-03-13','2026-03-20','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2026-01-17 00:00:00','Cancelled',12968.82);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (157,'Credit Card','Paid',12968.82);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (157,'House 997, Street 30','Delhi','Delhi','India','812522','2026-01-18','2026-01-22','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (79,'2025-11-17 00:00:00','Cancelled',45354.89);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (158,'Cash on Delivery','Paid',45354.89);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (158,'House 120, Street 27','Chennai','Tamil Nadu','India','658405','2025-11-18','2025-11-22','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (56,'2025-10-16 00:00:00','Pending',22165.23);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (159,'UPI','Paid',22165.23);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (159,'House 659, Street 35','Bengaluru','Karnataka','India','987422','2025-10-17','2025-10-21','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (69,'2025-11-18 00:00:00','Pending',40970.05);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (160,'Net Banking','Paid',40970.05);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (160,'House 660, Street 3','Mumbai','Maharashtra','India','189990','2025-11-19','2025-11-24','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (9,'2025-03-23 00:00:00','Shipped',38505.03);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (161,'Cash on Delivery','Paid',38505.03);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (161,'House 183, Street 26','Chennai','Tamil Nadu','India','880374','2025-03-24','2025-03-31','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (50,'2025-05-08 00:00:00','Delivered',49955.36);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (162,'Net Banking','Paid',49955.36);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (162,'House 827, Street 3','Bengaluru','Karnataka','India','681637','2025-05-09','2025-05-16','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2025-03-02 00:00:00','Pending',44198.94);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (163,'Net Banking','Paid',44198.94);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (163,'House 6, Street 39','Bengaluru','Karnataka','India','502889','2025-03-03','2025-03-09','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (67,'2026-01-21 00:00:00','Pending',24518.41);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (164,'Cash on Delivery','Paid',24518.41);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (164,'House 606, Street 1','Jaipur','Rajasthan','India','396431','2026-01-22','2026-01-26','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (71,'2025-08-30 00:00:00','Cancelled',24525.63);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (165,'Net Banking','Paid',24525.63);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (165,'House 915, Street 48','Hyderabad','Telangana','India','399421','2025-08-31','2025-09-06','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2025-03-14 00:00:00','Shipped',22232.17);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (166,'Credit Card','Paid',22232.17);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (166,'House 32, Street 41','Mumbai','Maharashtra','India','750999','2025-03-15','2025-03-21','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2025-06-25 00:00:00','Processing',46315.96);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (167,'Net Banking','Paid',46315.96);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (167,'House 85, Street 34','Jaipur','Rajasthan','India','106925','2025-06-26','2025-06-29','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-10-15 00:00:00','Cancelled',2147.55);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (168,'Credit Card','Paid',2147.55);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (168,'House 607, Street 18','Ahmedabad','Gujarat','India','763222','2025-10-16','2025-10-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2026-01-04 00:00:00','Processing',46386.56);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (169,'UPI','Paid',46386.56);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (169,'House 426, Street 8','Delhi','Delhi','India','910854','2026-01-05','2026-01-12','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (59,'2026-04-07 00:00:00','Shipped',14394.76);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (170,'Debit Card','Paid',14394.76);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (170,'House 30, Street 38','Kolkata','West Bengal','India','307477','2026-04-08','2026-04-13','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2025-10-01 00:00:00','Cancelled',40573.47);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (171,'Cash on Delivery','Paid',40573.47);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (171,'House 641, Street 50','Bengaluru','Karnataka','India','725186','2025-10-02','2025-10-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (22,'2025-01-03 00:00:00','Shipped',10479.44);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (172,'Credit Card','Paid',10479.44);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (172,'House 825, Street 28','Mumbai','Maharashtra','India','583222','2025-01-04','2025-01-08','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (84,'2026-02-06 00:00:00','Pending',18015.24);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (173,'UPI','Paid',18015.24);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (173,'House 171, Street 19','Kolkata','West Bengal','India','289877','2026-02-07','2026-02-10','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (23,'2025-02-28 00:00:00','Shipped',37836.65);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (174,'UPI','Paid',37836.65);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (174,'House 162, Street 19','Bengaluru','Karnataka','India','488747','2025-03-01','2025-03-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (63,'2025-09-10 00:00:00','Pending',35121.78);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (175,'Cash on Delivery','Paid',35121.78);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (175,'House 544, Street 10','Ahmedabad','Gujarat','India','265677','2025-09-11','2025-09-16','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (92,'2025-01-24 00:00:00','Delivered',10503.56);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (176,'Net Banking','Paid',10503.56);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (176,'House 493, Street 46','Kolkata','West Bengal','India','304564','2025-01-25','2025-01-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (31,'2025-02-09 00:00:00','Delivered',12079.0);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (177,'Net Banking','Paid',12079.0);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (177,'House 737, Street 4','Lucknow','Uttar Pradesh','India','334295','2025-02-10','2025-02-15','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2025-09-07 00:00:00','Delivered',42738.33);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (178,'UPI','Paid',42738.33);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (178,'House 984, Street 2','Lucknow','Uttar Pradesh','India','191659','2025-09-08','2025-09-10','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (95,'2025-12-22 00:00:00','Pending',13791.38);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (179,'Credit Card','Paid',13791.38);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (179,'House 291, Street 1','Bengaluru','Karnataka','India','981996','2025-12-23','2025-12-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (26,'2025-08-08 00:00:00','Cancelled',29603.17);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (180,'Debit Card','Paid',29603.17);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (180,'House 593, Street 45','Kolkata','West Bengal','India','569959','2025-08-09','2025-08-11','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (33,'2025-04-22 00:00:00','Cancelled',30013.67);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (181,'Debit Card','Paid',30013.67);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (181,'House 877, Street 36','Mumbai','Maharashtra','India','542061','2025-04-23','2025-04-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (57,'2026-01-18 00:00:00','Processing',26224.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (182,'Net Banking','Paid',26224.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (182,'House 15, Street 13','Ahmedabad','Gujarat','India','880837','2026-01-19','2026-01-25','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (46,'2025-12-04 00:00:00','Cancelled',16453.6);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (183,'Credit Card','Paid',16453.6);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (183,'House 217, Street 46','Mumbai','Maharashtra','India','502160','2025-12-05','2025-12-11','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (48,'2025-05-21 00:00:00','Cancelled',12199.37);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (184,'Net Banking','Paid',12199.37);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (184,'House 465, Street 50','Hyderabad','Telangana','India','601238','2025-05-22','2025-05-26','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (23,'2025-12-21 00:00:00','Shipped',26991.49);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (185,'Net Banking','Paid',26991.49);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (185,'House 867, Street 43','Delhi','Delhi','India','911894','2025-12-22','2025-12-29','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (54,'2025-06-28 00:00:00','Processing',36401.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (186,'Debit Card','Paid',36401.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (186,'House 505, Street 43','Mumbai','Maharashtra','India','759083','2025-06-29','2025-07-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (31,'2025-12-27 00:00:00','Shipped',31803.23);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (187,'Cash on Delivery','Paid',31803.23);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (187,'House 448, Street 47','Ahmedabad','Gujarat','India','121294','2025-12-28','2026-01-01','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (76,'2025-05-03 00:00:00','Cancelled',4840.61);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (188,'Credit Card','Paid',4840.61);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (188,'House 960, Street 47','Hyderabad','Telangana','India','665107','2025-05-04','2025-05-08','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (51,'2025-03-02 00:00:00','Cancelled',13022.27);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (189,'Net Banking','Paid',13022.27);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (189,'House 716, Street 22','Delhi','Delhi','India','128850','2025-03-03','2025-03-07','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (16,'2025-02-25 00:00:00','Shipped',19945.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (190,'UPI','Paid',19945.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (190,'House 329, Street 31','Pune','Maharashtra','India','133456','2025-02-26','2025-02-28','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (24,'2025-02-10 00:00:00','Pending',6317.84);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (191,'Cash on Delivery','Paid',6317.84);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (191,'House 24, Street 11','Bengaluru','Karnataka','India','455651','2025-02-11','2025-02-16','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (9,'2026-04-08 00:00:00','Shipped',32609.28);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (192,'UPI','Paid',32609.28);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (192,'House 37, Street 30','Chennai','Tamil Nadu','India','849744','2026-04-09','2026-04-14','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (55,'2025-11-03 00:00:00','Pending',28678.95);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (193,'Net Banking','Paid',28678.95);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (193,'House 236, Street 34','Mumbai','Maharashtra','India','631350','2025-11-04','2025-11-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-06-25 00:00:00','Processing',42335.18);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (194,'UPI','Paid',42335.18);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (194,'House 510, Street 41','Delhi','Delhi','India','820057','2025-06-26','2025-06-29','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (82,'2025-07-26 00:00:00','Pending',15895.18);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (195,'UPI','Paid',15895.18);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (195,'House 914, Street 10','Kolkata','West Bengal','India','297367','2025-07-27','2025-08-02','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (5,'2025-10-03 00:00:00','Shipped',31247.53);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (196,'UPI','Paid',31247.53);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (196,'House 638, Street 6','Pune','Maharashtra','India','718441','2025-10-04','2025-10-08','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (1,'2026-04-30 00:00:00','Delivered',40596.67);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (197,'Credit Card','Paid',40596.67);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (197,'House 23, Street 1','Hyderabad','Telangana','India','575738','2026-05-01','2026-05-06','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (16,'2025-04-12 00:00:00','Pending',40606.81);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (198,'Net Banking','Paid',40606.81);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (198,'House 384, Street 19','Pune','Maharashtra','India','952640','2025-04-13','2025-04-20','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (74,'2025-07-15 00:00:00','Cancelled',38313.5);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (199,'UPI','Paid',38313.5);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (199,'House 499, Street 18','Pune','Maharashtra','India','119794','2025-07-16','2025-07-23','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (81,'2025-04-10 00:00:00','Pending',10745.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (200,'UPI','Paid',10745.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (200,'House 115, Street 3','Chennai','Tamil Nadu','India','523297','2025-04-11','2025-04-15','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (31,'2025-04-14 00:00:00','Processing',2106.47);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (201,'UPI','Paid',2106.47);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (201,'House 323, Street 30','Ahmedabad','Gujarat','India','115351','2025-04-15','2025-04-19','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-07-02 00:00:00','Cancelled',9662.12);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (202,'Debit Card','Paid',9662.12);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (202,'House 476, Street 44','Lucknow','Uttar Pradesh','India','634970','2025-07-03','2025-07-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (92,'2026-03-06 00:00:00','Shipped',45869.73);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (203,'Credit Card','Paid',45869.73);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (203,'House 863, Street 13','Mumbai','Maharashtra','India','991341','2026-03-07','2026-03-09','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (10,'2026-01-26 00:00:00','Cancelled',12410.09);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (204,'Cash on Delivery','Paid',12410.09);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (204,'House 538, Street 1','Kolkata','West Bengal','India','847039','2026-01-27','2026-01-31','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-08-11 00:00:00','Processing',2316.55);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (205,'Credit Card','Paid',2316.55);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (205,'House 440, Street 18','Delhi','Delhi','India','874351','2025-08-12','2025-08-17','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (97,'2025-01-29 00:00:00','Pending',29853.4);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (206,'Debit Card','Paid',29853.4);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (206,'House 648, Street 47','Hyderabad','Telangana','India','442652','2025-01-30','2025-02-02','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2025-10-25 00:00:00','Pending',41522.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (207,'UPI','Paid',41522.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (207,'House 586, Street 14','Ahmedabad','Gujarat','India','433430','2025-10-26','2025-10-31','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (61,'2025-05-30 00:00:00','Delivered',30176.08);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (208,'UPI','Paid',30176.08);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (208,'House 151, Street 41','Lucknow','Uttar Pradesh','India','179557','2025-05-31','2025-06-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (76,'2025-05-10 00:00:00','Shipped',45269.95);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (209,'Debit Card','Paid',45269.95);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (209,'House 854, Street 8','Lucknow','Uttar Pradesh','India','269761','2025-05-11','2025-05-14','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2025-08-08 00:00:00','Processing',24704.73);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (210,'Debit Card','Paid',24704.73);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (210,'House 754, Street 14','Chennai','Tamil Nadu','India','117123','2025-08-09','2025-08-15','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (52,'2025-12-24 00:00:00','Processing',12222.25);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (211,'Credit Card','Paid',12222.25);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (211,'House 109, Street 40','Delhi','Delhi','India','420537','2025-12-25','2025-12-29','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (98,'2026-04-30 00:00:00','Delivered',44260.59);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (212,'Debit Card','Paid',44260.59);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (212,'House 188, Street 32','Jaipur','Rajasthan','India','818606','2026-05-01','2026-05-05','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2026-01-30 00:00:00','Delivered',17940.24);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (213,'UPI','Paid',17940.24);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (213,'House 980, Street 1','Jaipur','Rajasthan','India','588256','2026-01-31','2026-02-05','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (79,'2026-01-15 00:00:00','Pending',26247.96);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (214,'Debit Card','Paid',26247.96);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (214,'House 260, Street 13','Delhi','Delhi','India','194862','2026-01-16','2026-01-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (79,'2025-11-16 00:00:00','Cancelled',4681.27);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (215,'UPI','Paid',4681.27);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (215,'House 28, Street 32','Ahmedabad','Gujarat','India','184875','2025-11-17','2025-11-23','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (88,'2025-03-29 00:00:00','Processing',5679.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (216,'Net Banking','Paid',5679.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (216,'House 932, Street 31','Delhi','Delhi','India','798440','2025-03-30','2025-04-02','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (45,'2026-03-20 00:00:00','Cancelled',39465.2);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (217,'Credit Card','Paid',39465.2);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (217,'House 192, Street 26','Delhi','Delhi','India','195267','2026-03-21','2026-03-23','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (3,'2025-01-31 00:00:00','Shipped',44481.33);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (218,'Debit Card','Paid',44481.33);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (218,'House 33, Street 33','Ahmedabad','Gujarat','India','836582','2025-02-01','2025-02-04','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (67,'2025-02-01 00:00:00','Delivered',16908.09);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (219,'Net Banking','Paid',16908.09);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (219,'House 185, Street 17','Delhi','Delhi','India','484543','2025-02-02','2025-02-09','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-01-26 00:00:00','Delivered',23381.95);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (220,'Debit Card','Paid',23381.95);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (220,'House 998, Street 8','Jaipur','Rajasthan','India','511547','2025-01-27','2025-02-02','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (68,'2025-10-15 00:00:00','Delivered',9246.87);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (221,'UPI','Paid',9246.87);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (221,'House 594, Street 19','Kolkata','West Bengal','India','588520','2025-10-16','2025-10-19','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (28,'2026-04-06 00:00:00','Pending',16433.15);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (222,'Net Banking','Paid',16433.15);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (222,'House 52, Street 46','Lucknow','Uttar Pradesh','India','363336','2026-04-07','2026-04-13','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (21,'2025-12-27 00:00:00','Delivered',43721.37);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (223,'Debit Card','Paid',43721.37);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (223,'House 645, Street 3','Bengaluru','Karnataka','India','924555','2025-12-28','2026-01-04','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (31,'2026-04-02 00:00:00','Shipped',48606.92);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (224,'Net Banking','Paid',48606.92);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (224,'House 641, Street 16','Hyderabad','Telangana','India','883183','2026-04-03','2026-04-10','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (17,'2025-07-16 00:00:00','Pending',33229.2);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (225,'Net Banking','Paid',33229.2);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (225,'House 556, Street 16','Ahmedabad','Gujarat','India','378878','2025-07-17','2025-07-20','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (7,'2025-04-22 00:00:00','Pending',48246.62);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (226,'Credit Card','Paid',48246.62);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (226,'House 258, Street 1','Hyderabad','Telangana','India','591724','2025-04-23','2025-04-25','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (18,'2026-02-24 00:00:00','Delivered',43275.83);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (227,'UPI','Paid',43275.83);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (227,'House 793, Street 45','Kolkata','West Bengal','India','368201','2026-02-25','2026-02-28','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (67,'2025-07-05 00:00:00','Pending',3572.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (228,'Cash on Delivery','Paid',3572.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (228,'House 562, Street 6','Jaipur','Rajasthan','India','224483','2025-07-06','2025-07-12','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (8,'2025-01-29 00:00:00','Processing',16918.99);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (229,'UPI','Paid',16918.99);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (229,'House 332, Street 11','Mumbai','Maharashtra','India','430693','2025-01-30','2025-02-01','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (70,'2025-04-08 00:00:00','Shipped',46352.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (230,'UPI','Paid',46352.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (230,'House 29, Street 32','Chennai','Tamil Nadu','India','695747','2025-04-09','2025-04-14','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (48,'2026-01-23 00:00:00','Shipped',45657.4);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (231,'Credit Card','Paid',45657.4);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (231,'House 832, Street 47','Jaipur','Rajasthan','India','584746','2026-01-24','2026-01-28','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (57,'2026-05-14 00:00:00','Cancelled',49872.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (232,'Credit Card','Paid',49872.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (232,'House 295, Street 2','Kolkata','West Bengal','India','507329','2026-05-15','2026-05-17','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (100,'2026-05-12 00:00:00','Processing',46112.31);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (233,'Cash on Delivery','Paid',46112.31);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (233,'House 709, Street 38','Pune','Maharashtra','India','203460','2026-05-13','2026-05-19','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (18,'2026-05-16 00:00:00','Shipped',6260.28);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (234,'UPI','Paid',6260.28);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (234,'House 881, Street 27','Pune','Maharashtra','India','842719','2026-05-17','2026-05-19','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (28,'2026-02-28 00:00:00','Pending',13395.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (235,'Debit Card','Paid',13395.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (235,'House 806, Street 22','Bengaluru','Karnataka','India','275281','2026-03-01','2026-03-08','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (18,'2026-04-18 00:00:00','Processing',49743.46);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (236,'Cash on Delivery','Paid',49743.46);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (236,'House 502, Street 13','Pune','Maharashtra','India','122324','2026-04-19','2026-04-26','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (2,'2025-10-30 00:00:00','Shipped',33486.22);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (237,'Net Banking','Paid',33486.22);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (237,'House 738, Street 2','Pune','Maharashtra','India','461713','2025-10-31','2025-11-02','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (61,'2026-01-11 00:00:00','Cancelled',2860.27);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (238,'Credit Card','Paid',2860.27);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (238,'House 719, Street 28','Lucknow','Uttar Pradesh','India','997854','2026-01-12','2026-01-15','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (93,'2025-08-25 00:00:00','Pending',36445.11);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (239,'Cash on Delivery','Paid',36445.11);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (239,'House 764, Street 24','Mumbai','Maharashtra','India','465511','2025-08-26','2025-08-31','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (36,'2025-01-16 00:00:00','Cancelled',33111.73);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (240,'Credit Card','Paid',33111.73);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (240,'House 772, Street 15','Delhi','Delhi','India','617042','2025-01-17','2025-01-24','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (8,'2025-03-28 00:00:00','Shipped',31312.6);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (241,'Credit Card','Paid',31312.6);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (241,'House 300, Street 35','Jaipur','Rajasthan','India','713216','2025-03-29','2025-04-02','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-12-23 00:00:00','Cancelled',9004.21);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (242,'UPI','Paid',9004.21);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (242,'House 657, Street 37','Delhi','Delhi','India','777790','2025-12-24','2025-12-31','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (43,'2026-05-04 00:00:00','Pending',11564.87);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (243,'UPI','Paid',11564.87);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (243,'House 811, Street 30','Lucknow','Uttar Pradesh','India','569935','2026-05-05','2026-05-12','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (73,'2025-01-29 00:00:00','Cancelled',38264.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (244,'Cash on Delivery','Paid',38264.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (244,'House 577, Street 6','Hyderabad','Telangana','India','216354','2025-01-30','2025-02-05','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (56,'2025-03-19 00:00:00','Shipped',29260.38);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (245,'Debit Card','Paid',29260.38);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (245,'House 66, Street 34','Pune','Maharashtra','India','382070','2025-03-20','2025-03-23','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (52,'2025-09-28 00:00:00','Cancelled',34910.36);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (246,'Net Banking','Paid',34910.36);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (246,'House 236, Street 29','Jaipur','Rajasthan','India','460647','2025-09-29','2025-10-05','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (22,'2025-02-20 00:00:00','Cancelled',32808.82);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (247,'Cash on Delivery','Paid',32808.82);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (247,'House 814, Street 27','Bengaluru','Karnataka','India','224380','2025-02-21','2025-02-27','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (81,'2025-02-28 00:00:00','Shipped',35760.91);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (248,'Net Banking','Paid',35760.91);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (248,'House 426, Street 2','Kolkata','West Bengal','India','990937','2025-03-01','2025-03-06','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (40,'2026-02-19 00:00:00','Cancelled',21904.05);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (249,'Cash on Delivery','Paid',21904.05);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (249,'House 250, Street 31','Lucknow','Uttar Pradesh','India','999578','2026-02-20','2026-02-25','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (14,'2025-06-09 00:00:00','Pending',46098.18);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (250,'Net Banking','Paid',46098.18);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (250,'House 484, Street 49','Delhi','Delhi','India','492696','2025-06-10','2025-06-12','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (84,'2025-12-29 00:00:00','Shipped',14058.02);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (251,'Net Banking','Paid',14058.02);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (251,'House 826, Street 38','Ahmedabad','Gujarat','India','197077','2025-12-30','2026-01-04','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (93,'2025-02-01 00:00:00','Cancelled',13711.68);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (252,'Net Banking','Paid',13711.68);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (252,'House 759, Street 21','Jaipur','Rajasthan','India','114999','2025-02-02','2025-02-04','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-06-27 00:00:00','Processing',10733.75);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (253,'UPI','Paid',10733.75);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (253,'House 971, Street 7','Bengaluru','Karnataka','India','273220','2025-06-28','2025-07-03','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (21,'2025-11-14 00:00:00','Pending',43862.78);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (254,'Net Banking','Paid',43862.78);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (254,'House 808, Street 13','Kolkata','West Bengal','India','492850','2025-11-15','2025-11-18','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (96,'2025-06-02 00:00:00','Shipped',21027.25);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (255,'Cash on Delivery','Paid',21027.25);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (255,'House 989, Street 4','Jaipur','Rajasthan','India','732322','2025-06-03','2025-06-06','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (83,'2025-01-20 00:00:00','Delivered',38368.99);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (256,'Net Banking','Paid',38368.99);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (256,'House 113, Street 2','Pune','Maharashtra','India','829857','2025-01-21','2025-01-25','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (90,'2026-04-04 00:00:00','Delivered',3439.59);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (257,'Cash on Delivery','Paid',3439.59);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (257,'House 852, Street 15','Bengaluru','Karnataka','India','835685','2026-04-05','2026-04-10','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2025-05-24 00:00:00','Cancelled',41981.32);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (258,'Debit Card','Paid',41981.32);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (258,'House 67, Street 24','Hyderabad','Telangana','India','553273','2025-05-25','2025-05-27','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (92,'2025-06-03 00:00:00','Pending',22592.29);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (259,'UPI','Paid',22592.29);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (259,'House 599, Street 7','Pune','Maharashtra','India','405679','2025-06-04','2025-06-11','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (12,'2025-12-22 00:00:00','Processing',43937.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (260,'Cash on Delivery','Paid',43937.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (260,'House 847, Street 48','Pune','Maharashtra','India','694262','2025-12-23','2025-12-29','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2025-08-20 00:00:00','Shipped',41339.9);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (261,'Debit Card','Paid',41339.9);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (261,'House 894, Street 35','Pune','Maharashtra','India','998478','2025-08-21','2025-08-24','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (74,'2025-03-29 00:00:00','Cancelled',18522.85);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (262,'Debit Card','Paid',18522.85);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (262,'House 322, Street 10','Mumbai','Maharashtra','India','451451','2025-03-30','2025-04-05','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (2,'2026-03-09 00:00:00','Pending',16174.2);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (263,'Debit Card','Paid',16174.2);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (263,'House 70, Street 43','Delhi','Delhi','India','938002','2026-03-10','2026-03-13','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (73,'2025-02-12 00:00:00','Pending',10854.35);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (264,'Debit Card','Paid',10854.35);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (264,'House 610, Street 16','Jaipur','Rajasthan','India','266208','2025-02-13','2025-02-17','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (18,'2025-10-24 00:00:00','Processing',12302.49);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (265,'UPI','Paid',12302.49);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (265,'House 436, Street 15','Bengaluru','Karnataka','India','438805','2025-10-25','2025-10-27','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (64,'2025-07-07 00:00:00','Shipped',8998.61);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (266,'Credit Card','Paid',8998.61);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (266,'House 972, Street 29','Chennai','Tamil Nadu','India','577824','2025-07-08','2025-07-11','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (99,'2025-01-24 00:00:00','Delivered',45597.13);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (267,'Debit Card','Paid',45597.13);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (267,'House 286, Street 7','Lucknow','Uttar Pradesh','India','523828','2025-01-25','2025-01-30','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (38,'2025-11-27 00:00:00','Delivered',42788.07);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (268,'Debit Card','Paid',42788.07);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (268,'House 795, Street 17','Chennai','Tamil Nadu','India','410938','2025-11-28','2025-12-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (29,'2025-12-25 00:00:00','Processing',8134.55);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (269,'UPI','Paid',8134.55);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (269,'House 415, Street 33','Pune','Maharashtra','India','227964','2025-12-26','2026-01-02','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-09-23 00:00:00','Pending',39630.93);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (270,'Net Banking','Paid',39630.93);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (270,'House 347, Street 32','Delhi','Delhi','India','215819','2025-09-24','2025-09-28','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (52,'2025-05-01 00:00:00','Delivered',2239.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (271,'Debit Card','Paid',2239.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (271,'House 117, Street 14','Kolkata','West Bengal','India','244151','2025-05-02','2025-05-05','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (21,'2025-10-02 00:00:00','Cancelled',39884.8);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (272,'Debit Card','Paid',39884.8);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (272,'House 915, Street 47','Delhi','Delhi','India','939542','2025-10-03','2025-10-05','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (78,'2025-11-04 00:00:00','Delivered',14519.13);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (273,'Net Banking','Paid',14519.13);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (273,'House 964, Street 28','Bengaluru','Karnataka','India','303522','2025-11-05','2025-11-08','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (66,'2025-10-05 00:00:00','Processing',9386.0);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (274,'Credit Card','Paid',9386.0);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (274,'House 172, Street 1','Chennai','Tamil Nadu','India','436181','2025-10-06','2025-10-09','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-10-23 00:00:00','Shipped',30683.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (275,'Cash on Delivery','Paid',30683.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (275,'House 652, Street 33','Delhi','Delhi','India','709695','2025-10-24','2025-10-27','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (64,'2025-06-20 00:00:00','Shipped',37450.67);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (276,'Debit Card','Paid',37450.67);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (276,'House 292, Street 21','Chennai','Tamil Nadu','India','520172','2025-06-21','2025-06-25','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (26,'2025-09-01 00:00:00','Shipped',29134.25);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (277,'Credit Card','Paid',29134.25);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (277,'House 803, Street 30','Ahmedabad','Gujarat','India','894627','2025-09-02','2025-09-09','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (100,'2025-07-28 00:00:00','Cancelled',10520.39);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (278,'Debit Card','Paid',10520.39);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (278,'House 60, Street 2','Chennai','Tamil Nadu','India','620329','2025-07-29','2025-08-04','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (53,'2026-02-11 00:00:00','Processing',27168.3);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (279,'Credit Card','Paid',27168.3);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (279,'House 487, Street 49','Bengaluru','Karnataka','India','992942','2026-02-12','2026-02-19','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (19,'2026-03-21 00:00:00','Pending',40266.22);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (280,'Net Banking','Paid',40266.22);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (280,'House 126, Street 47','Lucknow','Uttar Pradesh','India','645395','2026-03-22','2026-03-27','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2025-04-10 00:00:00','Cancelled',44698.97);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (281,'UPI','Paid',44698.97);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (281,'House 979, Street 39','Bengaluru','Karnataka','India','164255','2025-04-11','2025-04-13','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (1,'2026-03-29 00:00:00','Delivered',40251.83);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (282,'Credit Card','Paid',40251.83);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (282,'House 893, Street 30','Pune','Maharashtra','India','746869','2026-03-30','2026-04-03','Shipped');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (85,'2025-10-10 00:00:00','Pending',23528.94);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (283,'Credit Card','Paid',23528.94);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (283,'House 1, Street 25','Kolkata','West Bengal','India','215907','2025-10-11','2025-10-14','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (81,'2025-03-18 00:00:00','Cancelled',18072.51);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (284,'Net Banking','Paid',18072.51);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (284,'House 333, Street 8','Kolkata','West Bengal','India','303381','2025-03-19','2025-03-24','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2025-11-30 00:00:00','Cancelled',26843.77);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (285,'UPI','Paid',26843.77);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (285,'House 848, Street 17','Delhi','Delhi','India','954148','2025-12-01','2025-12-05','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (23,'2025-12-26 00:00:00','Pending',23115.66);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (286,'UPI','Paid',23115.66);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (286,'House 49, Street 27','Mumbai','Maharashtra','India','943821','2025-12-27','2026-01-02','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (93,'2026-02-11 00:00:00','Processing',18106.08);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (287,'UPI','Paid',18106.08);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (287,'House 12, Street 38','Pune','Maharashtra','India','817804','2026-02-12','2026-02-18','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (4,'2026-02-24 00:00:00','Cancelled',44152.11);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (288,'Debit Card','Paid',44152.11);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (288,'House 874, Street 5','Hyderabad','Telangana','India','948645','2026-02-25','2026-03-01','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (64,'2026-03-05 00:00:00','Cancelled',39767.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (289,'Credit Card','Paid',39767.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (289,'House 648, Street 7','Jaipur','Rajasthan','India','219719','2026-03-06','2026-03-13','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (74,'2025-02-26 00:00:00','Delivered',10486.27);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (290,'Credit Card','Paid',10486.27);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (290,'House 131, Street 33','Ahmedabad','Gujarat','India','820025','2025-02-27','2025-03-03','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (60,'2025-07-18 00:00:00','Processing',44791.43);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (291,'Cash on Delivery','Paid',44791.43);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (291,'House 127, Street 40','Pune','Maharashtra','India','653921','2025-07-19','2025-07-22','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (100,'2025-09-19 00:00:00','Shipped',8014.78);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (292,'Cash on Delivery','Paid',8014.78);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (292,'House 916, Street 23','Ahmedabad','Gujarat','India','699516','2025-09-20','2025-09-25','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (86,'2025-12-10 00:00:00','Processing',25238.21);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (293,'Debit Card','Paid',25238.21);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (293,'House 262, Street 24','Kolkata','West Bengal','India','334683','2025-12-11','2025-12-15','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (66,'2025-07-07 00:00:00','Pending',13295.25);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (294,'UPI','Paid',13295.25);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (294,'House 908, Street 15','Pune','Maharashtra','India','180527','2025-07-08','2025-07-14','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (66,'2025-12-16 00:00:00','Delivered',45721.2);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (295,'Net Banking','Paid',45721.2);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (295,'House 871, Street 49','Pune','Maharashtra','India','463568','2025-12-17','2025-12-22','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (94,'2025-01-18 00:00:00','Pending',17453.16);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (296,'Credit Card','Paid',17453.16);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (296,'House 484, Street 22','Kolkata','West Bengal','India','645462','2025-01-19','2025-01-25','Delivered');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (77,'2025-10-22 00:00:00','Delivered',9770.31);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (297,'UPI','Paid',9770.31);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (297,'House 839, Street 24','Bengaluru','Karnataka','India','322312','2025-10-23','2025-10-30','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (3,'2025-02-19 00:00:00','Processing',26937.22);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (298,'Net Banking','Paid',26937.22);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (298,'House 199, Street 23','Pune','Maharashtra','India','792400','2025-02-20','2025-02-23','In Transit');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (89,'2025-02-11 00:00:00','Shipped',28890.79);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (299,'Credit Card','Paid',28890.79);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (299,'House 635, Street 15','Hyderabad','Telangana','India','443879','2025-02-12','2025-02-18','Preparing');
INSERT INTO orders(customer_id,order_date,order_status,total_amount) VALUES (35,'2025-07-03 00:00:00','Processing',5363.29);
INSERT INTO payments(order_id,payment_method,payment_status,amount) VALUES (300,'Cash on Delivery','Paid',5363.29);
INSERT INTO shipping(order_id,address,city,state,country,postal_code,shipping_date,delivery_date,shipping_status)
VALUES (300,'House 679, Street 12','Chennai','Tamil Nadu','India','716244','2025-07-04','2025-07-10','Delivered');
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (77,25,3,86837.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (225,2,5,80296.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (140,87,5,65751.48);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (251,79,5,81015.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (258,37,3,22319.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,15,3,40817.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (32,171,3,88446.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (243,116,3,26184.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (15,163,3,84400.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (145,96,2,78238.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (29,146,1,11461.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (119,90,3,61515.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (68,142,5,49791.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (153,72,1,70108.47);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (102,127,2,32410.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,168,1,19350.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (204,139,1,59942.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (232,141,5,48469.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (69,154,5,61248.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (40,93,1,55579.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (249,127,4,61911.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,198,3,95741.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (47,58,4,56059.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (89,194,5,4990.5);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (80,136,2,53772.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (131,52,5,14174.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (168,145,5,43673.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (237,4,1,11175.71);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (110,123,1,82091.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (207,149,5,22660.32);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (124,95,3,98538.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (135,177,5,29663.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (78,91,4,99148.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (11,70,4,73221.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (13,113,3,5871.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (173,200,4,82376.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (138,32,3,84886.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (196,8,4,89195.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (216,151,2,12399.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (210,12,2,22538.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (36,177,1,67308.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (202,5,2,10735.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (22,21,1,79074.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (80,62,5,4784.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (9,1,4,16981.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (114,36,5,26760.07);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (124,84,3,13504.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (256,162,3,89449.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (50,45,4,27046.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (267,47,2,3156.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (213,97,4,26949.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (213,181,4,65651.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (279,3,1,31447.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (212,46,3,75378.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (44,29,5,95594.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (267,92,2,1733.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (226,127,5,77110.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (290,104,4,61628.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (221,89,4,63886.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (175,113,1,54842.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (221,98,5,27053.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (85,65,5,46608.61);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (189,72,2,58573.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (158,109,1,56778.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (35,87,1,69686.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,157,3,88188.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (128,104,3,13002.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (3,117,1,83087.25);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (13,68,3,54582.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,57,2,4013.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (277,132,1,65005.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (53,38,5,83955.32);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,112,3,89407.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (151,113,2,57551.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,179,4,97527.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (164,81,3,81883.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (270,160,2,28531.23);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (105,154,1,80846.61);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (220,27,3,50994.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (226,20,1,64709.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (221,22,1,40433.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (200,117,1,48610.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (107,141,3,2916.5);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (217,38,4,63460.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,132,4,17584.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (81,121,4,80076.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (77,121,5,20036.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (258,88,1,74155.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (102,187,2,91258.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (47,106,1,66393.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (246,197,2,50468.14);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,67,4,31851.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (24,154,4,36106.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (239,107,2,45537.56);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,22,1,76589.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (51,122,5,52705.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (60,46,1,73306.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (125,104,3,86332.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,123,1,11810.08);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (284,118,3,46396.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (149,10,4,52231.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (297,121,4,43428.5);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (237,26,2,23813.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,161,5,74451.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (12,73,2,68802.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,160,3,93732.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (204,2,3,38167.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (196,16,1,252.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (101,120,5,14745.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (67,44,5,70047.48);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (214,55,2,17681.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (141,150,3,53715.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (281,146,3,17971.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (208,174,4,83575.48);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (230,173,3,905.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (168,144,5,9443.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (143,84,5,47850.13);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (276,26,2,79050.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (50,39,5,79363.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (156,112,5,73017.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (24,156,2,29582.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (292,41,4,97197.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (74,7,2,2597.3);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (138,124,1,24506.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (9,70,3,16500.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (116,65,2,22730.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (43,32,3,41965.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (258,61,5,26245.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,116,3,42259.04);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,4,1,79907.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (20,172,1,27268.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (266,118,3,67560.58);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,101,4,31099.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (57,88,4,67880.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (37,150,2,65997.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (178,153,2,71086.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (271,119,5,7859.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (203,91,1,10902.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (248,196,4,69354.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (201,161,3,90433.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (121,189,1,83272.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (154,72,2,62490.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (251,188,1,75543.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (81,36,1,78985.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (18,98,2,55575.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (237,45,3,87203.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (86,150,4,24607.3);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,161,4,51004.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (111,29,2,13684.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (164,67,3,37535.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (66,64,2,17593.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (252,56,1,72116.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (289,107,1,56501.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (99,138,3,76846.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (93,22,1,52257.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (51,53,1,78927.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (133,152,2,84310.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (114,115,5,74992.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (19,124,4,46795.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (244,184,1,78693.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (123,97,3,14412.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,143,2,78739.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (122,191,2,67350.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (274,98,5,14292.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (121,156,3,51969.47);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (181,121,3,24549.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (82,115,5,77812.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,170,3,79432.04);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (113,158,5,65609.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (143,192,3,57354.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,19,2,62862.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (273,121,4,16022.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (107,61,4,76031.23);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (175,91,4,16028.33);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (98,169,5,9892.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (18,2,1,3460.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (203,144,3,71304.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (182,67,2,59008.29);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (142,166,2,75595.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (203,94,4,25594.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (42,1,2,28993.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (80,186,1,97505.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (153,129,2,84342.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (128,114,1,82361.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (145,170,4,10904.09);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (294,16,4,22029.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,43,5,48994.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,110,1,27325.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (81,161,4,46251.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (201,103,1,68046.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (33,146,4,51041.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (270,53,2,98430.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (275,90,2,30111.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (243,14,4,35593.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (167,181,2,87885.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (149,137,3,13270.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (47,127,2,30385.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (115,131,1,9091.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (270,74,4,70922.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (122,133,4,38070.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (27,111,3,64240.29);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (28,65,5,81276.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,77,5,51046.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (290,172,5,18720.04);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (204,22,1,56831.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (292,19,1,8234.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,27,5,20552.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (189,66,2,47113.53);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (63,83,4,72343.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (152,13,1,28726.91);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (204,162,2,94147.14);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,189,1,17471.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (207,63,1,68802.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (227,161,1,73154.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,96,5,58393.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (210,120,1,35340.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (133,158,3,67465.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (280,114,2,84767.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (69,19,2,67190.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (38,8,3,60982.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (175,130,3,47833.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (216,137,4,14630.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (120,112,2,89809.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,48,4,56747.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (39,98,3,8358.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (66,27,4,91229.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (244,167,4,75625.67);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (223,139,1,20992.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (31,169,2,55456.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (198,2,3,70316.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (91,107,4,81215.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,46,3,83322.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (118,143,5,19273.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (126,19,4,29635.61);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (52,58,3,74104.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (134,44,4,56271.33);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (193,71,4,58017.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (287,61,2,87569.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (1,110,5,56690.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (7,49,3,63782.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (179,79,2,36795.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,137,4,72461.25);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (273,85,1,65646.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (193,17,2,71380.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (298,176,1,32278.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (237,34,5,14872.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (19,30,3,42971.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (34,18,1,56105.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (231,192,2,51637.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (39,169,2,25073.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (37,100,2,97048.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (108,136,5,48053.25);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (98,55,1,15446.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (274,42,2,21922.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (17,58,5,7468.08);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (279,8,4,95227.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (156,27,2,92859.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (130,162,1,36918.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (36,118,3,90477.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (244,100,5,65895.13);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (175,115,1,36108.47);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (133,158,5,64524.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (57,127,2,87386.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (168,93,5,52264.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (6,179,5,37848.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (197,148,1,56864.88);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (272,65,2,75135.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (283,151,3,3419.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (201,103,4,96516.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,149,2,94090.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,150,2,46301.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (228,8,5,84689.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (107,106,3,54858.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (85,153,3,79575.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,25,5,98436.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,141,4,97495.19);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (19,149,2,6485.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (287,55,3,1001.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (164,65,5,28809.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (57,181,1,77939.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (20,76,3,12095.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,170,1,90452.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (170,96,3,56877.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (262,20,4,62308.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (215,84,2,68762.09);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (238,108,4,8138.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (149,58,2,71269.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (128,110,3,99311.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,120,2,90690.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (136,155,2,7603.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (43,27,5,94718.5);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (18,128,5,46671.19);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (79,59,4,11453.95);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (139,55,5,96938.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (37,10,2,1283.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (167,198,5,88934.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (1,103,5,9435.14);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (224,132,3,17381.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,57,4,38271.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (110,48,4,36407.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (76,41,3,96093.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,91,1,69540.91);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (108,64,5,92834.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (229,53,1,90408.89);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (98,45,2,4571.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (154,2,4,77340.71);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (21,79,1,22709.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (154,48,5,19490.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (282,109,4,73138.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (37,77,4,95706.5);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,77,4,55154.08);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (149,153,5,34654.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,120,2,17760.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (28,41,4,35360.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (86,61,5,26591.53);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (17,76,5,56128.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,50,2,15495.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (153,127,1,95115.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (102,72,5,18453.89);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (217,143,5,54815.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (246,133,1,85503.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (117,23,5,41824.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (245,56,4,12729.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (180,78,2,26594.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (282,88,4,11794.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (269,18,1,1560.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (300,6,1,93381.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (139,87,2,33779.13);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (245,63,4,853.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (240,8,5,52590.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (6,158,3,58716.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (107,18,3,70796.46);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (149,28,4,38127.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (197,150,1,80064.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (36,11,3,87660.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (33,198,4,97250.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (220,193,5,14297.04);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (93,95,5,6410.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (61,71,2,85479.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (97,20,3,91028.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (143,160,2,18872.48);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (5,29,4,28200.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (215,200,5,84112.39);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (244,33,2,26805.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (237,166,5,92893.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (192,117,3,41235.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (262,93,2,23164.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (182,157,5,9297.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (254,80,3,93421.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (77,20,4,579.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (166,100,3,72369.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (238,94,2,57001.23);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (265,180,4,45481.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (88,103,1,25574.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (170,113,1,54202.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (135,198,5,46556.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (295,52,2,65787.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (36,193,2,18061.96);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (19,167,2,23018.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (81,143,2,56286.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (27,59,4,69316.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (110,165,3,11624.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (221,80,3,30709.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (26,175,2,60983.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (134,49,2,45362.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (258,2,1,79744.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (262,80,1,35555.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,64,1,31757.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (54,32,1,24539.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (176,78,4,31093.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (115,97,3,95515.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (217,158,2,63855.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (247,199,5,62194.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (94,173,3,57585.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (253,7,3,784.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (102,99,5,49804.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (235,193,3,31054.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,72,4,26600.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (215,109,2,1850.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (245,49,1,25467.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (185,33,1,78614.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (219,134,3,42599.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (58,171,3,21003.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (164,135,2,56988.61);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (62,179,5,36076.2);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (245,35,4,58101.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (119,69,1,29610.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (143,155,3,11446.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (64,95,4,1528.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (151,2,5,89289.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (140,157,4,34161.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (75,53,4,48204.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (25,148,2,91251.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (40,151,3,93877.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (285,138,3,17046.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,91,5,94738.47);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (1,13,1,4028.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (138,9,4,78677.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (211,181,4,12112.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (88,72,3,88606.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (66,45,2,23162.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (42,68,4,14813.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,63,5,11734.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (275,87,1,96735.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (274,14,1,19536.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (141,150,3,83634.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (108,113,3,22783.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (84,58,4,28940.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (115,143,2,47538.91);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (71,67,1,97946.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (239,194,4,99255.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (230,19,5,16921.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (139,16,2,79643.13);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (181,87,1,79768.87);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (82,109,1,36956.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (174,58,1,6100.78);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (34,188,5,72249.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,156,3,22337.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (51,137,4,13190.88);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (238,84,2,81240.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (108,145,2,59241.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,80,4,31526.88);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,84,4,10138.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (112,29,1,7354.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (185,138,5,27308.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (9,165,1,12220.89);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (5,66,4,72662.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (98,185,1,11581.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,130,1,91226.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (105,51,1,45350.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (207,74,4,34696.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (154,165,2,69398.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (181,191,2,19656.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (193,165,4,29453.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (70,138,5,89933.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (284,23,4,95240.39);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (236,194,4,29031.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (294,198,2,87191.47);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (89,97,4,94616.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (144,162,1,79491.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (56,143,1,97982.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (124,142,5,86255.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (219,166,5,71841.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (269,18,4,16586.3);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (62,55,1,97664.65);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (34,104,5,87391.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (13,171,3,83940.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (50,181,1,87512.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (181,5,1,80659.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (210,129,1,49145.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (270,56,3,24605.89);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (289,71,4,41011.96);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (63,17,3,44555.71);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (168,62,5,87188.71);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (147,152,2,85803.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (62,58,5,36668.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,165,2,24110.19);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (91,128,2,9146.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (152,193,3,8252.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (45,126,5,12245.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,159,2,59729.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (55,99,2,84848.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (20,89,3,8771.41);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (215,18,4,97926.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (168,164,5,6487.1);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (28,118,4,85997.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (231,112,2,49646.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (75,54,4,85440.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (188,98,5,35696.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (261,153,3,98920.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (246,108,1,92546.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (41,40,4,36690.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,117,5,89084.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (300,22,1,30577.73);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (220,23,1,79863.09);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (231,109,5,31715.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (148,151,4,60222.05);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (287,142,2,24069.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (230,99,2,79985.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (228,195,1,59852.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,114,4,86082.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (43,112,4,58405.29);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (5,166,1,48963.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (186,169,2,92579.88);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (244,152,1,40397.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (236,86,4,35681.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (238,102,4,27476.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (185,117,5,15537.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (223,56,4,15126.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (148,128,1,80547.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (215,173,2,41014.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (289,12,5,80850.96);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,153,3,44490.04);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (122,135,3,49890.61);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (9,21,4,65326.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (200,169,2,21310.39);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (138,51,4,69838.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (123,134,5,73948.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (296,170,3,42014.95);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (153,41,2,90524.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (290,22,2,54578.74);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (161,10,3,34129.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (187,191,3,67918.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,38,1,30333.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (143,90,1,91790.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (289,156,1,87547.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (35,115,5,84964.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (6,65,3,24475.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (174,139,4,99555.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (202,42,2,22306.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (135,15,4,45968.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (2,137,1,37652.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,192,2,83656.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (278,137,5,97553.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (63,83,4,2349.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (169,153,4,77519.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (209,136,1,89216.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (116,42,2,85126.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (107,119,2,80055.22);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (167,59,1,18202.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (48,153,1,52334.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (123,77,4,11308.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (290,26,1,59724.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (223,91,5,58127.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,114,2,12477.99);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (195,61,4,44353.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (187,193,5,89726.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (145,178,4,47867.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (129,117,3,48770.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (276,49,2,94335.01);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (219,62,1,60258.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (225,25,1,44333.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (214,60,5,48717.58);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (135,141,1,41758.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,179,5,62442.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (186,32,3,11553.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (45,96,2,51237.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (56,10,4,90176.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (27,85,4,68129.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (101,173,5,85292.07);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (122,180,3,84083.25);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (269,159,1,72044.32);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (193,86,3,5637.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (113,62,1,42308.28);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (57,67,1,4323.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (234,81,1,53166.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (60,105,3,31692.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (293,2,5,62524.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (249,187,3,90015.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (34,151,1,4778.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (25,50,2,27830.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (125,187,5,51267.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,119,5,57206.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (96,77,3,10288.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (276,14,3,55599.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (152,102,4,13627.08);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (288,85,3,84884.23);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (44,30,1,90768.6);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (150,166,1,27033.93);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (240,150,2,42951.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (262,133,2,9229.88);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (111,63,5,57386.89);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (281,45,5,42737.53);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (177,108,2,92604.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,34,3,94509.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (120,31,2,43893.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (162,34,1,85710.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (210,103,2,55745.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (240,36,3,1942.57);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (268,12,5,90236.69);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (25,99,2,19626.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (211,9,4,91759.48);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (97,123,4,34816.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (32,72,3,66935.3);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,137,3,63970.58);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,64,3,91154.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,169,1,32492.96);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (259,131,3,51453.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (246,16,4,72399.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (216,189,3,79581.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (284,129,4,71786.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,126,1,2776.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (283,174,5,20971.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (87,147,3,40688.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (199,18,5,16510.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (216,51,4,37561.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,96,5,19336.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,94,5,90963.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (169,175,3,34001.07);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (300,65,3,8294.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (79,160,5,29028.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (293,26,3,96367.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (224,15,4,38111.83);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (200,39,4,37206.66);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (276,183,1,69195.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (100,162,2,712.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (201,83,3,79277.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (217,56,3,45273.85);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (285,193,1,85343.31);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (284,55,3,34987.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (206,25,3,78106.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (179,165,1,70268.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (90,26,3,4075.97);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (11,149,3,87736.92);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (272,166,4,89043.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (60,77,4,87274.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (26,3,4,28034.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (196,24,4,17329.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (131,66,1,50776.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (137,195,4,45887.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (225,155,1,3293.38);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (235,48,5,14978.95);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (101,186,4,62315.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (40,61,3,12507.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (266,28,4,58489.75);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (92,138,4,77169.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (290,138,1,45911.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (135,105,3,19280.39);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (158,189,1,33260.07);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (16,53,1,19561.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,143,1,56019.14);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (157,72,3,29604.51);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (300,145,5,11254.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (220,35,2,62037.82);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (201,91,1,51185.52);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (195,103,4,13184.15);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (163,198,4,65704.06);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (257,13,3,32759.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,50,4,85437.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (282,68,2,21533.27);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (261,132,5,58409.79);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (118,137,2,66280.12);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (195,120,2,29216.21);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (192,20,4,57001.72);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (98,120,2,74393.07);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (193,139,5,98798.3);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (23,63,3,68315.62);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (69,166,5,62755.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (255,22,3,40961.34);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (264,168,5,83397.84);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (247,179,4,56004.09);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,3,2,90866.81);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (212,166,4,29942.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (89,61,1,18128.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (78,71,5,36737.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (190,17,4,83960.29);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (267,180,5,86620.02);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (109,48,4,73451.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (194,28,5,1839.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (127,93,2,57331.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (31,134,3,53390.9);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (242,190,4,18913.63);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (264,21,2,47993.76);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (66,78,1,6536.59);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (10,195,4,17336.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (56,108,1,56491.66);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (110,128,1,65296.43);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (202,72,3,6032.16);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (124,190,4,1208.0);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (45,151,4,94187.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (208,126,1,99087.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (295,140,4,98607.39);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (179,199,3,26247.8);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (60,195,1,41249.49);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (267,74,1,46436.68);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (242,37,4,62963.44);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (300,110,3,80457.42);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (191,168,2,71771.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (280,197,1,89484.37);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (49,4,5,86779.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (262,39,5,85967.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (182,92,2,30812.35);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (256,183,4,82228.03);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (14,9,2,47426.54);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (241,109,3,1983.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (5,130,2,1570.24);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (63,64,4,85553.64);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (114,94,1,59710.77);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,115,4,69142.26);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (71,138,5,5918.86);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (220,74,2,758.4);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (171,128,2,32507.66);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (169,93,4,47935.96);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (114,128,2,14589.7);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (5,88,1,67858.09);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (69,87,2,42415.67);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (157,126,4,39506.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (187,114,4,8920.18);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (164,9,5,89802.14);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (81,191,5,22396.36);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (156,35,1,92833.55);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (173,146,5,11691.45);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (283,126,3,62718.08);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (226,120,2,25910.94);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (8,76,3,31575.71);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (101,96,4,95072.11);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (251,98,1,46898.98);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (4,160,4,78179.13);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (64,55,1,37939.17);
INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES (41,22,5,23895.71);
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,184,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (57,149,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (21,173,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,16,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,15,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (88,135,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (43,85,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (73,36,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (47,140,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (35,3,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,45,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (1,117,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,123,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,162,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,66,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,165,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,20,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,145,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,114,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (98,46,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (48,142,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,46,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (51,21,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (17,56,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,71,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (82,16,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,107,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,15,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,51,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (42,122,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (82,181,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,179,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,141,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,130,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (37,77,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (18,190,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,173,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,194,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (63,95,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (47,176,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (33,119,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,9,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (58,121,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (87,180,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,85,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (4,191,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (81,153,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (90,108,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (97,14,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (57,103,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,111,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,103,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (65,116,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,53,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,54,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,98,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (83,159,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,175,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (35,176,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (13,99,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (43,23,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,114,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,86,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,160,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (21,78,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,175,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,152,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,9,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,125,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (18,167,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,59,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,95,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,195,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,123,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (52,27,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,168,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,182,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,135,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,166,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (68,182,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,139,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,142,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (3,60,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,121,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (18,196,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,166,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,112,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,36,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,89,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,189,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,63,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,39,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (63,22,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,146,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,81,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,120,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,177,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (65,141,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,51,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,40,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (13,192,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (23,118,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (57,11,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (64,115,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (43,82,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,44,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,32,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,107,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (89,77,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (46,124,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (52,87,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,54,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (69,170,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,91,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,125,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,195,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,134,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,179,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,43,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,7,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,56,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,28,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (43,193,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (69,102,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (85,94,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,70,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,112,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,137,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,130,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,92,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,123,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,169,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,187,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (35,110,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,17,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (78,45,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,116,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (72,86,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (78,115,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (9,34,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (61,41,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (80,142,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (82,92,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,119,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,170,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (49,81,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (4,140,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,171,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (9,179,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,81,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (46,54,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (71,145,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (3,63,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,187,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,106,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,79,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (88,81,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,157,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (16,77,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (89,52,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,193,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (2,191,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (94,134,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,106,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,41,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (10,119,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (42,160,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (73,168,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,190,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,112,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,159,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (13,38,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,9,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,131,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (83,157,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,35,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (32,123,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (89,191,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (10,186,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,65,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (46,48,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (3,51,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,192,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (63,142,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,156,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,17,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,177,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,52,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,25,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,146,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,138,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (37,88,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,11,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (46,156,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (73,145,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (71,32,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,23,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,46,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (97,57,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (61,99,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (23,169,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (83,17,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (10,66,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,131,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,78,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (26,170,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (82,120,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,120,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,47,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,21,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,69,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,100,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,123,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (74,115,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,58,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,134,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (90,40,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,192,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (94,70,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (88,182,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (91,122,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (31,35,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (86,25,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,180,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,38,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,66,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,101,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (51,73,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,85,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,70,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,1,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (79,124,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,95,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (38,60,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,32,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,143,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,114,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,67,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,178,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,82,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (82,85,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,169,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (68,157,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,81,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,39,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (52,62,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,104,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (94,182,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,69,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,116,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,168,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,124,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,26,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (53,183,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (73,164,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,179,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (79,1,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (94,53,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,33,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,195,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (85,127,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,23,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (47,147,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,94,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,67,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,7,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,174,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,78,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (3,109,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (98,99,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (42,41,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,17,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (91,132,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,62,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (69,10,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (2,200,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (69,123,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,91,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,107,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (18,193,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (47,139,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (21,135,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,141,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,197,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (65,86,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,37,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (87,147,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,35,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,35,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (98,91,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,29,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,197,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,181,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (90,55,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,157,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (1,195,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (74,2,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,196,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,188,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,149,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,9,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,144,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (71,50,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,122,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,39,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (74,163,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,175,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,76,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (87,9,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,54,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,124,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,14,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (3,127,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,97,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (2,185,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,56,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (35,16,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (97,152,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,69,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,14,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,25,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (46,67,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (81,116,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (75,39,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,142,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (5,40,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (76,20,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,187,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (78,118,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (81,187,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (37,194,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (42,70,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,138,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,177,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,2,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,123,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (89,185,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,30,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,105,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,3,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (97,161,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,187,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (40,85,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (95,160,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (35,187,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (52,146,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,154,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,143,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (22,118,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,138,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (85,130,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (86,171,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,1,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,132,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (93,6,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,97,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,84,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,92,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (74,19,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,43,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (68,98,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,141,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,198,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (43,8,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,28,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,117,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (85,17,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (16,151,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (49,67,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,17,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,166,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,131,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (57,21,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,79,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,152,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (13,175,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (33,188,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (83,9,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (85,104,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,18,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,39,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (26,130,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (49,85,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,104,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,185,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (61,46,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (73,194,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,61,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,191,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,34,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (17,17,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (33,2,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,189,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,11,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,142,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,158,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (63,156,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (23,55,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (9,133,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (83,31,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (42,78,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (69,160,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (19,40,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,193,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (75,5,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (7,36,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (100,150,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,40,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,114,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (70,98,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (99,142,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (29,18,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (72,35,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,52,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (1,160,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,96,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (45,114,3,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,144,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (76,87,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (10,162,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (4,21,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,32,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,161,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (61,123,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (36,25,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (1,186,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (33,193,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (84,66,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (91,164,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,181,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (36,122,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (21,163,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,181,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,106,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (76,150,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (56,71,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (98,65,4,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (36,12,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (59,124,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (32,60,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (2,186,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (60,130,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,183,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,9,2,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,173,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,172,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (32,15,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (67,83,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,78,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,9,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (77,31,4,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (66,117,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (6,147,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,109,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (79,34,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (12,195,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (1,122,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,20,5,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (68,175,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (26,126,4,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (58,113,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (92,170,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,131,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (11,12,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (26,45,2,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (54,200,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (34,78,1,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (26,65,5,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (25,193,3,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (78,75,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,99,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (49,195,2,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (27,51,5,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (72,135,1,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (50,68,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (36,138,1,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (89,66,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (75,112,5,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (36,19,1,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (23,7,3,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (51,80,2,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (14,71,4,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (51,40,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (58,181,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (90,172,1,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (96,54,3,'Worth the money');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (62,200,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (20,7,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (41,193,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (10,180,1,'Fast delivery');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (28,147,4,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (18,106,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (76,70,2,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (15,23,4,'Highly recommended');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (44,179,5,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (57,185,5,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (30,32,3,'Average quality');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (24,146,2,'Excellent product');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (8,125,3,'Good value');
INSERT INTO reviews(customer_id,product_id,rating,review_text)
VALUES (55,112,5,'Worth the money');
COMMIT;