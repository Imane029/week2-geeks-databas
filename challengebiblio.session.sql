CREATE TABLE Customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE Customer_profile (
    id SERIAL PRIMARY KEY,
    isLoggedIn BOOLEAN DEFAULT FALSE,
    customer_id INT UNIQUE REFERENCES Customer(id)
);

INSERT INTO Customer (first_name, last_name) VALUES
('John', 'Doe'),
('Jerome', 'Lalu'),
('Lea', 'Rive');

INSERT INTO Customer_profile (isLoggedIn, customer_id) VALUES
(TRUE, (SELECT id FROM Customer WHERE first_name = 'John')),
(FALSE, (SELECT id FROM Customer WHERE first_name = 'Jerome'));

SELECT C.first_name
FROM Customer AS C
JOIN Customer_profile AS CP
ON C.id = CP.customer_id
WHERE CP.isLoggedIn = TRUE;

SELECT C.first_name, CP.isLoggedIn
FROM Customer AS C
LEFT JOIN Customer_profile AS CP
ON C.id = CP.customer_id;

SELECT COUNT(C.id) AS NotLoggedInCustomers
FROM Customer AS C
LEFT JOIN Customer_profile AS CP
ON C.id = CP.customer_id
WHERE CP.isLoggedIn IS NULL OR CP.isLoggedIn = FALSE;

CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);

CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    age INT,
    CHECK (age <= 15)
);

INSERT INTO Book (title, author) VALUES
('Alice In Wonderland', 'Lewis Carroll'),
('Harry Potter', 'J.K Rowling'),
('To kill a mockingbird', 'Harper Lee');

INSERT INTO Student (name, age) VALUES
('John', 12),
('Lera', 11),
('Patrick', 10),
('Bob', 14);

CREATE TABLE Library (
    book_fk_id INT REFERENCES Book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    student_fk_id INT REFERENCES Student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    borrowed_date DATE,
    PRIMARY KEY (book_fk_id, student_fk_id)
);

INSERT INTO Library (book_fk_id, student_fk_id, borrowed_date) VALUES
((SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'), (SELECT student_id FROM Student WHERE name = 'John'), '2022-02-15'),
((SELECT book_id FROM Book WHERE title = 'To kill a mockingbird'), (SELECT student_id FROM Student WHERE name = 'Bob'), '2021-03-03'),
((SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'), (SELECT student_id FROM Student WHERE name = 'Lera'), '2021-05-23'),
((SELECT book_id FROM Book WHERE title = 'Harry Potter'), (SELECT student_id FROM Student WHERE name = 'Bob'), '2021-08-12');

SELECT * FROM Library;

SELECT S.name AS student_name, B.title AS book_title
FROM Library AS L
JOIN Student AS S ON L.student_fk_id = S.student_id
JOIN Book AS B ON L.book_fk_id = B.book_id;

SELECT AVG(S.age)
FROM Student AS S
JOIN Library AS L
ON S.student_id = L.student_fk_id
JOIN Book AS B
ON L.book_fk_id = B.book_id
WHERE B.title = 'Alice In Wonderland';

DELETE FROM Student WHERE name = 'John';

SELECT * FROM Library;
