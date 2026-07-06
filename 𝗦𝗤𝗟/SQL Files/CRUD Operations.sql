-- Performing Basic Crud Operations 
-- #create

Create TABLE cars( 
id SERIAL PRIMARY KEY,
Name Varchar(50),
Cost INT,
Colour Varchar(50)
)


-- Select * from cars


INSERT INTO cars(name,cost,colour)
Values
('Maruti Suzuki',500000,'Red'),
('Pagani',9000000,'Black'),
('Fortuner',600000,'White');

-- Select * from cars


Update cars
SET colour = 'Magenta'
where name='Pagani';


Select * from cars



DELETE from cars
where name = 'Fortuner';

Select * from cars

------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------

-- # Challenges 


-- Add two more cars.

Insert into cars(name,cost,colour)
Values
('Car 1',400000,'Black'),
('Car 2',200000,'Green');


Select * from cars


-- Show only the name and cost

Select name,cost from cars


-- Show only cars whose cost is greater than 700000.

Select * from cars
where cost> 700000


-- Change the cost of Maruti Suzuki to 550000

Update cars
SET cost = 550000
where name = 'Maruti Suzuki';

Select * from cars


-- Delete the Pagani record.

Delete from cars
where name = 'Pagani';

Select * from cars