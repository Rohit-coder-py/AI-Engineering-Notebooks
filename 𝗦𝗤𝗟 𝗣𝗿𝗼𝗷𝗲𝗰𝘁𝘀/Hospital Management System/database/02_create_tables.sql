
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE,
    email VARCHAR(100) UNIQUE
);



CREATE TABLE library_cards (
    card_id SERIAL PRIMARY KEY,

    student_id INT UNIQUE NOT NULL,

    card_number VARCHAR(20) UNIQUE NOT NULL,

    issue_date DATE DEFAULT CURRENT_DATE,

    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
);

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);


CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);



CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,

    title VARCHAR(200) NOT NULL,

    author_id INT NOT NULL,

    category_id INT NOT NULL,

    publication_year INT,

    copies_available INT DEFAULT 1
    CHECK (copies_available >= 0),

    FOREIGN KEY (author_id)
    REFERENCES authors(author_id),

    FOREIGN KEY (category_id)
    REFERENCES categories(category_id)
);


CREATE TABLE borrow_records (
    borrow_id SERIAL PRIMARY KEY,

    student_id INT NOT NULL,

    book_id INT NOT NULL,

    borrow_date DATE DEFAULT CURRENT_DATE,

    due_date DATE NOT NULL,

    return_date DATE,

    status VARCHAR(20)
    DEFAULT 'Borrowed'
    CHECK (status IN ('Borrowed', 'Returned')),

    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    FOREIGN KEY (book_id)
    REFERENCES books(book_id)
);