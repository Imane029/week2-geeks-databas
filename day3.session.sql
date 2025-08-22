CREATE TABLE IF NOT EXISTS language (
    language_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS film (
    film_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_year INT,
    language_id INT REFERENCES language(language_id)
);

INSERT INTO language (name) VALUES
('English'),
('French'),
('Spanish');

INSERT INTO film (title, description, release_year, language_id) VALUES
('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality.', 1999, 1),
('Le Fabuleux Destin d''Amélie Poulain', 'Amélie, a shy waitress in Paris, decides to change the lives of those around her.', 2001, 2),
('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', 2019, 1),
('Un film espagnol', 'Description d''un film en espagnol.', 2020, 3);


SELECT * FROM language;


SELECT
    film.title,
    film.description,
    language.name AS language_name
FROM
    film
JOIN
    language ON film.language_id = language.language_id;


SELECT
    film.title,
    film.description,
    language.name AS language_name
FROM
    language
LEFT JOIN
    film ON language.language_id = film.language_id;


CREATE TABLE new_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO new_film (name) VALUES
    ('The Big Lebowski'),
    ('Pulp Fiction');


CREATE TABLE customer_review (
    review_id SERIAL PRIMARY KEY,
    film_id INT REFERENCES new_film(id) ON DELETE CASCADE,
    language_id INT REFERENCES language(language_id),
    title VARCHAR(255) NOT NULL,
    score INT CHECK (score >= 1 AND score <= 10) NOT NULL,
    review_text TEXT,
    last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


INSERT INTO customer_review (film_id, language_id, title, score, review_text) VALUES
    (1, 1, 'Film génial !', 10, 'Une des meilleures comédies jamais réalisées. Le Dude est parfait.'),
    (2, 1, 'Un chef-d''œuvre classique', 9, 'Tarantino au sommet de son art. Les dialogues sont incroyables.');


DELETE FROM new_film WHERE id = 1;


SELECT * FROM customer_review;