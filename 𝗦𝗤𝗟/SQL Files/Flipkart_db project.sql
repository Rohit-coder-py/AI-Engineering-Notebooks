Create Table flipkart_db(

Product_ID serial unique Primary Key,
Product_name Varchar(180) Not Null,
skucode CHAR(8) Unique check (char_length(skucode)=8),
Price_Max int,
Stock_Quantity INT CHECK (Stock_Quantity>=0),
is_available Boolean DEFAULT True,
Category Text Not Null,
Date_of_addition TIMESTAMP default now() )

Select * from flipkart_db


-- now lets insert values

Insert into flipkart_db (Product_name,skucode,Price_Max,Stock_Quantity,is_available,Category)
Values
('Wireless Mouse','87654322',799,25,True,'Electronics'),
('Gaming Keyboard','87654323',2499,15,True,'Electronics'),
('Bluetooth Speaker','87654324',1899,30,True,'Electronics'),
('LED Monitor','87654325',11999,8,True,'Computers'),
('Laptop Stand','87654326',999,40,True,'Accessories'),
('USB Cable','87654327',299,100,True,'Accessories'),
('Smart Watch','87654328',6999,18,True,'Wearables'),
('Fitness Band','87654329',2499,20,True,'Wearables'),
('Mobile Cover','87654330',399,60,True,'Mobile Accessories'),
('Power Bank','87654331',1499,35,True,'Electronics'),
('Water Bottle','87654332',499,50,True,'Home'),
('Office Chair','87654333',6999,7,True,'Furniture'),
('Study Table','87654334',5499,10,True,'Furniture'),
('Notebook Pack','87654335',299,120,True,'Stationery'),
('Gel Pen Set','87654336',199,90,True,'Stationery'),
('Cricket Bat','87654337',2499,12,True,'Sports'),
('Football','87654338',799,22,True,'Sports'),
('Yoga Mat','87654339',899,17,True,'Fitness'),
('Dumbbell Set','87654340',3499,9,True,'Fitness'),
('Cookware Set','87654341',4599,11,True,'Kitchen'),
('Mixer Grinder','87654342',3799,8,True,'Kitchen'),
('Air Fryer','87654343',5999,6,True,'Kitchen'),
('Vacuum Cleaner','87654344',7499,5,True,'Home Appliances'),
('Electric Iron','87654345',1299,20,True,'Home Appliances'),
('Hair Dryer','87654346',1599,16,True,'Beauty'),
('Face Wash','87654347',299,70,True,'Beauty'),
('Perfume','87654348',1899,15,True,'Beauty'),
('Sunglasses','87654349',999,27,True,'Fashion'),
('Leather Wallet','87654350',799,30,True,'Fashion'),
('Backpack','87654351',1499,18,True,'Bags'),
('Travel Bag','87654352',2599,12,True,'Bags'),
('School Bag','87654353',1299,25,True,'Bags'),
('Digital Clock','87654354',699,14,True,'Home Decor'),
('Wall Clock','87654355',999,19,True,'Home Decor'),
('Table Lamp','87654356',799,28,True,'Lighting'),
('LED Bulb','87654357',199,80,True,'Lighting'),
('Ceiling Fan','87654358',2499,13,True,'Electrical'),
('Extension Board','87654359',699,35,True,'Electrical'),
('Phone Charger','87654360',599,55,True,'Electronics'),
('Tablet','87654361',18999,6,True,'Electronics'),
('Printer','87654362',8999,4,True,'Computers'),
('Webcam','87654363',2499,21,True,'Computers'),
('Microphone','87654364',3199,15,True,'Audio'),
('Tripod','87654365',1199,26,True,'Photography'),
('DSLR Camera','87654366',54999,3,True,'Photography'),
('Toy Train','87654367',999,18,True,'Toys'),
('Building Blocks','87654368',1499,16,True,'Toys'),
('Puzzle Game','87654369',699,22,True,'Toys'),
('Remote Car','87654370',2499,9,True,'Toys'),
('Baby Doll','87654371',899,14,True,'Toys'),
('Novel Book','87654372',499,45,True,'Books'),
('Dictionary','87654373',699,12,True,'Books'),
('Cookbook','87654374',799,10,True,'Books'),
('Headphones','87654375',2999,20,True,'Audio'),
('Earbuds','87654376',3499,24,True,'Audio'),
('Soundbar','87654377',8999,5,True,'Audio'),
('Coffee Mug','87654378',399,60,True,'Kitchen'),
('Dinner Set','87654379',2999,8,True,'Kitchen'),
('Bedsheet','87654380',999,30,True,'Home'),
('Blanket','87654381',1999,15,True,'Home'),
('Curtains','87654382',1599,18,True,'Home'),
('T-Shirt','87654383',699,50,True,'Fashion'),
('Jeans','87654384',1499,25,True,'Fashion'),
('Jacket','87654385',2999,10,True,'Fashion'),
('Sports Shoes','87654386',3999,16,True,'Footwear'),
('Running Shoes','87654387',3499,12,True,'Footwear'),
('Slippers','87654388',499,35,True,'Footwear'),
('Formal Shoes','87654389',2799,9,True,'Footwear'),
('Watch Strap','87654390',299,44,True,'Accessories'),
('Mouse Pad','87654391',249,75,True,'Computers'),
('External HDD','87654392',5499,11,True,'Computers'),
('SSD 1TB','87654393',6999,13,True,'Computers'),
('RAM 16GB','87654394',4299,19,True,'Computers'),
('Graphics Card','87654395',35999,2,True,'Computers'),
('CPU Cooler','87654396',2499,14,True,'Computers'),
('Mechanical Pencil','87654397',99,120,True,'Stationery'),
('Marker Set','87654398',249,70,True,'Stationery'),
('Sketch Book','87654399',349,45,True,'Stationery'),
('Water Colors','87654400',599,30,True,'Art'),
('Paint Brush Set','87654401',399,40,True,'Art'),
('Canvas Board','87654402',699,20,True,'Art'),
('Keyboard Cover','87654403',299,26,True,'Accessories'),
('Monitor Cleaner','87654404',199,60,True,'Accessories'),
('Phone Holder','87654405',399,35,True,'Accessories'),
('Car Charger','87654406',699,28,True,'Automotive'),
('Helmet','87654407',1799,18,True,'Automotive'),
('Car Vacuum','87654408',2299,9,True,'Automotive'),
('Bike Cover','87654409',899,15,True,'Automotive'),
('Pressure Cooker','87654410',2499,12,True,'Kitchen'),
('Rice Cooker','87654411',3299,10,True,'Kitchen'),
('Juicer','87654412',2899,11,True,'Kitchen'),
('Toaster','87654413',1799,13,True,'Kitchen'),
('Electric Kettle','87654414',1499,20,True,'Kitchen'),
('Gaming Chair','87654415',9999,4,True,'Furniture'),
('Bean Bag','87654416',2499,14,True,'Furniture'),
('Bookshelf','87654417',5499,8,True,'Furniture'),
('Smart TV','87654418',45999,5,True,'Electronics'),
('Streaming Stick','87654419',3499,18,True,'Electronics'),
('Router','87654420',2299,21,True,'Networking');




--phase 3

-- clause and operators and agreegation functions 
-- query extracton questions 

-- Q1. Show the name and price of all products.



SELECT Product_name, Price_Max FROM flipkart_db;



-- Q2. Show all products where the category is 'Electronics'

Select * from flipkart_db  where category='Electronics';


-- Q3. Group products by category. Show each category once.

SELECT Category FROM flipkart_db
GROUP BY Category;


-- Q4. Show categories that have more than 1 product. (Use after
-- GROUP BY)

SELECT Category,
       COUNT(*) AS Total_Products
FROM flipkart_db
GROUP BY Category
HAVING COUNT(*) > 1;


-- Q5. Show all products sorted by price in ascending order

SELECT * FROM flipkart_db ORDER BY Stock_quantity desc;

-- asc and desc

Select * from flipkart_db ORDER BY Category , Price_Max desc;


-- Q6. Show only the first 3 products from the table.

Select * from flipkart_db LIMIT 3;


-- Q7. Show product name as "Item_Name" and price as "Item_Price"

SELECT Product_name, Price_Max FROM flipkart_db;

SELECT Product_name AS Item_Name,Price_Max AS Item_Price
FROM flipkart_db;


"tem_Price".

-- Q8. Show all the unique categories from the products

Select DISTINCT category from flipkart_db;


