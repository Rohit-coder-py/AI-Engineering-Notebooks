# 🎓 Student Management System

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-025E8C?style=for-the-badge&logo=postgresql&logoColor=white)
![Database](https://img.shields.io/badge/Database-Relational-success?style=for-the-badge)
![Beginner Project](https://img.shields.io/badge/Level-Beginner-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A beginner-friendly SQL project built using PostgreSQL to manage student records, marks, and fee payments. This project demonstrates database design, relationships, SQL queries, and views using a real-world Student Management System.

---

## 📌 Project Introduction

The Student Management System is designed to store and manage student information efficiently. It keeps track of student details, academic marks, and fee payment records while demonstrating the core concepts of relational database management.

This project was created to practice SQL fundamentals and build a portfolio-ready database project.

---

## ✨ Features

- Store student information
- Manage subject-wise marks
- Track fee payments
- Generate reports using SQL queries
- Create reusable database views
- Demonstrate relationships using foreign keys

---

## 🛠 Technologies Used

- PostgreSQL
- pgAdmin 4
- SQL

---

## 🗄 Database Schema

The database consists of three tables:

### Students
Stores personal details of students.

### Marks
Stores subject-wise marks for each student.

### Fees
Stores fee payment information and payment status.

---

## 📋 Tables Description

### Students

| Column | Description |
|---------|-------------|
| student_id | Primary Key |
| name | Student Name |
| gender | Gender |
| dob | Date of Birth |
| phone | Phone Number |
| email | Email Address |
| city | City |
| admission_date | Admission Date |

---

### Marks

| Column | Description |
|---------|-------------|
| mark_id | Primary Key |
| student_id | Foreign Key |
| subject | Subject Name |
| marks | Marks Obtained |

---

### Fees

| Column | Description |
|---------|-------------|
| payment_id | Primary Key |
| student_id | Foreign Key |
| amount | Fee Amount |
| payment_date | Payment Date |
| status | Paid / Pending |

---

## 🔗 Relationships

- One student can have multiple marks.
- One student can have multiple fee records.
- `student_id` is used as the foreign key in both the `marks` and `fees` tables.

Entity Relationship Diagram:


A graphical ER Diagram is available in:

```
docs/Entity_Relationships_diagram.png
```

---

## 📚 SQL Concepts Used

- Database Creation
- Tables
- Primary Keys
- Foreign Keys
- Constraints
- INSERT
- SELECT
- WHERE
- ORDER BY
- GROUP BY
- HAVING
- Aggregate Functions
- INNER JOIN
- LEFT JOIN
- Subqueries
- CASE
- Window Functions
- Views

---

## 🚀 Installation Steps

1. Clone this repository.

```bash
git clone https://github.com/your-username/Student-Management-System.git
```

2. Open PostgreSQL using pgAdmin.

3. Execute the SQL files in the following order:

```
01_create_database.sql
02_create_tables.sql
03_insert_sample_data.sql
04_queries.sql
05_views.sql
```

4. Explore the database using the provided queries and views.

---

## 💻 Sample Queries

Some example operations included in this project:

- Display all students
- Find students by city
- Student marks report
- Student fee report
- Students with pending fees
- Students with paid fees
- Average marks of each student
- Top-performing students
- Complete student report using JOINs
- Ranking students using Window Functions

---

## 📷 Screenshots

### Tables
```
screenshots/tables.png
```

### Sample Data
```
screenshots/sample_data.png
```

### Views
```
screenshots/views.png
```

---

## 👨‍💻 Author

**Rohit Jha**

Aspiring AI Engineer | Data Science & Machine Learning Enthusiast

GitHub: https://github.com/your-github-username

LinkedIn: https://linkedin.com/in/your-linkedin-profile

---

## 📄 License

This project is created for educational and portfolio purposes.