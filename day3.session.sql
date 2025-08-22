--CREATE TABLE IF NOT EXISTS language (
    --language_id SERIAL PRIMARY KEY,
    --name VARCHAR(50) NOT NULL
--);

--CREATE TABLE IF NOT EXISTS film (
    --film_id SERIAL PRIMARY KEY,
    --title VARCHAR(255) NOT NULL,
    --description TEXT,
    --release_year INT,
    --language_id INT REFERENCES language(language_id)
--);

--INSERT INTO language (name) VALUES
--('English'),
--('French'),
--('Spanish');

--INSERT INTO film (title, description, release_year, language_id) VALUES
--('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality.', 1999, 1),
--('Le Fabuleux Destin d''Amélie Poulain', 'Amélie, a shy waitress in Paris, decides to change the lives of those around her.', 2001, 2),
--('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', 2019, 1),
--('Un film espagnol', 'Description d''un film en espagnol.', 2020, 3);


--SELECT * FROM language;

--SELECT
    --film.title,
    --film.description,
    --language.name AS language_name
--FROM
    --film
--JOIN
   --language ON film.language_id = language.language_id;

--SELECT
    --film.title,
    --film.description,
    --language.name AS language_name
--FROM
    --language
--LEFT JOIN
    --film ON language.language_id = film.language_id;


-- CREATE TABLE new_film (
   -- id SERIAL PRIMARY KEY,
   -- name VARCHAR(255) NOT NULL
-- );

--INSERT INTO new_film (name) VALUES
    --('The Big Lebowski'),
    --('Pulp Fiction');

--SELECT * FROM new_film;

--CREATE TABLE customer_review (
    --review_id SERIAL PRIMARY KEY,
    --film_id INT REFERENCES new_film(id) ON DELETE CASCADE,
    --language_id INT REFERENCES language(language_id),
    --title VARCHAR(255) NOT NULL,
    --score INT CHECK (score >= 1 AND score <= 10) NOT NULL,
    --review_text TEXT,
    --last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW()
--);

--INSERT INTO customer_review (film_id, language_id, title, score, review_text) VALUES
    --(1, 1, 'Film génial !', 10, 'Une des meilleures comédies jamais réalisées. Le Dude est parfait.'),
   -- (2, 1, 'Un chef-d''œuvre classique', 9, 'Tarantino au sommet de son art. Les dialogues sont incroyables.');

--DELETE FROM new_film WHERE id = 1;
--SELECT * FROM customer_review;


UPDATE film
SET
    language_id = (SELECT language_id FROM language WHERE name = 'French')
WHERE
    title = 'The Matrix';

UPDATE film
SET
    language_id = (SELECT language_id FROM language WHERE name = 'English')
WHERE
    title = 'Le Fabuleux Destin d''Amélie Poulain';

SELECT
    film.title,
    language.name AS language_name
FROM
    film
JOIN
    language ON film.language_id = language.language_id
WHERE
    film.title IN ('The Matrix', 'Le Fabuleux Destin d''Amélie Poulain');

DROP TABLE customer_review;

SELECT COUNT(*) AS outstanding_rentals
FROM rental
WHERE return_date IS NULL;

SELECT f.title, f.rental_rate
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NULL
ORDER BY f.rental_rate DESC
LIMIT 30;

SELECT f.title
FROM film f
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE a.first_name = 'Penelope'
AND a.last_name = 'Monroe'
AND f.description ILIKE '%sumo wrestler%';

SELECT title
FROM film
WHERE length < 60
AND rating = 'R'
AND description ILIKE '%documentary%';

SELECT f.title
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN customer c ON r.customer_id = c.customer_id
JOIN payment p ON r.rental_id = p.rental_id
WHERE c.first_name = 'Matthew' AND c.last_name = 'Mahan'
AND p.amount > 4.00
AND r.return_date BETWEEN '2005-07-28' AND '2005-08-01';

SELECT f.title
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN customer c ON r.customer_id = c.customer_id
WHERE c.first_name = 'Matthew' AND c.last_name = 'Mahan'
AND (f.title ILIKE '%boat%' OR f.description ILIKE '%boat%')
ORDER BY f.replacement_cost DESC
LIMIT 1;
