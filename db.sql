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
    popularity INTEGER DEFAULT 5, -- Number of likes
    reviews_number INTEGER DEFAULT 1,
    alcohol_content INTEGER NOT NULL,
    recipe_by TEXT NOT NULL
);
ALTER TABLE cocktails ADD COLUMN method TEXT NOT NULL DEFAULT '';
ALTER TABLE cocktails ADD COLUMN created_by INTEGER NOT NULL;
ALTER TABLE cocktails ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE;
SELECT * FROM cocktails;

-- ALTER TABLE cocktails RENAME TO old_cocktails;
CREATE TABLE cocktails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    popularity INTEGER DEFAULT 5,
    reviews_number INTEGER DEFAULT 1,
    alcohol_content INTEGER NOT NULL,
    recipe_by TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT '',
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
);

INSERT INTO cocktails (id, name, image, popularity, reviews_number, alcohol_content, recipe_by, method, created_by)
SELECT id, name, image, popularity, reviews_number, alcohol_content, recipe_by, method, created_by FROM old_cocktails;

SELECT * FROM cocktails;


CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO ingredients (name) VALUES
('Vodka'),
('Gin'),
('Rum'),
('Tequila'),
('Whiskey'),
('Triple Sec'),
('Vermouth'),
('Campari'),
('Cointreau'),
('Amaretto'),
('Bitters'),
('Grenadine'),
('Simple Syrup'),
('Lime Juice'),
('Lemon Juice'),
('Orange Juice'),
('Pineapple Juice'),
('Cranberry Juice'),
('Coconut Cream'),
('Tonic Water'),
('Soda Water'),
('Cola'),
('Ginger Beer'),
('Mint Leaves'),
('Sugar Cubes'),
('Egg White'),
('Angostura Bitters'),
('Blue Curaçao'),
('Sweet Vermouth'),
('Dry Vermouth'),
('Cherry Liqueur'),
('Peach Schnapps'),
('Baileys Irish Cream'),
('Coffee Liqueur'),
('Absinthe'),
('Mezcal'),
('Maraschino Liqueur'),
('Chartreuse'),
('Aperol'),
('Honey Syrup'),
('Club Soda'),
('Dark Rum'),
('Prosecco'),
('Irish Whiskey'),
('Espresso'),
('Cinnamon'),
('Nutmeg'),
('Bourbon'),
('Maple Syrup'),
('Apple Cider'),
('Red Wine'),
('Egg Nog');

INSERT INTO cocktails (name,image,popularity, reviews_number, alcohol_content,recipe_by) VALUES
('Cosmopolitan', 'cosmopolitan.jpg', 50, 20, 1, 'c4rriebradshaw'),
('Old Fashioned', 'old_fashioned.jpg', 80, 40, 1, 'mhobbes'),
('Aperol Spritz', 'aperol_spritz.jpg', 60, 30, 1, 'charY0rk'),
('Dirty Martini', 'dirty_martini.jpg', 55, 25, 1, 'SamJones'),
('Vodka with Coke', 'vodka_with_coke.jpg', 123, 100, 1, 'OP'),
('Whiskey with Coke', 'whiskey_with_coke.jpg', 90, 50, 1, 'OP'),
('Mojito', 'mojito.jpg', 70, 35, 1, 'BartenderX'),
('Margarita', 'margarita.jpg', 85, 45, 1, 'DrinkMaster42'),
('Pina Colada', 'pina_colada.jpg', 78, 38, 1, 'TropicalJoe'),
('Long Island Iced Tea', 'long_island_iced_tea.jpg', 95, 50, 1, 'PartyGuru'),
('Negroni', 'negroni.jpg', 65, 28, 1, 'ClassicCocktail'),
('Espresso Martini', 'espresso_martini.jpg', 88, 47, 1, 'CaffeineAddict'),
('Irish Coffee', 'irish_coffee.jpg', 58, 22, 1, 'DublinBartender'),
('Mai Tai', 'mai_tai.jpg', 75, 33, 1, 'TikiMan'),
('Daiquiri', 'daiquiri.jpg', 72, 31, 1, 'CubaLibre'),
('Manhattan', 'manhattan.jpg', 82, 39, 1, 'NYCDrinker'),
('Boulevardier', 'boulevardier.jpg', 62, 27, 1, 'WhiskeyAficionado'),
('Sazerac', 'sazerac.jpg', 55, 20, 1, 'NewOrleansMixologist');

-- UPDATE cocktails SET created_by = 1 WHERE id = 1;
-- UPDATE cocktails SET created_by = 2 WHERE id = 2;
-- UPDATE cocktails SET created_by = 3 WHERE id = 3;
-- UPDATE cocktails SET created_by = 4 WHERE id = 4;
-- UPDATE cocktails SET created_by = 5 WHERE id = 5;
-- UPDATE cocktails SET created_by = 6 WHERE id = 6;
-- UPDATE cocktails SET created_by = 7 WHERE id = 7;
-- UPDATE cocktails SET created_by = 8 WHERE id = 8;
-- UPDATE cocktails SET created_by = 9 WHERE id = 9;
-- UPDATE cocktails SET created_by = 10 WHERE id = 10;
-- UPDATE cocktails SET created_by = 11 WHERE id = 11;
-- UPDATE cocktails SET created_by = 12 WHERE id = 12;
-- UPDATE cocktails SET created_by = 13 WHERE id = 13;
-- UPDATE cocktails SET created_by = 14 WHERE id = 14;
-- UPDATE cocktails SET created_by = 15 WHERE id = 15;
-- UPDATE cocktails SET created_by = 16 WHERE id = 16;
-- UPDATE cocktails SET created_by = 17 WHERE id = 17;
-- UPDATE cocktails SET created_by = 18 WHERE id = 18;
-- UPDATE cocktails SET created_by = 19 WHERE id = 19;
-- UPDATE cocktails SET created_by = 20 WHERE id = 20;
-- UPDATE cocktails SET created_by = 21 WHERE id = 21;
-- UPDATE cocktails SET created_by = 22 WHERE id = 22;
-- UPDATE cocktails SET created_by = 23 WHERE id = 23;
-- UPDATE cocktails SET created_by = 24 WHERE id = 24;


CREATE TABLE IF NOT EXISTS cocktail_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cocktail_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    UNIQUE (cocktail_id, ingredient_id) 
);

CREATE TABLE IF NOT EXISTS favorites (
    favorites_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cocktail_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE
);

INSERT INTO favorites (user_id, cocktail_id) VALUES
(3, 1);

SELECT * FROM favorites;

INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id) VALUES
-- Cosmopolitan
(1, 1),
(1, 9),
(1, 18),
(1, 14),
-- Old Fashioned
(2, 5),
(2, 11),
(2, 24),
-- Aperol Spritz
(3, 39),
(3, 44),
(3, 21),
-- Dirty Martini
(4, 2),
(4, 30),
-- Vodka with Coke
(5, 1),
(5, 22),
-- Whiskey with Coke
(6, 5),
(6, 22),
-- Mojito
(7, 3),
(7, 24),
(7, 14),
(7, 23),
(7, 21),
-- Margarita
(8, 4),
(8, 9),
(8, 14),
-- Pina Colada
(9, 3),
(9, 19),
(9, 17),
-- Long Island Iced Tea
(10, 1),
(10, 2),
(10, 3),
(10, 4),
(10, 6),
(10, 14),
(10, 22),
-- Negroni
(11, 2),
(11, 7),
(11, 8),
-- Espresso Martini
(12, 1),
(12, 34),
(12, 43),
-- Irish Coffee
(13, 45),
(13, 34),
(13, 43),
-- Mai Tai
(14, 3),
(14, 31),
(14, 14),
-- Daiquiri
(15, 3),
(15, 14),
(15, 12),
-- Manhattan
(16, 5),
(16, 7),
(16, 11),
-- Boulevardier
(17, 5),
(17, 8),
(17, 7),
-- Sazerac
(18, 5),
(18, 35),
(18, 11),
(18, 24);

INSERT INTO favorites (user_id, cocktail_id) VALUES
(3, 1);

SELECT name FROM ingredients;


SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC;

SELECT * FROM cocktail_ingredients;
SELECT * FROM cocktails;

CREATE TABLE follows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follower_id INTEGER NOT NULL,
    following_id INTEGER NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (following_id) REFERENCES users(id)
);

SELECT * FROM follows;

SELECT * FROM users;
