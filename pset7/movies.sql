SELECT title from movies WHERE year == "2008";

SELECT birth FROM people WHERE name == "Emma Stone";

SELECT title FROM movies WHERE year >= "2018" ORDER BY title;

SELECT COUNT(*) from ratings WHERE rating == "10.0";

SELECT title, year FROM movies WHERE title LIKE "Harry Potter%" ORDER BY year;

SELECT AVG(rating) from ratings JOIN movies ON movies.id = ratings.movie_id where year = "2012";

SELECT title, rating from ratings JOIN movies ON movies.id = ratings.movie_id WHERE year = "2010" ORDER BY rating DESC, title ASC;

SELECT name FROM
((stars INNER JOIN movies ON stars.movie_id = movies.id)
INNER JOIN people ON people.id = stars.person_id)
WHERE title = "Toy Story";

SELECT DISTINCT name FROM
((stars INNER JOIN movies ON stars.movie_id = movies.id)
INNER JOIN people ON people.id = stars.person_id)
WHERE year = "2004" ORDER BY birth;

SELECT DISTINCT name FROM
((people INNER JOIN directors on people.id = directors.person_id)
INNER JOIN ratings on directors.movie_id = ratings.movie_id)
WHERE rating >= 9.0;

SELECT movies.title from people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
JOIN ratings on movies.id = ratings.movie_id
WHERE people.name = "Chadwick Boseman"
ORDER BY rating DESC LIMIT 5;

SELECT title FROM
((movies INNER JOIN stars on movies.id = stars.movie_id)
INNER JOIN people on stars.person_id = people.id)
WHERE people.name = "Johnny Depp" AND title IN
(SELECT title FROM
((movies INNER JOIN stars on movies.id = stars.movie_id)
INNER JOIN people on stars.person_id = people.id)
WHERE people.name = "Helena Bonham Carter");

SELECT DISTINCT name FROM
people JOIN stars ON people.id = stars.person_id
WHERE movie_id IN
(SELECT movie_id FROM stars JOIN people on
stars.person_id = people.id
WHERE people.name = "Kevin Bacon" AND people.birth = "1958")
AND name != "Kevin Bacon";
