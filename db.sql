CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cocktails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL, -- Path to image in static folder
    popularity INTEGER DEFAULT 0, -- Number of likes
    reviews_number INTEGER DEFAULT 0,
    alcohol_content INTEGER NOT NULL,
    recipe TEXT NOT NULL,
    recipe_by TEXT NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE 
);

INSERT INTO cocktails (name,image,popularity, reviews_number, alcohol_content,recipe_by) VALUES
('Cosmopolitan','cosmopolitan.jpg',0, 1, 1,'c4rriebradshaw'),
('Old Fashioned','old_fashioned.jpg',7, 4, 1, 'mhobbes'),
('Aperol Spritz','aperol_spritz.jpg',1, 1, 1, 'charY0rk'),
('Dirty Martini','dirty_martini.jpg',2, 1, 1, 'SamJones'),
('Vodka with coke', 'vodka_with_coke', 123, 100, 1, 'OP'),
('Whiskey with coke', 'whiskey_with_coke', 15, 3, 1, 'OP');


SELECT * FROM users;
SELECT * FROM cocktails;

SELECT name,popularity/reviews_number FROM cocktails ORDER BY popularity/reviews_number DESC;

ALTER TABLE cocktails ADD COLUMN created_by INTEGER NOT NULL DEFAULT 1;

UPDATE cocktails SET created_by = 1 WHERE name = 'Cosmopolitan';
UPDATE cocktails SET created_by = 2 WHERE name = 'Old Fashioned';
UPDATE cocktails SET created_by = 3 WHERE name = 'Aperol Spritz';
UPDATE cocktails SET created_by = 4 WHERE name = 'Dirty Martini';
UPDATE cocktails SET created_by = 5 WHERE name = 'Vodka with coke';
UPDATE cocktails SET created_by = 6 WHERE name = 'Whiskey with coke';

CREATE TABLE IF NOT EXISTS favorites (
    favorites_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cocktail_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE
);

INSERT INTO favorites (user_id, cocktail_id) VALUES
(3, 1);

SELECT * from Favorites;
