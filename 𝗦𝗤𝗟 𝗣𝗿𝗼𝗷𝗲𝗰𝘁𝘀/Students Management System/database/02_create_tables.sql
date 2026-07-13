CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50) NOT NULL,
    admission_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(50) NOT NULL,
    marks INT NOT NULL CHECK (marks BETWEEN 0 AND 100),

    CONSTRAINT fk_marks_student
    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
    ON DELETE CASCADE
);


CREATE TABLE fees (
    payment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    payment_date DATE,
    status VARCHAR(20) DEFAULT 'Pending'
        CHECK (status IN ('Paid', 'Pending')),

    CONSTRAINT fk_fees_student
    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
    ON DELETE CASCADE
);



Select * from students join marks on students.student_id 